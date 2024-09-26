import uvicorn

from fastapi import FastAPI
from routes.login import auth
from routes.resources import resource

app = FastAPI()
app.include_router(auth)
app.include_router(resource)


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)