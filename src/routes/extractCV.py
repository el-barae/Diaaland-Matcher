
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import fitz  # PyMuPDF
import re

router = APIRouter()

# Sample list of skills
skills = [
    "Java", "Python", "C", "C++", "C#", "JavaScript", "Ruby", "Go", "PHP", "Swift",
    "Kotlin", "HTML", "CSS", "SQL", "No SQL", "MongoDB", "React", "Angular", "Vue",
    ".Net", "Spring", "Laravel", "Node", "Django", "Flask", "Cloud Computing",
    "Cybersecurity", "DevOps", "Flutter", "React Native", "Project planning",
    "Project management", "Project conception", "Data Analysis", "Business Intelligence",
    "Artificial Intelligence", "Machine learning", "Natural Language Processing (NLP)",
    "Virtualization", "Internet of Things", "Problem solving", "Communication", "Linux", "Commands", "Agile", "Data warehouse",
    "web scrapping", "Jquery", "Ajax", "Bootstrap" , "Tailwind", "Frontend", "Backend", "UML", "Conception"
]

# Common education degree patterns
degree_patterns = [
    r"Bachelor[^\n,]*",
    r"Licence[^\n,]*",
    r"Master[^\n,]*",
    r"Engineer[^\n,]*",
    r"Engineering[^\n,]*",
    r"Baccalaureate[^\n,]*",
    r"Baccalaureat[^\n,]*",
    r"Doctorat[^\n,]*",
    r"Diplome[^\n,]*",
    r"Ph\.?D[^\n,]*",
    r"Associate[^\n,]*",
    r"Diploma[^\n,]*",
    r"Degree[^\n,]*",
    r"Doctor[^\n,]*",
    r"Certificate[^\n,]*",
    r"Certificat[^\n,]*",
    r"Certification[^\n,]*",
    r"Course[^\n,]*",
    r"Graduate[^\n,]*",
    r"Undergraduate[^\n,]*",
    r"High School[^\n,]*",
    r"Secondary School[^\n,]*",
    r"Primary School[^\n,]*",
    r"Postdoctoral[^\n,]*",
    r"Fellowship[^\n,]*",
    r"Residency[^\n,]*",
    r"Major[^\n,]*",
    r"Minor[^\n,]*",
    r"Concentration[^\n,]*"
]

class ExtractRequest(BaseModel):
    file_path: str

def extract_text(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_skills(text):
    extracted_skills = [skill for skill in skills if skill.lower() in text.lower()]
    return extracted_skills

def extract_educations(text):
    extracted_educations = []
    for pattern in degree_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        extracted_educations.extend(matches)
    return extracted_educations

@router.post('/extract')
async def extract(request: ExtractRequest):
    if not request.file_path:
        raise HTTPException(status_code=400, detail="Invalid request body")

    file_path = request.file_path
    try:
        text = extract_text(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read the file: {e}")

    extracted_skills = extract_skills(text)
    extracted_educations = extract_educations(text)

    return {
        'skills': extracted_skills,
        'educations': extracted_educations
    }
