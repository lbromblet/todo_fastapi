from fastapi import APIRouter, Depends, Request, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..schema import Todo, TodoUpdate
from ..db.database import get_db
from .. import crud

router = APIRouter(
    prefix="/api/todos",
    tags=["todos"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

@router.get("/api")
async def api_get_list(request: Request, db: Session = Depends(get_db)):
    return crud.get_todos(db)


@router.get("/api/{id}")
async def api_get(request: Request, id: int, db: Session = Depends(get_db)):
    todo = crud.get_todos(db, id)
    if todo:
        return todo
    else:
        raise HTTPException(404, crud.error_message('No todo found for id {}'.format(id)))


@router.post("/api/add")
async def api_create(request: Request, todo: Todo, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo)


@router.put("/api/{id}")
async def api_update(request: Request, id: int, new_todo: Todo, db: Session = Depends(get_db)):
    todo = crud.get_todos(db, id)
    if todo:
        return crud.update_todo(db, id, new_todo)
    else:
        raise HTTPException(404, crud.error_message('No todo found for id {}'.format(id)))


@router.patch("/api/{id}")
async def api_patch(request: Request, id: int, new_todo: TodoUpdate, db: Session = Depends(get_db)):
    todo = crud.get_todos(db, id)
    if todo:
        return crud.patch_todo(db, id, new_todo)
    else:
        raise HTTPException(404, crud.error_message('No todo found for id {}'.format(id)))



@router.delete("/api/{id}")
async def api_delete(request: Request, id: int, db: Session = Depends(get_db)):
    todo = crud.get_todos(db, id)
    if todo:
        crud.delete_todo(db, id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(404, crud.error_message('No todo found for id {}'.format(id)))

