
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List
import fitz  # PyMuPDF
import re
import io

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

def extract_skills(text: str):
    extracted = []
    lower_text = text.lower()
    for skill in skills:
        # match sans espace / casse
        if skill.lower().replace(" ", "") in lower_text.replace(" ", ""):
            extracted.append(skill)
    return list(set(extracted))  # éviter doublons

def extract_educations(text: str):
    extracted = []
    for pattern in degree_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        extracted.extend(matches)
    return list(set(extracted))


@router.post("/extract")
async def extract(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        # ouvrir directement depuis mémoire
        with fitz.open(stream=contents, filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text("text")  # "text" = layout simple

        extracted_skills = extract_skills(text)
        extracted_educations = extract_educations(text)

        return {
            "skills": extracted_skills,
            "educations": extracted_educations
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {e}")