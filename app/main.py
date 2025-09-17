from fastapi import FastAPI
from app.routers import auth,users,generate
from app.core.databases import create_tables


app=FastAPI()

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(generate.router)

@app.get("/")
def read_root():
  return {"Hello" : "World"}

