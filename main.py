from src.schemas.models import Jobs, Skills, Experiences, Educations, Certificates
from src.db_utils.db_connector import db_connect
from src.feature_extraction.jobInfoExtraction import JobInfoExtraction
from src.feature_extraction.Matcher import Matcher
from resources import DEGREE_IMPORTANCE
import json
import pandas as pd
from fastapi import FastAPI


def transform_dict_to_json(data_dict):
    json_data = json.dumps(data_dict, indent=4)
    return json_data

def add_to_database(job_entities, session, model, entity):
    for label in job_entities[entity]:
        found = session.query(model).filter(model.name == label).first()

        if found is None:
            found = model(name=label, type_=model.__tablename__)
            session.add(found)
    session.commit()
    session.close()

app = FastAPI()


@app.get("/extraction/{job_id}")
def extract_job(job_id):
    skills_pattern_path = "resources/data/skills.jsonl"
    model_path = "model_path"
    tokenizer_path = "tokenizer_path"

    # Connect to database:
    session = db_connect("postgresql", "username", "host", "database")
    
    # Initialize the job extractor
    job_extractor = JobInfoExtraction(model_path, tokenizer_path, DEGREE_IMPORTANCE, skills_pattern_path, session, Jobs)

    # Extract job information
    job_entities = job_extractor.extract_entities(job_id)

    # Add Extracted skills to the database:
    add_to_database(job_entities, session, Skills, "skills")

    # Add Extracted experiences to the database:
    add_to_database(job_entities, session, Experiences, "experiences")

    # Add Extracted educations to the database:
    add_to_database(job_entities, session, Educations, "degrees")

    # Add Extracted certificates to the database:
    add_to_database(job_entities, session, Certificates, "certificates")

    # Add Extracted Job title to the database:
    add_to_database(job_entities, session, Jobs, "job_title")


    # Convert the job data to JSON
    job_json = transform_dict_to_json(job_entities)


    return job_json






if __name__ == "__main__":
    pass


