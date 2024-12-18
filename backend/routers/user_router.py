from fastapi import APIRouter, Depends, Header
from typing import List

from db.schemas.user_schema import UserLogin, UserBase, UserCrate
from db.dao.user_dao import UserDao
from utils.depends import DALGetter, LoggedIn, NeedAdmin

user_api = APIRouter(prefix="/user",tags=["User"])


@user_api.post("/login")
async def login(
    user: UserLogin,
    user_dao: UserDao = Depends(DALGetter(UserDao))
):
    return await user_dao.login(user)


@user_api.post("/register")
async def register(
    user: UserCrate,
    user_dao: UserDao = Depends(DALGetter(UserDao))
):
    await user_dao.register(user)
    return user.email


@user_api.get("/current_user", dependencies=[Depends(LoggedIn)])
async def current_user_info(
    current_user: UserBase = Depends(LoggedIn)
):
    return current_user.model_dump_json()


@user_api.get("/select_all", dependencies=[Depends(NeedAdmin)])
async def select_all_user(
    user_dao: UserDao = Depends(DALGetter(UserDao))
):
    return await user_dao.select_all()


@user_api.post("/update_user", dependencies=[Depends(NeedAdmin)])
async def update_user(
    user: UserBase,
    user_dao: UserDao = Depends(DALGetter(UserDao)),
):
    return await user_dao.update_user(user)


@user_api.post("/update_self", dependencies=[Depends(LoggedIn)])
async def update_self(
    user: UserBase,
    current_user: UserBase = Depends(LoggedIn),
    user_dao: UserDao = Depends(DALGetter(UserDao)),
):
    return await user_dao.update_self(current_user, user)


# @user_api.get("/test_login", dependencies=[Depends(LoggedIn)])
# async def test_login(
#     current_user: UserBase = Depends(LoggedIn)
# ):
#     print(current_user.model_dump_json())
#     return "ok"


# @user_api.get("/test_admin", dependencies=[Depends(NeedAdmin)])
# async def test_admin(
#     current_user: UserBase = Depends(NeedAdmin)
# ):
#     print(current_user.model_dump_json())
#     return "ok"

# @user_api.get("/master_test",dependencies=[Depends(master)])
# async def mastertest():
#     return "ok"

# @user_api.get("/cookie_test")
# async def mastertest(cookie =Depends(get_cookie)):
#     return cookie


# @user_api.post("/add",response_model=UserOut)
# async def create_user_api(
#         *,
#         dao=Depends(DALGetter(UserDao)),
#         user:UserIn
# ):
#     try:
#         async with async_session().begin() as ss:
#             db_user = await dao.insert(user)
#             return UserOut(status=Code.SUCCESS,data=db_user)
#     except UserError as e:
#         return UserOut(status=Code.INSERT_ERROR,msg=e.__str__())


# @user_api.get("/add")
# async def create_user_web(request:Request):
#     return template.TemplateResponse("user/create_user.html",{"request":request})


# @user_api.api_route("/userinfo",methods=["POST","GET"])
# async def get_user_info(*,user=Depends(login),request:Request):

#     return template.TemplateResponse("user/user_info.html",{"request":request,"user":UserBase(**user.__dict__)})
