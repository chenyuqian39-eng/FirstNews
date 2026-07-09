from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

def success_response(message: str ="success", data = None):
    content = {"code":200,
               "message": message,
               "data": data}
# FastAPI ORM Pydantic 对象都要正常响应 ->code message data
    return JSONResponse(content = jsonable_encoder(content))
