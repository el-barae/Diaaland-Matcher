from src.schemas.matchedResume import ResumeMatchedModel
from src.schemas.extractedJob import ExtractedJobModel
from src.schemas.job import JobDBModel
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


app = FastAPI()


@app.get("/extraction/{job_id}")
def extract_job(job_id):
    skills_pattern_path = "resources/data/skills.jsonl"
    model_path = "model_path"
    tokenizer_path = "tokenizer_path"

    # Connect to database:
    session = db_connect("postgresql", "username", "host", "database")
    
    # Initialize the job extractor
    job_extractor = JobInfoExtraction(model_path, tokenizer_path, DEGREE_IMPORTANCE, skills_pattern_path, session, JobDBModel)

    # Extract job information
    job = job_extractor.extract_entities(job_id)

    # Create an ExtractedJobModel instance
    extracted_job = ExtractedJobModel(
            id = job['id'],
            degrees = job['degrees'],
            job_title = job['job_title'],
            skills = job['skills'],
            experiences = job['experiences']
        )

    # Add the extracted job data to the database
    session.add(extracted_job)
    session.commit()
    session.close()

    # Convert the job data to JSON
    job_json = transform_dict_to_json(job)


    return jobs_json






if __name__ == "__main__":
    pass


