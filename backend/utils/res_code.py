from fastapi.responses import JSONResponse
from pydantic import BaseModel


class PdsfException(Exception):
    ...


def code_and_msg(code: int, msg: str):

    def wrapper(cls):
        setattr(cls, 'code', code)
        setattr(cls, 'msg', msg)
        return cls
    return wrapper


def response_builder(data: BaseModel | PdsfException ) -> JSONResponse:
    if isinstance(data, BaseModel):
        return JSONResponse(
            content={
                "code": 0,
                "msg": "",
                "data": data.model_dump(),
            }
        )
    elif isinstance(data, PdsfException):
        return JSONResponse(
            content={
                "code": data.code,
                "msg": data.msg,
                "data": [],
            }
        )

    else:
        raise RuntimeError()