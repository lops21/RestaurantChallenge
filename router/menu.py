from fastapi import status,HTTPException, Depends,APIRouter
import schemas
import models
import token_2
from database import SessionLocal
from typing import List
from hashing import Hash
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import hashing,oauth2
from datetime import datetime,date

router = APIRouter()
db = SessionLocal()

#Creating Restaurant
@router.post('/menu/restaurant',response_model=schemas.Restaurant,status_code=status.HTTP_201_CREATED)
def create_resto(restaurant:schemas.Restaurant,curent_user: schemas.User = Depends(oauth2.current_user)):
    # existing_resto = db.query(models.Restaurant).filter(models.Restaurant.name == restaurant.name).filter(models.Restaurant.place == restaurant.place)
    # if existing_resto.first():
    #     return "Resturant is already existing"

    try:
        new_resto = models.Restaurant(
            name=restaurant.name,
            place=restaurant.place)
    
        db.add(new_resto)
        db.commit()
        return new_resto
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail="Restaurant is already exists",)

#Creating Users
@router.post('/menu/user',response_model=schemas.User,status_code=status.HTTP_201_CREATED)
def create_user(user:schemas.User,curent_user: schemas.User = Depends(oauth2.current_user)):
    try:
        new_user = models.Users(

            name = user.name,
            email = user.email,
            password =Hash.bcrypt(user.password),
            position = user.position
        )
        db.add(new_user)
        db.commit()
        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail="User is already exists",)
#creating menu
@router.post('/menu/menus')
def create_menu(menus:schemas.Menus,curent_user: schemas.User = Depends(oauth2.current_user)):

    datetoday = date.today()
    menu_today = db.query(models.Menus).filter(models.Menus.resto_id == menus.resto_id).filter( models.Menus.date == datetoday)
    if menu_today.first():
        return 'You already place menu for today'
   
    new_menu = models.Menus(
        menu_item = menus.menu_item,
        price = menus.price,
        date = menus.date,
        resto_id = menus.resto_id
    )
    db.add(new_menu)
    db.commit()
    return 'Succesfully Created Menu'


#Creating entry for voting
@router.post('/menu/vote')
def entry_voting(votes:schemas.Voting,curent_user: schemas.User = Depends(oauth2.current_user)):

    new_vote = models.VotingNew(
        vote = votes.vote,
        date = votes.date,
        menu_id = votes.menu_id,
        user_id = votes.user_id

    )

    verify_menu = db.query(models.Menus).filter(models.Menus.id == votes.menu_id).filter(models.Menus.date == votes.date)
    if verify_menu.first():
        return 'There is no menu of that today'


    verify_entry = db.query(models.VotingNew).filter(models.VotingNew.menu_id == votes.menu_id).filter(models.VotingNew.date == votes.date)
    if verify_entry.first():
        return 'Entry for that menu is already existing for today'

    db.add(new_vote)
    db.commit()
    return 'Successfully Insert Entry for Voting'

#voting
@router.put('/vote/now')
def vote_now(votes:schemas.Voting,curent_user: schemas.User = Depends(oauth2.current_user)):

    duplicate_vote = db.query(models.VotingNew).filter(models.VotingNew.user_id == votes.user_id).filter(
        models.VotingNew.date == date.today()).first()
    if duplicate_vote:
        return "You already voted"

    existing_vote = db.query(models.VotingNew).filter(models.VotingNew.menu_id == votes.menu_id).first()
    existing_vote.vote+=1
    db.commit()
    return 'Succesfully Voted'
   



#get meal to day
@router.get('/meal/today')
def get_meal_today():
    highest_vote = db.query(models.VotingNew).filter(models.VotingNew.date == date.today()).order_by(models.VotingNew.vote.desc()).first()
    meal_today = db.query(models.Menus).filter(models.Menus.id == highest_vote.menu_id).first()
    return meal_today


#get all resto
@router.get('/menu/restaurant/all',response_model=List[schemas.Restaurant],status_code=200)
def get_all_resto(curent_user: schemas.User = Depends(oauth2.current_user)):
    all_resto = db.query(models.Restaurant).all()

    return all_resto

#get all user
@router.get('/menu/user/all',response_model=List[schemas.User],status_code=200)
def get_all_resto(curent_user: schemas.User = Depends(oauth2.current_user)):
    all_users = db.query(models.Users).all()

    return all_users

#get all menu today
@router.get('/menu/menus/all',response_model=List[schemas.Menus],status_code=200)
def get_all_menu_today(curent_user: schemas.User = Depends(oauth2.current_user)):
    all_menu = db.query(models.Menus).filter(models.Menus.date == date.today()).all()

    return all_menu

#getll all votes today
@router.get('/menu/vote/today',response_model=List[schemas.Voting],status_code=200)
def get_all_votes(curent_user: schemas.User = Depends(oauth2.current_user)):
    all_votes = db.query(models.VotingNew).filter(models.VotingNew.date == date.today()).all()
    return all_votes



