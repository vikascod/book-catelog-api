from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models, database
from app.oauth2 import get_current_user
from typing import List

router = APIRouter(
    prefix='/book',
    tags=["Books"]
)

@router.post('/add', status_code=status.HTTP_201_CREATED)
async def add_book(book:schemas.BookCreate, db:Session=Depends(database.get_db), current_user:int=Depends(get_current_user)):
    new_book = models.Book(user_id=current_user.id, **book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@router.get('/', response_model=List[schemas.Book])
async def show_all_book(db:Session=Depends(database.get_db)):
    books = db.query(models.Book).all()
    return books


@router.get('/author/{author}')
async def show(author:str, db:Session=Depends(database.get_db)):
    books = db.query(models.Book).filter(models.Book.author.like(f'%{author}%')).all()
    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No books found for author: {author}")
    return books



@router.get('/genre/{genre}')
async def show(genre:str, db:Session=Depends(database.get_db)):
    book = db.query(models.Book).filter(models.Book.genre.like(f'%{genre}%')).all()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{genre} not found")
    return book


@router.get('/book-title/{title}')
async def show(title:str, db:Session=Depends(database.get_db)):
    book = db.query(models.Book).filter(models.Book.title.like(f'%{title}%')).all()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{title} not found")
    return book


@router.put('/edit/{book_id}')
async def update_book(book_id:int, request:schemas.BookUpdate, db:Session=Depends(database.get_db), current_user:int=Depends(get_current_user)):
    edit_book = db.query(models.Book).filter(models.Book.id==book_id)
    book = edit_book.first()

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book not found {book_id}")

    if book.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform action")

    edit_book.update(request.dict())
    db.commit()
    return edit_book.first()


@router.delete('/delete/{book_id}')
async def destroy(book_id:int, db:Session=Depends(database.get_db), current_user:int=Depends(get_current_user)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book not found {book_id}")
    
    if book.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform action")
    db.delete(book)
    db.commit()
    return "Deleted"