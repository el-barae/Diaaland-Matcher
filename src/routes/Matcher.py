from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
from sentence_transformers import SentenceTransformer, util
import numpy as np
from fastapi import APIRouter, HTTPException

router = APIRouter()

class CandidateDetails(BaseModel):
    candidateId: int
    skills: List[str]
    educations: List[Optional[str]]

class JobRequest(BaseModel):
    jobId: int
    jobDescription: str
    candidatesDetails: List[CandidateDetails]
    degrees: List[str]

class CandidateRequest(BaseModel):
    candidateId: int
    skills: List[str]
    educations: List[Optional[str]]
    jobsDetails: List[Dict[str, Any]]

class Matcher:
    def __init__(self, model: SentenceTransformer, degree_importance: Dict[str, int]):
        self.model = model
        self.degree_importance = degree_importance

    def semantic_similarity(self, job_feature: str, resume_feature: str) -> float:
        try:
            job_embeddings = self.model.encode(job_feature, convert_to_tensor=True)
            resume_embeddings = self.model.encode(resume_feature, convert_to_tensor=True)
            cosine_scores = util.pytorch_cos_sim(job_embeddings, resume_embeddings)
            return float(np.mean(cosine_scores.cpu().numpy()))
        except Exception as e:
            logging.error(f"Error calculating semantic similarity: {e}")
            return 0.0

    def matching_score_by_job(
        self, candidate: Dict[str, Any], job_description: str, job_degrees: List[str], job_id: int
    ) -> Dict[str, Any]:
        skills = candidate.get("skills", [])
        educations = [deg for deg in candidate.get("educations", []) if deg]
        candidate_id = candidate.get("candidateId")

        # --- Similarité sémantique entre description et skills ---
        skills_score = 0.0
        for skill in skills:
            skills_score += self.semantic_similarity(job_description, skill)
        if skills:
            skills_score /= len(skills)

        # --- Bonus mots-clés exacts ---
        job_text = job_description.lower()
        keyword_count = sum(1 for skill in skills if skill.lower() in job_text)
        keyword_boost = 0.05 * keyword_count  # chaque skill trouvé ajoute 0.05

        # --- Matching diplômes ---
        degree_score = 0.0
        if job_degrees and educations:
            min_required_degree = min(job_degrees, key=lambda d: self.degree_importance.get(d, 0))
            max_candidate_degree = max(educations, key=lambda d: self.degree_importance.get(d, 0))
            hierarchy_match = int(
                self.degree_importance.get(max_candidate_degree, 0) >= self.degree_importance.get(min_required_degree, 0)
            )
            # Bonus sémantique diplômes
            semantic_degree = max((self.semantic_similarity(job_description, deg) for deg in educations), default=0.0)
            degree_score = 0.5 * hierarchy_match + 0.5 * semantic_degree

        # --- Score final ---
        final_score = 0.7 * skills_score + 0.3 * degree_score + keyword_boost
        final_score = round(min(final_score, 1.0), 2)  # clamp à 1.0 max

        return {
            "idJob": job_id,
            "idCandidate": candidate_id,
            "matchingScore": final_score,
            "skillsScore": round(skills_score, 2),
            "degreeScore": round(degree_score, 2),
            "keywordBoost": round(keyword_boost, 2)
        }

    def matching_score_by_candidate(
        self, jobs: List[Dict[str, Any]], candidate_skills: List[str], candidate_degrees: List[str], candidate_id: int
    ) -> List[Dict[str, Any]]:
        candidate_data = {
            "skills": candidate_skills,
            "educations": candidate_degrees,
            "candidateId": candidate_id
        }
        results = []
        for job in jobs:
            job_id = job.get("id") or job.get("jobId", 0)
            job_desc = job.get("description") or job.get("jobDescription", "")
            job_degrees = job.get("degrees", [])
            match = self.matching_score_by_job(candidate_data, job_desc, job_degrees, job_id)
            results.append(match)
        return results


degree_importance = {
    "Primary School": 1,
    "Secondary School": 2,
    "High School": 3,
    "Baccalaureate": 4,
    "Bachelor": 5,
    "Licence": 5,
    "Master": 6,
    "Engineer": 6,
    "PhD": 7,
    "Doctorat": 7,
    "Postdoctoral": 8
}

# Charger le modèle une seule fois
model = SentenceTransformer("all-MiniLM-L6-v2")
matcher = Matcher(model, degree_importance)

@router.post("/match_resumes/")
async def match_resumes(job_request: JobRequest):
    try:
        results = []
        for candidate in job_request.candidatesDetails:
            candidate_data = {
                "candidateId": candidate.candidateId,
                "skills": candidate.skills,
                "educations": candidate.educations
            }
            # Appel sur l'instance matcher, pour chaque candidat
            match = matcher.matching_score_by_job(
                candidate=candidate_data,
                job_description=job_request.jobDescription,
                job_degrees=job_request.degrees,
                job_id=job_request.jobId
            )
            results.append(match)
        return results

    except Exception as e:
        logging.error(f"Error matching resumes: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/match_jobs/")
async def match_jobs(candidate_request: CandidateRequest):
    try:
        candidate_id = candidate_request.candidateId
        candidate_skills = candidate_request.skills or []
        candidate_degrees = [deg for deg in candidate_request.educations if deg]
        jobs = candidate_request.jobsDetails

        # Utilisation de l'instance
        results = matcher.matching_score_by_candidate(
            jobs=jobs,
            candidate_skills=candidate_skills,
            candidate_degrees=candidate_degrees,
            candidate_id=candidate_id
        )

        logging.info(f"Results for candidate {candidate_id}: {results}")
        return results

    except Exception as e:
        logging.error(f"Error in /match_jobs/: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
