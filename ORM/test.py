import uvicorn
from pydantic import BaseModel
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body


def information() -> dict:
    all_posts = dict()
    all_posts[1] = Post(title='Первый пост',
                        content='Тестовый контент Тестовый контентТестовый контентТестовый контентТестовый контент'
                                'Тестовый контентТестовый контентмТестовый контентТестовый контентТестовый контентТестовый контент'
                                'Тестовый контентТестовый контентТестовый контентТестовый контентТестовый контентТестовый контент',
                        published=True)
    all_posts[2] = Post(title='Второй пост',
                        content='Тестовый контент Тестовый контентТестовый контентТестовый контентТестовый контент'
                                'Тестовый контентТестовый контентмТестовый контентТестовый контентТестовый контентТестовый контент'
                                'Тестовый контентТестовый контентТестовый контентТестовый контентТестовый контентТестовый контент',
                        published=True)
    all_posts[3] = Post(title='Третий пост',
                        content='Тестовый контент Тестовый контентТестовый контентТестовый контентТестовый контент'
                                'Тестовый контентТестовый контентмТестовый контентТестовый контентТестовый контентТестовый контент'
                                'Тестовый контентТестовый контентТестовый контентТестовый контентТестовый контентТестовый контент',
                        published=True,
                        rating=5)
    return all_posts    


app = FastAPI(debug=True)   


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


MEMORY_DB = information()


@app.get("/posts")
async def all_posts():
    return {'data': MEMORY_DB}


@app.get("/posts/first")
async def first_post():
    return {"data": MEMORY_DB[min(MEMORY_DB.keys())]}


@app.get("/posts/latest")
async def latest_post():
    return {'data': MEMORY_DB[max(MEMORY_DB.keys())]}


@app.get("/posts/{id}")
async def one_post(id: int, responce: Response):
    one_post = MEMORY_DB.get(id)
    if not one_post:
        # responce.status_code = 404
        # responce.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} doesnt exist!"}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} doesnt exist!"
        )
    return {'data': one_post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(newpost: Post):
    print(newpost)
    # print(newpost.dict())
    print(newpost.model_dump())
    MEMORY_DB[len(MEMORY_DB) + 1] = newpost.model_dump()
    return {'data': newpost}


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
async def full_update(id: int, post: Post):
    if not MEMORY_DB.get(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} doesnt exist!"
        )
    MEMORY_DB[id] = post.model_dump()
    return {'data': {'id': id, 'post': MEMORY_DB[id]}}


@app.patch("/posts/{id}", status_code=status.HTTP_200_OK)
async def update(id: int, post: dict = Body(...)):
    before = MEMORY_DB.get(id).model_copy()

    if post.get('title') and type(post.get('title')) == str:
        MEMORY_DB[id].title = post.get('title')
    if post.get('content') and type(post.get('content')) == str:
        MEMORY_DB[id].content = post.get('content')
    if post.get('published') and type(post.get('published')) == bool:
        MEMORY_DB[id].published = post.get('published')
    if post.get('rating') and type(post.get('rating')) == int:
        MEMORY_DB[id].rating = post.get('rating')

    return {
        "data": "post patched",
        "before": before,
        "after": MEMORY_DB[id]
    }


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int):
    if not MEMORY_DB.pop(id, None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} doesn't exist!"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
