from fastapi import APIRouter, Depends, Request, Form, status, HTTPException
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from ..schema import Todo
from ..db.database import get_db
from .. import crud
from starlette.templating import Jinja2Templates
templates = Jinja2Templates(directory="app/templates")


router = APIRouter(
    prefix="",
    tags=["todos_form"],
    dependencies=[],
)

@router.get("/")
async def read_root(request: Request, error_create: bool = False, db: Session = Depends(get_db)):
    todos = crud.get_todos(db)
    return templates.TemplateResponse("base.html",
                                    {"request": request, "todo_list": todos, "error_create": error_create})


@router.post("/add")
async def add(request: Request, title: str = Form(...), db: Session = Depends(get_db)):
    todo = Todo(title=title, complete=False)
    crud.create_todo(db, todo)
    url = router.url_path_for("read_root")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@router.get("/update/{id}")
async def update(request: Request, id: int, db: Session = Depends(get_db)):
    todo = crud.get_todos(db, id)
    if todo:
        crud.update_complete_todo(db, id)
        url = router.url_path_for("read_root")
        return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)
    else:
        raise HTTPException(404, crud.error_message('No todo found for id {}'.format(id)))


@router.get("/delete/{id}")
async def delete(request: Request, id: int, db: Session = Depends(get_db)):
    todo = crud.get_todos(db, id)
    if todo:
        crud.delete_todo(db, id)
        url = router.url_path_for("read_root")
        return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)
    else:
        raise HTTPException(404, crud.error_message('No todo found for id {}'.format(id)))


