from fastapi import FastAPI
from pydantic import BaseModel
import json
# from typing import List


app = FastAPI()


class GroupCreate(BaseModel):
    group_name: str

@app.get("/")
def root():
    return {"message": "Bill Splitter API"}

Datafile = "groups.json"
@app.post("/groups")
def create_group(userdata: GroupCreate):
    try:
        with open(Datafile, "r") as f:
            group = json.load(f)
    except FileNotFoundError:
        return []

    next_id = max((item["group_id"] for item in group), default=0) + 1
    group_data = {
        "group_name": userdata.group_name,
        "group_id": next_id
    }
    group.append(group_data)
    with open(Datafile, "w")as f:
        json.dump(group, f)
    return group_data


@app.get("/groups")
def get_groups():
    with open(Datafile, "r") as f:
        return json.load(f)

@app.delete("/groups_delete/{item_id}")
def delete_groups(item_id: int):
    with open(Datafile, "r") as f:
        group = json.load(f)
    group = [item for item in group if item["group_id"] != item_id]
    with open(Datafile, "w") as f:
        json.dump(group, f)









