from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Todo(BaseModel):
    title: str
    completed: bool = False


todos = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "completed": False
    },
    {
        "id": 2,
        "title": "Learn MySQL",
        "completed": False
    },
    {
        "id": 3,
        "title": "Build a project",
        "completed": True
    }
]


@app.get("/todos")
def get_todos():
    return todos


@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo

    return {"message": "Todo not found"}


@app.post("/todos")
def create_todo(todo: Todo):
    new_todo = {
        "id": len(todos) + 1,
        "title": todo.title,
        "completed": todo.completed
    }

    todos.append(new_todo)

    return new_todo

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: Todo):
    for item in todos:
        if item["id"] == todo_id:
            item["title"] = todo.title
            item["completed"] = todo.completed
            return item

    return {"message": "Todo not found"}