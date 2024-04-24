import uvicorn
from fastapi import FastAPI, Response, status, HTTPException, Depends

from sqlalchemy.orm import Session

from .database import engine, get_db
from . import models, shemas

models.Base.metadata.create_all(bind=engine)
app = FastAPI(debug=True)

@app.get("/posts")
async def all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post)
    return {"data": posts}

@app.get("/posts/{id}")
async def one_post(id: int, db:Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id = {id} does not exists!"
        )
    return {"data": post}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_post(post:shemas.PostBase, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"message":"post created", "data":new_post}

if __name__ == '__main__':
    uvicorn.run(app)

