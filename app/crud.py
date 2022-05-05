from sqlalchemy.orm import Session
from . import schema, models


def get_todos(db: Session, id: int = None):
    if id is None:
        return db.query(models.Todo).all()
    else:
        return db.query(models.Todo).filter(models.Todo.id == id).first()


def create_todo(db: Session, todo: schema.Todo):
    new_todo = models.Todo(**todo.dict())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


def update_todo(db: Session, id: int, new_todo: schema.Todo):
    todo = db.query(models.Todo).filter(models.Todo.id == id).first()
    todo.title = new_todo.title
    todo.complete = new_todo.complete
    db.commit()
    return todo


def update_complete_todo(db: Session, id: int):
    todo = db.query(models.Todo).filter(models.Todo.id == id).first()
    todo.complete = not todo.complete
    db.commit()
    return todo


def delete_todo(db: Session, id: int):
    todo = db.query(models.Todo).filter(models.Todo.id == id).first()
    db.delete(todo)
    db.commit()


def patch_todo(db: Session, id: int, todo: schema.TodoUpdate):
    db_todo = db.get(models.Todo, id)
    todo_data = todo.dict(exclude_unset=True)
    for key, value in todo_data.items():
        setattr(db_todo, key, value)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo



def error_message(message):
    return {
        'error': message
    }