from fastapi import APIRouter, status, Response, Request, Depends, HTTPException
from schema import BookSchema
from sqlalchemy.orm import Session
from model import get_db, Book, User

book = APIRouter()


@book.post('/add', status_code=status.HTTP_201_CREATED,tags=["Book"])
def add_book(body: BookSchema, response: Response, request: Request, db: Session = Depends(get_db)):
    """
        Description: This api is used to add the book
        Parameter: response : Response  it response to the user
                   db: Session = Depends on the get_db  i.e. he yield the database
                   request : Request send by the user
                   body: schema of the book
        Return: JSON form dict in that message, status code
    """
    try:
        user = db.query(User).filter_by(id=request.state.user.id).one_or_none()
        if user and not user.is_super_user:
            raise HTTPException(detail='Sorry You are Not a Super User', status_code=status.HTTP_400_BAD_REQUEST)

        data = body.model_dump()
        data.update({'user_id': request.state.user.id})
        book_data = Book(**data)
        db.add(book_data)
        db.commit()
        db.refresh(book_data)
        return {'message': 'Book added successfully', 'status': 201, 'data': book_data}
    except Exception as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}


@book.get('/get/{id}', status_code=status.HTTP_200_OK,tags=["Book"])
def get_book(id: int, response: Response, db: Session = Depends(get_db)):
    """
        Description: This api is used to get the book using book_id
        Parameter: response : Response  it response to the user
                   db: Session = Depends on the get_db  i.e. yield the database
                   request : Request used to getting all authenticated data
                   id : get the book id 
        Return: JSON form dict in that message, status code
    """
    try:
        book_data = db.query(Book).filter_by(id=id).one_or_none()
        if book_data is None:
            raise HTTPException(detail='This Book is not present', status_code=status.HTTP_400_BAD_REQUEST)
        return {'message': 'Book Found', 'data': book_data}
    except Exception as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}


@book.get('/get_all', status_code=status.HTTP_200_OK,tags=["Book"])
def get_all_books(request: Request, response: Response, db: Session = Depends(get_db)):
    """
        Description: This api is used to get the all books of the store 
        Parameter: response : Response  it response to the user
                   db: Session = Depends on the get_db  i.e. yield the database
                   request : Request used to getting all authenticated data
        Return: JSON form dict in that message, status code
    """
    try:
        books_data = db.query(Book).all()
        if books_data is None:
            raise HTTPException(detail='Super User Not Added any book', status_code=status.HTTP_400_BAD_REQUEST)

        return {'message': 'Books Found', 'status': 200, 'data': books_data}
    except Exception as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}

@book.put('/update/{id}',status_code=status.HTTP_200_OK,tags=["Book"])
def update_book(id:int,body:BookSchema,request:Request,response:Response,db:Session = Depends(get_db)):
    """
        Description: This api is used to update the book data using book_id
        Parameter: response : Response  it response to the user
                   db: Session = Depends on the get_db  i.e. yield the database
                   request : Request used to getting all authenticated data
                   id : get the book id 
        Return: JSON form dict in that message, status code
    """
    try:
        user_data = db.query(User).filter_by(id=request.state.user.id).one_or_none()
        if not user_data.is_super_user:
            raise HTTPException(detail="You are Not a Super user",status_code=status.HTTP_400_BAD_REQUEST)

        book_data = db.query(Book).filter_by(id=id).one_or_none()
        if book_data is None:
            raise HTTPException(detail="This book is Not Present",status_code=status.HTTP_400_BAD_REQUEST)
        [setattr(book_data,key,value) for key,value in body.model_dump().items()]
        db.commit()
        db.refresh(book_data)
        return {'message':'Book Updated Successfully','status':200}
    except Exception as ex:
        response.status_code=status.HTTP_400_BAD_REQUEST
        return {'message':str(ex),'status':400}

@book.delete('/del/{id}',status_code=status.HTTP_200_OK,tags=["Book"])
def delete_book(id:int,request:Request,response:Response,db:Session = Depends(get_db)):
    """
        Description: This api is used to delete the book using book_id
        Parameter: response : Response  it response to the user
                   db: Session = Depends on the get_db  i.e. yield the database
                   request : Request used to getting all authenticated data
                   id : get the book id 
        Return: JSON form dict in that message, status code
    """
    try:
        user_data = db.query(User).filter_by(id=request.state.user.id).one_or_none()
        if not user_data.is_super_user:
            raise HTTPException(detail="You are not a super user",status_code=status.HTTP_400_BAD_REQUEST)

        book_data = db.query(Book).filter_by(id=id).one_or_none()
        if not book_data:
            raise HTTPException(detail="This Book is not present ",status_code=status.HTTP_400_BAD_REQUEST)
        db.delete(book_data)
        db.commit()
        return {'message':'Book Deleted Successfully','status':200}
    except Exception as ex:
        response.status_code=status.HTTP_400_BAD_REQUEST
        return {'message':str(ex),'status':400}
