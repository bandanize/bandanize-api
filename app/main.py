import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from v1.config import engine
import v1.bands.routes as bands
import v1.bands.models as BandModels
import v1.users.routes as users
import v1.users.models as UserModels

BandModels.Base.metadata.create_all(bind=engine)
UserModels.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bands.router, prefix="/v1/band", tags=["band"])
app.include_router(users.router, prefix="/v1/user", tags=["user"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)