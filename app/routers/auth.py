from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from .. import schemas, models, utils, oauth2
from sqlalchemy.orm import Session

router = APIRouter(tags=['Authentication'])

@router.post("/login", response_model=schemas.Token)
def login(user_crendentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user_crendentials.username).first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials!")
    
    if not utils.verify_password(user_crendentials.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials!")
    
    access_token = oauth2.create_access_token(data={"user_id": db_user.id})
    return {"access_token": access_token, "token_type": "bearer"}
