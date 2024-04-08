from fastapi import APIRouter , status , Depends , Request
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from werkzeug.security import generate_password_hash , check_password_hash

from typing import Optional, Union, Annotated
from datetime import timedelta, datetime, timezone

from schemas import UserModel, AdminModel, Settings
from db import engine, Base, Session
from models import User

from jose import JWTError, jwt

db = Session(bind=engine)

settings = Settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/admin/login")

router = APIRouter(
    prefix='/api/admin',
    tags=['Auth API']
)


@router.post('/signup' , response_model=AdminModel, status_code = status.HTTP_201_CREATED)
async def signup(user:UserModel) : 
    db_email = db.query(User).filter(User.email == user.email).first()

    if db_email is not None : 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user with email already exists")
    
    db_username = db.query(User).filter(User.username == user.username).first()

    if db_username is not None : 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user with username already exists")

    print("\n" , user , "\n")  

    new_user = User(
        username = user.username,
        email = user.email , 
        password = generate_password_hash(user.password),
        is_admin = True
    )

    db.add(new_user)
    db.commit()

    return new_user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=15))

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm= settings.ALGORITHM)
    return encoded_jwt

@router.post('/login' , status_code = status.HTTP_200_OK)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) : 
    db_user = db.query(User).filter(User.username == form_data.username).first()

    if db_user and check_password_hash( db_user.password , form_data.password) : 
        access_token_expires = timedelta(minutes= settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"subject": db_user.username}, expires_delta= access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="valid username or password required",
            headers={"WWW-Authenticate": "Bearer"},
        )
