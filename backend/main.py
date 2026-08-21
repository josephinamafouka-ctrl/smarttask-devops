from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import psycopg2
from pydantic import BaseModel

app = FastAPI(title="SmartTask API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:secretpassword@db:5432/smarttask")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@app.get("/")
def read_root():
    return {"message": "API SmartTask opérationnelle !"}

@app.get("/tasks")
def get_tasks():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, title, completed FROM tasks;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [{"id": r[0], "title": r[1], "completed": r[2]} for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class TaskCreate(BaseModel):
    title: str

@app.post("/tasks")
def create_task(task: TaskCreate):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO tasks (title) VALUES (%s) RETURNING id, title, completed;", (task.title,))
        new_task = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return {"id": new_task[0], "title": new_task[1], "completed": new_task[2]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
