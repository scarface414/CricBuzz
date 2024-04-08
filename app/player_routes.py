from fastapi import APIRouter , status , Depends , Request
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import JWTError, jwt

from typing import Optional, Union, Annotated

from schemas import MatchModel,TeamModel,PlayerModel,Settings
from db import engine, Base, Session
from models import Player


router = APIRouter(
    prefix='/api/players',
    tags=['Player API']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/admin/login")
settings = Settings()

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
) 

db = Session(bind=engine)

@router.get("/")
async def all_players():
    return db.query(Player).all()

@router.post("/", response_model=PlayerModel , status_code= status.HTTP_201_CREATED)
async def create_player(player:PlayerModel , token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("subject") 
    except JWTError:
        raise credentials_exception

    new_player = Player(
        name = player.name,
        matches_played = player.matches_played,
        runs = player.runs,
        wickets = player.wickets
    )

    db.add(new_player)
    db.commit()

    return  new_player

@router.get("/{player_id}/teams") 
async def get_teams_of_player_by_playerid(player_id : int) : 
    player = db.query(Player).filter(Player.player_id == player_id).first()

    if player is None : 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Player Does Not Exist")
    
    teams = jsonable_encoder(player.teams)

    return {
        "player_id" : player_id,
        "name" : player.name,
        "teams" : teams
    }
