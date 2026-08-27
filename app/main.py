from fastapi import FastAPI, Response, status
from pydantic import BaseModel
import json
# from typing import List


app = FastAPI()


Datafile = "groups.json"


class GroupCreate(BaseModel):
    group_name: str


def load_group():
    try:
        with open(Datafile, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_group(groups):
    with open(Datafile, "w") as f:
        json.dump(groups, f)


@app.get("/")
def root():
    return {"Message": "Bill Splitter API"}


@app.get("/groups")
def get_group():
    return load_group()


@app.post("/groups", status_code=status.HTTP_201_CREATED)
def create_group(userdata: GroupCreate):
    groups = load_group()

    next_id = max((item["group_id"] for item in groups), default=0) + 1
    group_data = {
        "group_name": userdata.group_name,
        "group_id": next_id
    }

    groups.append(group_data)
    save_group(groups)

    return group_data


@app.delete("/groups/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(item_id: int, response: Response):
    groups = load_group()
    original_len = len(groups)
    groups = [item for item in groups if item["group_id"] != item_id]
    if len(groups) == original_len:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Message": "Group Not Found"}

    save_group(groups)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/groups/{item_id}")
def update_group(item_id: int, userdata: GroupCreate, response: Response):
    groups = load_group()
    original_len = len(groups)
    groups = [item for item in groups if item["group_id"] != item_id]
    if len(groups) == original_len:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Message": "Group Not Found"}

    group_data = {
        "group_id" :item_id, "group_name": userdata.group_name
    }

    groups.append(group_data)
    save_group(groups)
    return {"Message": "Group Updated"}

