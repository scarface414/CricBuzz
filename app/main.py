from fastapi import FastAPI
import match_routes, team_routes, auth_routes, player_routes

app = FastAPI() 
app.include_router(match_routes.router)
app.include_router(team_routes.router)
app.include_router(auth_routes.router)
app.include_router(player_routes.router)
