from fastapi import FastAPI

app=FastAPI()

@app.get("/")
async def init():
    return {"msg":"hello world."}
