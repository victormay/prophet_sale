from fastapi import APIRouter,Depends,Form,Request
from app.utils.depends import DALGetter
from app.db.schemas import UserIn,UserOut,UserBase
from app.db.dao import UserDao,UserError
from app.utils import Code
from app.db import sm
from app.extensions import template
from app.utils.depends import login,master,get_cookie

user_api = APIRouter(prefix="/user",tags=["User"])


@user_api.get("/login_test",dependencies=[Depends(login)])
async def logintest():
    return "ok"


@user_api.get("/master_test",dependencies=[Depends(master)])
async def mastertest():
    return "ok"

@user_api.get("/cookie_test")
async def mastertest(cookie =Depends(get_cookie)):
    return cookie


@user_api.post("/add",response_model=UserOut)
async def create_user_api(
        *,
        dao=Depends(DALGetter(UserDao)),
        user:UserIn
):
    try:
        async with sm().begin() as ss:
            db_user = await dao.insert(user)
            return UserOut(status=Code.SUCCESS,data=db_user)
    except UserError as e:
        return UserOut(status=Code.INSERT_ERROR,msg=e.__str__())


@user_api.get("/add")
async def create_user_web(request:Request):
    return template.TemplateResponse("user/create_user.html",{"request":request})


@user_api.api_route("/userinfo",methods=["POST","GET"])
async def get_user_info(*,user=Depends(login),request:Request):

    return template.TemplateResponse("user/user_info.html",{"request":request,"user":UserBase(**user.__dict__)})
