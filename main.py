from src.schemas.matchedResume import ResumeMatchedModel
from src.schemas.extractedJob import JobModel
from src.db_utils.db_connector import db_connect
from src.feature_extraction.jobInfoExtraction import JobInfoExtraction
from src.feature_extraction.Matcher import Matcher
import json
import pandas as pd
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder


def dataframe_to_json(dataframe):
    # Transforms dataframe into a json file format
    
    temp = dataframe.to_json(orinet="records")
    parsed = json.loads(temp)
    json_data = json.dumps(parsed, indent=4)

    return json_data

app = FastAPI()



if __name__ == "__main__":
    pass


