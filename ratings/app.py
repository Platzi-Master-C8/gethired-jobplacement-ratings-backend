from fastapi import FastAPI
from ratings.routes import example_root

app = FastAPI(title="Jobplacement - Ratings API")
app.include_router(example_root)

