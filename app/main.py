from fastapi import FastAPI, Request, status
from fastapi.exception_handlers import (
    request_validation_exception_handler,
)
from starlette.responses import RedirectResponse
from fastapi.exceptions import RequestValidationError
from .db.database import SessionLocal, engine
from . import models
from .routers import todos, todos_form

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(todos.router)
app.include_router(todos_form.router)



template_urls = ['/add']

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    endpoint = str(request.url).replace(request.headers['origin'], '')
    if endpoint in template_urls:
        url = app.url_path_for("read_root") + '?error_create=true'
        return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
    # DEBUG :
    # return JSONResponse(
    #     status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    #     content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    # )
    return await request_validation_exception_handler(request, exc)


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}
