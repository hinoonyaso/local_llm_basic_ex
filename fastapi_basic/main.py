from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

# FastAPI 객채 생성
api = FastAPI()


# DTO : 데이터 전송 객체
class UserCreate(BaseModel):
    username: str
    password: str
    user_full_name: Optional[str] = None
    avatar_url: Optional[HttpUrl] = None


# http://localhost:8000/ 접속 시 Hello World! 출력
# http://127.0.0.1:8000/
@api.get("/")
async def read_root():
    # 비즈니스 로직
    data = "db에서 데이터 읽어오기"
    return {"message": data}


# http://127.0.0.1:8000/items
@api.get("/items")
def read_item():
    item_id = 1
    q = "사과"
    return {"item_id": item_id, "q": q}


# http://127.0.0.1:8000/items/5?q=싫어 # 8000 = tcp 포트
@api.get("/items/{item_id}")
def read_item_by_id(item_id: int, q: str | None = None):
    # 비즈니스 로직 처리
    print(f"item_id: {item_id}, q: {q}")
    return {"item_id": item_id, "q": q}


@api.post("/user_info/")
def create_user(user: UserCreate):
    # 비즈니스 로직 처리
    print(f"user_full_name: {user.user_full_name}")
    print(f"avatar_url: {user.avatar_url}")
    print(f"username: {user.username}, password: {user.password}")

    return user
    #return {"user": user}

@api.post("/user_info/{user_id}")
def create_user_by_id(user_id: int, q: str | None = None):
    # 비즈니스 로직 처리
    print(f"user_id: {user_id}, q: {q}")
    return {"user_id": user_id, "q": q}
