from fastapi import Depends, Request
from fastapi.exceptions import HTTPException

from db import async_session
from utils.common import parse_token
from db.schemas.user_schema import UserBase


class DALGetter:
    def __init__(self, dal_cls):
        self.dal_cls = dal_cls

    async def __call__(self):
        async with async_session() as session:
            async with session.begin():
                yield self.dal_cls(session)


async def LoggedIn(
    request: Request
) -> UserBase:
    token = request.headers.get("token")
    if request.headers.get("token") is None:
        raise HTTPException(401, "login in first")
    user = UserBase(**parse_token(token))
    return user


async def NeedAdmin(
    request: Request
):
    user: UserBase = await LoggedIn(request)
    if not user.admin:
        raise HTTPException(403, "you are not admin user")
    return user


# async def login(token=Depends(auth_tool),dao: UserDao = Depends(DALGetter(UserDao))):
#
#     try:
#         info = parse_token(token)
#         db_user = await dao.get_and_valid_user_by_count(info)
#         return db_user
#     except (UserError,JWTError) as e:
#         raise HTTPException(
#             status_code=401,
#             detail="Not authenticated",
#             headers={"WWW-Authenticate": "Bearer", "message": e.__str__()},
#         )
#
#
# async def master(db_user=Depends(login),dao: UserDao = Depends(DALGetter(UserDao))):
#     try:
#         db_user = await dao.is_master(db_user)
#         return db_user
#     except UserError as e:
#         raise HTTPException(
#             status_code=403,
#             headers={"WWW-Authenticate": "Bearer","message":e.__str__()},
#         )


# def cookie_format(cookie:str):
#     try:
#         dict_cookie = {}
#         for item in cookie.split(";"):
#             key,values = [i.strip() for i in item.split("=")]
#             dict_cookie[key] = values
#         # print(dict_cookie)
#         return dict_cookie
#     except:
#         raise HTTPException(
#             status_code=401,
#             detail="Not authenticated",
#             headers={"WWW-Authenticate": "Bearer", "message": "cookie error"},
#         )


# async def get_cookie(request:Request):
#     cookie = request.headers.get("cookie")
#     if not cookie:
#         raise HTTPException(
#             status_code=401,
#             detail="Not authenticated",
#             headers={"WWW-Authenticate": "Bearer", "message": "have not login yet!"},
#         )
#     format_cookie = cookie_format(cookie)
#     token = format_cookie.get("token")
#     if token is None:
#         raise HTTPException(
#             status_code=401,
#             detail="Not authenticated",
#             headers={"WWW-Authenticate": "Bearer", "message": "have not login yet!"},
#         )
#     return token


# async def login(token=Depends(get_cookie), dao:UserDao=Depends(DALGetter(UserDao))):
#     try:
#             info = parse_token(token)
#             db_user = await dao.get_and_valid_user_by_count(info)
#             return db_user
#     except (UserError,JWTError) as e:
#         raise HTTPException(
#             status_code=401,
#             detail="Not authenticated",
#             headers={"WWW-Authenticate": "Bearer", "message": e.__str__()},
#         )


# async def master(db_user=Depends(login),dao: UserDao = Depends(DALGetter(UserDao))):
#     try:
#         db_user = await dao.is_master(db_user)
#         return db_user
#     except UserError as e:
#         raise HTTPException(
#             status_code=403,
#             headers={"WWW-Authenticate": "Bearer","message":e.__str__()},
#         )


