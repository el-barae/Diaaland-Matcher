"""
from src.schemas.models import Jobs, Skills, Experiences, Educations, Certificates
from sqlalchemy.orm import Session
from src.db_utils.db_connector import db_connect
from src.feature_extraction.jobInfoExtraction import JobInfoExtraction
#from src.feature_extraction.Matcher import Matcher
from resources import DEGREE_IMPORTANCE
import json
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
from eureka_client import register_with_eureka
from src.routes.extractCV import router as extract_router
from src.routes.Matcher import router as matcher_router

"""
def get_db():
    db = db_connect("postgresql", "postgres", "host", "database")
    try:
        yield db
    finally:
        db.close()

def add_to_database(job_entities, model, entity, session= Depends(get_db)):
    for label in job_entities[entity]:
        found = session.query(model).filter(model.name == label).first()

        if found is None:
            found = model(name=label, type_=model.__tablename__)
            session.add(found)
    session.commit()
    session.close()

# Define a dependency for job extraction
def get_job_extractor(db: Session = Depends(get_db)):
    skills_pattern_path = "resources/data/skills.jsonl"
    model_path = "model_path"
    tokenizer_path = "tokenizer_path"
    return JobInfoExtraction(model_path, tokenizer_path, DEGREE_IMPORTANCE, skills_pattern_path, db, Jobs)


app = FastAPI()


# Define the endpoint
@app.get("/extraction/{job_id}")
async def extract_job(job_id, job_extractor: JobInfoExtraction = Depends(get_job_extractor)):
    # Extract job information
    job_entities = job_extractor.extract_entities(job_id)

    if job_entities is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return job_entities


@app.get("/matching/{job_id}")
async def matching(job_id):

    # Connect to database:
    session = db_connect("postgresql", "username", "host", "database")

    # Get the job offer:
    job = session.query(Jobs).filter(Jobs.id == job_id).first()

"""

@asynccontextmanager
async def lifespan(app: FastAPI):
    register_with_eureka()
    yield
    # Ici, tu peux ajouter la désinscription si tu veux plus tard

app = FastAPI(lifespan=lifespan)

@app.get("/")
def hello():
    return {"message": "Hello from FastAPI with Eureka!"}


# Include your routes
app.include_router(extract_router)
app.include_router(matcher_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



# # Run the app
# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host='127.0.0.1', port=8000)


