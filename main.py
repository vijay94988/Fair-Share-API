from fastapi import FastAPI
from pydantic import BaseModel
import json
# from typing import List


app = FastAPI()


Datafile = "groups.json"


class GroupCreate(BaseModel):
    group_name: str


def load_groups():
    try:
        with open(Datafile, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_groups(groups):
    with open(Datafile, "w") as f:
        json.dump(groups, f)


@app.get("/")
def root():
    return {"Message": "Bill Splitter API"}


@app.get("/groups")
def get_groups():
    return load_groups()


@app.post("/groups")
def create_group(userdata: GroupCreate):
    group = load_groups()

    next_id = max((item["group_id"] for item in group), default=0) + 1
    group_data = {
        "group_name": userdata.group_name,
        "group_id": next_id
    }

    group.append(group_data)
    save_groups(group)

    return group_data


@app.delete("/groups_delete/{item_id}")
def delete_groups(item_id: int):
    group = load_groups()

    group = [item for item in group if item["group_id"] != item_id]

    save_groups(group)

    return {"Message": "Group Deleted"}
