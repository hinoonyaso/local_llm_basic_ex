from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
import uvicorn # fastapi 내장 웹서버

# FastAPI 객채 생성
app = FastAPI()


# DTO : 데이터 전송 객체
class UserCreate(BaseModel):
    username: str
    password: str
    user_full_name: Optional[str] = None
    avatar_url: Optional[HttpUrl] = None


# DTO : 응답 전송 객체
class UserResponse(BaseModel):
    username: str
    avatar_url: Optional[HttpUrl] = None

# http://localhost:8000/ 접속 시 Hello World! 출력
# http://127.0.0.1:8000/
@app.get("/")
async def read_root():
    # 비즈니스 로직
    data = "db에서 데이터 읽어오기"
    return {"message": data}


# http://127.0.0.1:8000/items
@app.get("/items")
def read_item():
    item_id = 1
    q = "사과"
    return {"item_id": item_id, "q": q}


# http://127.0.0.1:8000/items/5?q=싫어 # 8000 = tcp 포트
@app.get("/items/{item_id}")
def read_item_by_id(item_id: int, q: str | None = None):
    # 비즈니스 로직 처리
    print(f"item_id: {item_id}, q: {q}")
    return {"item_id": item_id, "q": q}


@app.post("/user_info/",response_model=UserResponse)
def create_user(user: UserCreate):
    # 비즈니스 로직 처리
    print(f"user_full_name: {user.user_full_name}")
    print(f"avatar_url: {user.avatar_url}")
    print(f"username: {user.username}, password: {user.password}")

    user_info = UserResponse(
        username = user.username,
        avatar_url = user.avatar_url
    )
    return user_info
    #return {"user": user}

@app.post("/user_info/{user_id}")
def create_user_by_id(user_id: int, q: str | None = None):
    # 비즈니스 로직 처리
    print(f"user_id: {user_id}, q: {q}")
    return {"user_id": user_id, "q": q}

# uv run fastapi dev
# uv run main.py
if __name__ == "__main__":
    # uvicorn.run("현재 파일이름:fastapi 객체식별자", reload=True : 코드 변경시 자동 재시작)
    uvicorn.run("main:app", reload=True)