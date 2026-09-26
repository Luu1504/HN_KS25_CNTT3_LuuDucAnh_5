from fastapi import FastAPI, Depends, Response
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/", response_model=schemas.APIResponse)
def root():
    return {
        "statusCode": 200,
        "error": None,
        "message": "API đang chạy",
        "data": None
    }


@app.get("/books", response_model=schemas.APIResponse)
def get_books(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    books_data = [schemas.BookResponse.model_validate(b) for b in books]
    return {
        "statusCode": 200,
        "error": None,
        "message": "Lấy danh sách sách thành công",
        "data": books_data
    }





@app.get("/books/{book_id}", response_model=schemas.APIResponse)
def get_book(book_id: int, response: Response, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        response.status_code = 404
        return {
            "statusCode": 404,
            "error": "Not Found",
            "message": "Không tìm thấy sách",
            "data": None
        }
    return {
        "statusCode": 200,
        "error": None,
        "message": "Lấy chi tiết sách thành công",
        "data": schemas.BookResponse.model_validate(book)
    }


@app.post("/books", response_model=schemas.APIResponse, status_code=201)
def create_book(book: schemas.BookCreate, response: Response, db: Session = Depends(get_db)):
    new_book = models.Book(
        title=book.title,
        author=book.author,
        category=book.category,
        quantity=book.quantity
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    response.status_code = 201
    return {
        "statusCode": 201,
        "error": None,
        "message": "Thêm sách thành công",
        "data": schemas.BookResponse.model_validate(new_book)
    }


@app.put("/books/{book_id}", response_model=schemas.APIResponse)
def update_book(book_id: int, book_data: schemas.BookCreate, response: Response, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        response.status_code = 404
        return {
            "statusCode": 404,
            "error": "Not Found",
            "message": "Không tìm thấy sách",
            "data": None
        }

    book.title = book_data.title
    book.author = book_data.author
    book.category = book_data.category
    book.quantity = book_data.quantity

    db.commit()
    db.refresh(book)

    return {
        "statusCode": 200,
        "error": None,
        "message": "Cập nhật sách thành công",
        "data": schemas.BookResponse.model_validate(book)
    }


@app.delete("/books/{book_id}", response_model=schemas.APIResponse)
def delete_book(book_id: int, response: Response, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        response.status_code = 404
        return {
            "statusCode": 404,
            "error": "Not Found",
            "message": "Không tìm thấy sách",
            "data": None
        }

    db.delete(book)
    db.commit()

    return {
        "statusCode": 200,
        "error": None,
        "message": "Xóa sách thành công",
        "data": None
    }