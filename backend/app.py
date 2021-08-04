import os
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional, List
import motor.motor_asyncio
import uvicorn
from dotenv import load_dotenv, find_dotenv
import praw
from pymongo import MongoClient

from models import StudentModel, UpdateStudentModel, SubredditModel
from scanners.subreddits import SubredditsScraper

load_dotenv(find_dotenv())
app = FastAPI()


@app.get("/subreddits/default", response_description="Get the stats for the default subreddits", response_model=List[SubredditModel])
async def get_default_subreddits():
    client = MongoClient(username=os.getenv("MONGODB_USER"), password=os.getenv("MONGODB_PW"))
    reddit_client = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
        username=os.getenv("REDDIT_USERNAME"),
        password=os.getenv("REDDIT_PW"),
    )
    sel_vars = ["_path", "display_name", "subscribers", "over18", "icon_img"]
    sub_parser = SubredditsScraper(reddit_client, mongo_client=client, default=True,
                                   name="default_subreddit_scraper", variables=sel_vars)

    default_subreddits = sub_parser.get_stored_data()
    return default_subreddits


# @app.post("/", response_description="Add new student", response_model=StudentModel)
# async def create_student(student: StudentModel = Body(...)):
#     db = client.college
#     student = jsonable_encoder(student)
#     new_student = await db["students"].insert_one(student)
#     created_student = await db["students"].find_one({"_id": new_student.inserted_id})
#     return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_student)
#
#
# @app.get(
#     "/", response_description="List all students", response_model=List[StudentModel]
# )
# async def list_students():
#     db = client.college
#     students = await db["students"].find().to_list(1000)
#     return students
#
#
# @app.get(
#     "/{id}", response_description="Get a single student", response_model=StudentModel
# )
# async def show_student(id: str):
#     db = client.college
#     if (student := await db["students"].find_one({"_id": id})) is not None:
#         return student
#
#     raise HTTPException(status_code=404, detail=f"Student {id} not found")
#
#
# @app.put("/{id}", response_description="Update a student", response_model=StudentModel)
# async def update_student(id: str, student: UpdateStudentModel = Body(...)):
#     db = client.college
#     student = {k: v for k, v in student.dict().items() if v is not None}
#
#     if len(student) >= 1:
#         update_result = await db["students"].update_one({"_id": id}, {"$set": student})
#
#         if update_result.modified_count == 1:
#             if (
#                     updated_student := await db["students"].find_one({"_id": id})
#             ) is not None:
#                 return updated_student
#
#     if (existing_student := await db["students"].find_one({"_id": id})) is not None:
#         return existing_student
#
#     raise HTTPException(status_code=404, detail=f"Student {id} not found")
#
#
# @app.delete("/{id}", response_description="Delete a student")
# async def delete_student(id: str):
#     db = client.college
#     delete_result = await db["students"].delete_one({"_id": id})
#
#     if delete_result.deleted_count == 1:
#         return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
#
#     raise HTTPException(status_code=404, detail=f"Student {id} not found")
