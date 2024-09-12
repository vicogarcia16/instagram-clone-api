from fastapi import APIRouter, Depends, status, File, UploadFile
from sqlalchemy.orm.session import Session
from db import db_post
from db.database import get_db
from fastapi.exceptions import HTTPException
from schemas.schemas import PostBase, PostDisplay, UserAuth
from typing import List
import string, random
from auth.oauth2 import get_current_user
from tools.bucket import supabase, SUPABASE_BUCKET_NAME, SUPABASE_URL

router = APIRouter(
    prefix="/post",
    tags=["post"],
    responses={404: {"description": "Not found"}}
    )

image_url_types = ['absolute', 'relative']

@router.post("/", response_model=PostDisplay)
def create(request: PostBase, db: Session = Depends(get_db), 
           current_user: UserAuth = Depends(get_current_user)):
    if not request.image_url_type in image_url_types:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Parameter image_url_type can only be 'absolute' or 'relative'")
    return db_post.create(db, request)

@router.get("/all/", response_model=List[PostDisplay])
def posts(db: Session = Depends(get_db)):
    return db_post.get_all_posts(db)

@router.post("/image/")
async def upload_image(image: UploadFile = File(...), 
                 current_user: UserAuth = Depends(get_current_user)):
    letters = string.ascii_letters
    rand_str = ''.join(random.choice(letters) for i in range(6))
    new = f"_{rand_str}."
    filename = new.join(image.filename.rsplit('.', 1))
    file_content = await image.read()

    try:
        response = supabase.storage.from_(SUPABASE_BUCKET_NAME).upload(filename, file_content)
        if hasattr(response, 'error') and response.error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Supabase error: {response.error}")

        # Devuelve la URL pública del archivo
        url = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET_NAME}/{filename}"
        return {"filename": url}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(e))

@router.delete("/delete/{id}/")
def delete(id: int, db: Session = Depends(get_db), 
            current_user: UserAuth = Depends(get_current_user)):
    return db_post.delete(db, id, current_user.id)
