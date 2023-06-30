from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import get_db
from werkzeug.security import generate_password_hash
from app.oauth2 import get_current_user


router = APIRouter(
    prefix='/user',
    tags=['Users']
)

@router.post('/create-account/')
async def create_user(user:schemas.UserCreate, db:Session=Depends(get_db)):
    hashed_password = generate_password_hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{user_id}')
async def show_user(user_id:int, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user found {user_id}")
    return user


@router.get('/')
async def get_user(db:Session=Depends(get_db), current_user:int=Depends(get_current_user)):
    users = db.query(models.User).all()
    return users