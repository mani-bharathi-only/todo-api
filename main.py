from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class Todo(BaseModel):
    title: str
    completed: bool = False

class Todo_response(BaseModel):
    id : int 
    title : str
    completed : bool


todos = [
    {
        "id": 1,
        "title": "fastapi",
        "completed": False
    },
    {
        "id": 2,
        "title": "mysql",
        "completed": False
    },
    {
        "id": 3,
        "title": "project",
        "completed": True
    }
]

next_id =4

@app.get("/todos", response_model=list[Todo_response])
def get_todos(
    completed: bool | None = None,
    limit: int = Query(10,gt=1,lt=100) ):
    results = todos

    if completed is not None:
        results = [
            todo for todo in results
            if todo["completed"] == completed
        ]

    return results[:limit]


@app.get("/todos/{todo_id}", response_model=Todo_response)
def get_todo(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo not found"
    )

@app.post(
    "/todos",
    response_model=Todo_response,
    status_code=status.HTTP_201_CREATED
)
def create_todo(todo: Todo):
    global next_id

    new_todo = {
        "id": next_id,
        "title": todo.title,
        "completed": todo.completed
    }

    todos.append(new_todo)
    next_id += 1

    return new_todo


@app.put("/todos/{todo_id}",response_model=list[Todo_response])
def update_todo(todo_id: int, todo: Todo):
    for item in todos:
        if item["id"] == todo_id:
            item["title"] = todo.title
            item["completed"] = todo.completed

            return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Tod not found"
    )

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id : int):
    for todo in todos:
        if todo["id"] == todo_id:
            todos.remove(todo)
            return {"message" : "todo deleted"}

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

# Query Parameters


@app.get("/todos/search")
def search_todos(title: Optional[str] = None):
    if title is None:
        return todos

    results = []

    for todo in todos:
        if title.lower() in todo["title"].lower():
            results.append(todo)

    return results
