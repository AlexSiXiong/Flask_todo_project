from fastapi import FastAPI, Form

# uvicorn fastapi_start:app --reload

app=FastAPI()

DISHES = {
    "China": "dumplings",
    "New Zealand": "fish&chips",
    "India": "yellow curry"
}

@app.get("/init")
async def init():
    return {"msg":"hello world."}


@app.get("/")
async def get_all_dishes():
    return DISHES


@app.get("/{country_name}")
async def get_dish(country_name):
    return DISHES[country_name]

@app.post("/") 
async def add_dish(country_name, dish_name):
    assert len(country_name) > 0
    assert len(dish_name) > 0

    DISHES[country_name] = dish_name
    return {"msg": "a dish added."}

@app.put("/{country_name}")
async def update_dish(country_name, dish_name):
    DISHES[country_name] = dish_name
    return {"msg": "a country's dish updated."}

@app.delete("/{country_name}")
async def delete_dish(country_name):
    del DISHES[country_name]
    return {"msg": "a country's dish removed."}

@app.post("/user/login")
async def user_login(username=Form(), password=Form()):
    return {
        "username": username,
        "password": password
    }