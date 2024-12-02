from fastapi import APIRouter, Depends,HTTPException,Response,Request,Form
from fastapi.responses import JSONResponse
from app.utils.common import gen_token, Token
from app.utils.depends import DALGetter
from app.db.dao import UserDao
from app.config import Config
from app.db.schemas import UserIn
from app.routers.user_router import user_api

auth = APIRouter(prefix="/auth", tags=["Auth"])


@auth.post("/token")
async def get_token_api(*,
                    dao:UserDao=Depends(DALGetter(UserDao)),
                    form = Depends(UserIn.as_form),
                    request:Request
                    ):
    usercount = form.usercount
    password = form.password
    info = {"usercount": usercount, "password": password}
    try:
        await dao.get_and_valid_user_by_count(info)
        token = {
            "code": 0,
            "access_token": gen_token(info),
            "token_type": "Bearer",
            "expires_in": Config.TOKEN_EXPIRE
            }
        response = JSONResponse(content=token)
        # response.set_cookie("token",token,expires=Config.TOKEN_EXPIRE)
        return response

    except UserError as e:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer","message":e.__str__()},
        )
