from fastapi import APIRouter, Depends, HTTPException, status
import models
import token_2
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import SessionLocal
from hashing import Hash

router = APIRouter()
db = SessionLocal()


#login
@router.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends()):
    user = db.query(models.Users).filter(models.Users.email ==  request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Username is not existing')
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Password is incorrect')
    

    access_token = token_2.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}