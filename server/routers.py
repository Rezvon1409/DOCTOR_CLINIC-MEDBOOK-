from fastapi import FastAPI
from accounts.views import auth


app = FastAPI()
app.include_router(auth, prefix="/auth", tags=["accounts"])


