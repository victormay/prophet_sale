from fastapi import APIRouter, Depends, Header

from db.schemas.user_schema import UserLogin, UserBase
from db.dao.user_dao import UserDao
from utils.depends import DALGetter, LoggedIn, NeedAdmin

user_api = APIRouter(prefix="/user",tags=["User"])


@user_api.post("/login")
async def login(
    user: UserLogin,
    user_dao: UserDao = Depends(DALGetter(UserDao))
):
    return await user_dao.login(user)


@user_api.get("/test_login", dependencies=[Depends(LoggedIn)])
async def test_login(
    current_user: UserBase = Depends(LoggedIn)
):
    print(current_user.model_dump_json())
    return "ok"


@user_api.get("/test_admin", dependencies=[Depends(NeedAdmin)])
async def test_admin(
    current_user: UserBase = Depends(NeedAdmin)
):
    print(current_user.model_dump_json())
    return "ok"

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
