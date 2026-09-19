from fastapi import FastAPI
from .modules.users.router import userrouter
from .modules.restaurants.router import resto_router

app = FastAPI()
app.include_router(userrouter)
app.include_router(resto_router)

@app.get("/")
def read_root() -> dict[str, str]:
	return {"message": "Hello World"}
