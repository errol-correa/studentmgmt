from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Enable CORS (For local testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/frontend", StaticFiles(directory="frontend"), name="static")

# In-memory task list
tasks = [{"id": 1, "text": "Sample Task 1"}, {"id": 2, "text": "Sample Task 2"}]
task_counter = 3  # Unique ID counter

# Define Task Model
class Task(BaseModel):
    text: str  # Only text, ID is auto-generated

@app.get("/tasks")
def get_tasks():
    return tasks


@app.post("/tasks")
def add_task(task: Task):
    global task_counter
    new_task = {"id": task_counter, "text": task.text}
    tasks.append(new_task)
    task_counter += 1
    return {"message": "Task added successfully", "task": new_task}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return {"message": "Task deleted successfully"}