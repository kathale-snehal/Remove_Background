
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel

# app = FastAPI()

# class Task(BaseModel):
#     title: str
#     description: str = ""

# tasks = []

# @app.get("/tasks")
# def read_task():
#     if not tasks:
#         return {"message": "no task here"}
#     return tasks

# @app.post("/tasks")
# def add_task(task: Task):
#     tasks.append(task)
#     return {"message": "task added"}

# @app.get("/tasks/{task_id}", response_model=Task)
# def get_task_from_id(task_id: int):
#     if 0 <= task_id < len(tasks):
#         return tasks[task_id]
#     raise HTTPException(status_code=404, detail="task not found")

# @app.put("/tasks/{task_id}", response_model=Task)
# def update_task_from_id(task_id: int, updated_task: Task):
#     if 0 <= task_id < len(tasks):
#         tasks[task_id] = updated_task
#         return updated_task
#     raise HTTPException(status_code=404, detail="task not found")

# @app.delete("/tasks/{task_id}", response_model=Task)
# def delete_task_from_id(task_id: int):
#     if 0 <= task_id < len(tasks):
#         return tasks.pop(task_id)
#     raise HTTPException(status_code=404, detail="task not found")



from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    title: str
    description: str = ""

tasks = []

@app.get("/tasks")
def read_tasks():
    return tasks or {"message": "No tasks available"}

@app.post("/tasks")
def add_task(task: Task):
    tasks.append(task)
    return {"message": "Task added successfully", "task": task}

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    try:
        return tasks[task_id]
    except IndexError:
        raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    try:
        tasks[task_id] = updated_task
        return {"message": "Task updated", "task": updated_task}
    except IndexError:
        raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    try:
        deleted_task = tasks.pop(task_id)
        return {"message": "Task deleted", "task": deleted_task}
    except IndexError:
        raise HTTPException(status_code=404, detail="Task not found")