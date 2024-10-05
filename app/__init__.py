from fastapi import FastAPI, HTTPException
from sqlmodel import select
from db import Task, TaskCreate, Config, Model


app = FastAPI(debug=True)


@app.get("/task/list", response_model=list[Task])
def task_list():
    response = Config.session.scalars(select(Task))
    return response


@app.get("/task/{name}", response_model=list[Task])
def task_get(name:str):
    response = Config.session.scalars(select(Task).where(Task.name == name)).one_or_none
    return response


@app.post("/task/create")
def task_create(task: TaskCreate):
    with Config.SESSION.begin() as session:
        query = select(Model).where(Model.name == task.name)
        model = (
            session.scalars(query).one_or_none()
            or session.scalars(select(Model)).first()
        )
        if not model:
            raise HTTPException(status_code=404, detail="Name not found")
        session.add(
            Task(
                name=task.name,
                model=task.for_what,
                money=task.money,
                result=task.result,
            )
        )
        return{"ok":True}


def get_task():
    if task_item:
        task_item.sqlmodel_update(task)

@app.put("/task/edit", response_model=list[dict])
def task_edit(task:Task):
    with Config.SESSION.begin() as session:
        query = select(Task).where(Task.id == task.id)
        task_item = session.scalars(query).one_or_none()
        if task_item:
            task_item = get_task(task_id=int(task.id))
            return{"If you done the task write 'complete' instead 'incomplete'":True}
        else:
            raise HTTPException(status_code=404, detail="Task not found")
        

@app.put("/task/info/complete", response_model = list[dict])
def task_info(task:Task):
    with Config.SESSION.begin()as session:
        query = select(Task).where(Task.id ==task.id)
        task_item = session.scalars(query).one_or_none()
        result_task = task_item.result
        for x in task_item:
            if result_task == "complete":
                task_item = get_task(task_id=int(task.id))
                return{"This is only 'complete' tasks":True}
            
            

@app.put("/task/info/incomplete", response_model = list[dict])
def task_info(task:Task):
    with Config.SESSION.begin()as session:
        query = select(Task).where(Task.id ==task.id)
        task_item = session.scalars(query).one_or_none()
        result_task = task_item.result
        for x in task_item:
            if  result_task == "incomplete":
                task_item = get_task(task_id=int(task.id))
                return{"This is only 'incomplete' tasks":True}
                

@app.delete("/task/delete", response_model=list[dict])
def task_delete(task:Task):
    with Config.SESSION.begin() as session:
        query = select(Task).where(Task.id == task.id)
        task_item = session.scalars(query).one_or_none()
        if task_item:
            session.delete(task_item)
            return{"ok":True}
        else:
            raise HTTPException(status_code=404, detail="Task not found")
        