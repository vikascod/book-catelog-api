from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models, database
from app.oauth2 import get_current_user
from typing import List

router = APIRouter(
    prefix='/review',
    tags=["Reviews"]
)

@router.post('/rate/{book_id}', status_code=status.HTTP_201_CREATED)
async def create_review_for_book(book_id:int, review:schemas.ReviewCreate, db:Session=Depends(database.get_db), current_user: models.User = Depends(get_current_user)):

    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail=f"Book not found {book_id}")

    existing_user = db.query(models.Review).filter(models.Review.user_id==current_user.id, models.Review.book_id==book_id).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already rated this book")

    review = models.Review(**review.dict(), book_id=book_id, user_id=current_user.id)
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@router.get('/{book_id}', response_model=List[schemas.Review])
async def read_reviews_for_book(book_id: int, db: Session = Depends(database.get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book.reviews
