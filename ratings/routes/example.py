from fastapi import APIRouter

example = APIRouter()


@example.get("/")
def example_root():
    return {"Hello": "World"}
