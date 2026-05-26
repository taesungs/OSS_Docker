from fastapi import FastAPI
from pydantic import BaseModel
import json
from pathlib import Path

app = FastAPI()

DATA_FILE = Path("courses.json")


class Course(BaseModel):
    name: str
    year: int
    semester: str
    credit: int


def load_courses():
    if not DATA_FILE.exists():
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_courses(courses):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(courses, f, ensure_ascii=False, indent=4)


@app.get("/")
def root():
    return {"message": "FastAPI Docker Course API"}


@app.get("/courses")
def get_courses():
    return load_courses()


@app.post("/courses")
def add_course(course: Course):
    courses = load_courses()
    courses.append(course.model_dump())
    save_courses(courses)
    return {
        "message": "Course added successfully",
        "course": course
    }