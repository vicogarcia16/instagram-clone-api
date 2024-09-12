from schemas.schemas import PostBase
from sqlalchemy.orm.session import Session
from db.models import DbPost, DbComment
from datetime import datetime
from fastapi import HTTPException, status
from tools.bucket import supabase, SUPABASE_BUCKET_NAME, SUPABASE_URL

def create(db: Session, request: PostBase):
    new_post = DbPost(
        image_url=request.image_url, 
        image_url_type=request.image_url_type, 
        caption=request.caption,
        timestamp=datetime.now(),
        user_id=request.creator_id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def get_all_posts(db: Session):
    return db.query(DbPost).all()

def delete(db: Session, id: int, user_id: int):
    post = db.query(DbPost).filter(DbPost.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} not found")
    if post.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Only post creator can delete the post")
    image = post.image_url
    if image:
        image_filename = image.split('/')[-1]
        try:
            response = supabase.storage.from_(SUPABASE_BUCKET_NAME).remove([image_filename])
            if hasattr(response, 'error') and response.error:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Supabase error: {response.error}")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=str(e))
            
    comments = db.query(DbComment).filter(DbComment.post_id == id).all()
    for comment in comments:
        db.delete(comment)
        
    db.delete(post)
    db.commit()
    return 'Deleted'
   