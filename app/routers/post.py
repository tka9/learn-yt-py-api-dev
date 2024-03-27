from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional

router = APIRouter(prefix="/posts", tags=['Posts'])

@router.get("/", response_model=list[schemas.PostOut])
# @router.get("/")
async def get_posts(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user), limit: int = 10, offset: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    if search:
        # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(offset).all()
        posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(offset).all()
    else:
        posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).limit(limit).offset(offset).all()
        # posts = db.query(models.Post).limit(limit).offset(offset).all()
    # posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    # print(posts)
    return posts
    

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.model_dump(), owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    print(current_user.email)
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found!")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post2delete = deleted_post_query.first()

    if post2delete == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found!")
    
    if post2delete.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested operation!")
    
    deleted_post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    db_post = post_query.first()

    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found!")
    
    if db_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested operation!")
    

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    return {"data": 'successful'}