from fastapi import APIRouter , status , Depends , Request
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import JWTError, jwt

from typing import Optional, Union, Annotated

from schemas import MatchModel,TeamModel,Settings
from db import engine, Base, Session
from models import Match, Team

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/admin/login")
settings = Settings()

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
) 

db = Session(bind=engine)

router = APIRouter(
    prefix='/api/matches',
    tags=['Match API']
)

@router.get("/")
async def all_matches():
    return db.query(Match).all()

@router.get("/{team_id}")
async def get_match_by_id(team_id : int):
    return db.query(Team).filter(Team.team_id == team_id).first().matches

@router.post("/" , response_model=MatchModel , status_code= status.HTTP_201_CREATED)
async def add_match(match_details:MatchModel, token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("subject") 
    except JWTError:
        raise credentials_exception

    if(match_details.team1_id == match_details.team2_id) : 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Same Opponents")

    team1 = db.query(Team).filter(Team.team_id == match_details.team1_id).first()
    team2 = db.query(Team).filter(Team.team_id == match_details.team2_id).first()


    if team1 is None or team2 is None : 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                             detail="Team {} or Team {} Team Doesnt Exist"
                             .format(match_details.team1_id , match_details.team2_id)
                            )


    new_match = Match(
        venue = match_details.venue,
        datetime = match_details.datetime,
        team1_id = match_details.team1_id,
        team2_id = match_details.team2_id
    )

    db.add(new_match)
    db.commit()

    return new_match