from fastapi.responses import JSONResponse

def code_and_msg(code: int, msg: str):

    def wrapper(cls):
        setattr(cls, 'code', code)
        setattr(cls, 'msg', msg)
        return cls
    return wrapper


@code_and_msg("101", "MyException")
class MyException(Exception):
    ...

if __name__ == "__main__":

    try:
        raise MyException()
    except Exception as e:
        print(e.code, e.msg)