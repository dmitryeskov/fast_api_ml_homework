import os
import joblib
import dotenv

from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import Auth
from app.db import JsonDb
from app.schemas import Features, Token

dotenv.load_dotenv()

CWD = os.getcwd()
MODELS_DIR = "models/"
MODEL_FILE = "wine_model.pkl"
MODEL_PATH = os.path.normpath(os.path.join(CWD, MODELS_DIR, MODEL_FILE))
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "1"))

app = FastAPI()
db = JsonDb().get_db()
auth = Auth(db=db)
model = joblib.load(os.path.join(CWD, MODELS_DIR, MODEL_FILE))


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect user name or password",
            headers={"WWW-Authentificate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/make_inference")
async def make_inference(
    features: Features, current_user=Depends(auth.get_current_user)
):
    prediction = model.predict([features.features])

    return {"prediction": int(prediction[0]), "user": current_user}
