from fastapi import APIRouter

router = APIRouter(prefix="/todos")

@router.get("/{todo_id}")
def get_todos(todo_id : int):
    return [
        {"message": "Get all todos"},
        {"todo_id":todo_id}
        ]

@router.post("")
def create_todo():
    return {"message": "Create todo"}
