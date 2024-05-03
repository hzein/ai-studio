import logging
import shutil
import subprocess
import os
import time
import uvicorn
import torch
import utils

# API queue addition
from threading import Lock

# FastAPI
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated

# Database
from sql_db import models
from sql_db.database import SessionLocal, engine
from sqlalchemy.orm import Session

# Local imports
from run_ai_studio import retrieval_qa_pipline
from config import MODEL_BASENAME, SAVE_QA, SHOW_SOURCES, USE_HISTORY
from routers import users, auth
from routers.auth import get_current_active_user

request_lock = Lock()

device = "cuda" if torch.cuda.is_available() else "cpu"

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s",
    level=logging.INFO,
)
logging.info(f"Running on: {device}")
logging.info(f"Display Source Documents set to: {SHOW_SOURCES}")
logging.info(f"Use history set to: {USE_HISTORY}")

qa = retrieval_qa_pipline(
    device_type=device,
    use_history=False,
    promptTemplate_type="mistral",
)


class User(BaseModel):
    username: str
    email: str
    is_active: bool = True


class UserInDb(User):
    hashed_password: str


class TextIn(BaseModel):
    text: str
    key: str


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dependency
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_active_user)]

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://localhost:5000",
]

app.add_middleware(CORSMiddleware, allow_origins=origins)


@app.get("/")
def home():
    return {
        "health_check": "OK",
        "model": MODEL_BASENAME,
        "status": "Running",
    }


@app.post("/chat/")
def predict(user: user_dependency, payload: TextIn):

    user_prompt = payload.text
    if user_prompt:
        # Get the answer from the chain
        start_time = time.time()
        res = qa.invoke(user_prompt)
        end_time = time.time()
        answer, docs = res["result"], res["source_documents"]

        # Log the Q&A to CSV only if save_qa is True
        time_taken = end_time - start_time
        if SAVE_QA:
            utils.log_to_csv(MODEL_BASENAME, time_taken, user_prompt, answer)

        prompt_response_dict = {
            "Prompt": user_prompt,
            "Answer": answer,
        }

        prompt_response_dict["Sources"] = []

        if SHOW_SOURCES:
            for document in docs:
                prompt_response_dict["Sources"].append(
                    (
                        os.path.basename(str(document.metadata["source"])),
                        str(document.page_content),
                    )
                )
        else:
            prompt_response_dict["Sources"] = None

        return prompt_response_dict
    else:
        return "No user prompt received"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
