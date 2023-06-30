from fastapi import FastAPI
from app import models
from app.database import Base, engine
from app.router import user, auth, book, review

models.Base.metadata.create_all(engine)

app = FastAPI(
    title="Book Catelog"
)

@app.get('/')
def home():
    return "Welcome to Online Book Library"


app.include_router(user.router)
app.include_router(auth.router)
app.include_router(book.router)
app.include_router(review.router)