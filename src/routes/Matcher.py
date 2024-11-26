from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
from sentence_transformers import SentenceTransformer, util
import numpy as np
from fastapi import HTTPException

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
            similarity_score = np.mean(cosine_scores.cpu().numpy())
            return similarity_score
        except Exception as e:
            logging.error(f"Error calculating semantic similarity: {e}")
            return 0.0

    def degree_matching(self, candidates: List[Dict[str, Any]], job_degrees: List[str]) -> List[Dict[str, Any]]:
        min_required_degree = min(job_degrees, key=lambda degree: self.degree_importance.get(degree, 0))
        degree_measure = 'Degree job matching'

        for i, candidate in enumerate(candidates):
            candidate_degrees = candidate.get('educations', [])
            if not candidate_degrees:
                candidates[i][degree_measure] = 0
                continue

            candidate_degrees = [degree for degree in candidate_degrees if degree is not None]
            if not candidate_degrees:
                candidates[i][degree_measure] = 0
                continue

            max_candidate_degree = max(candidate_degrees, key=lambda degree: self.degree_importance.get(degree, 0))
            candidates[i][degree_measure] = int(self.degree_importance.get(max_candidate_degree, 0) >= self.degree_importance.get(min_required_degree, 0))
        return candidates

    def skills_matching(self, candidates: List[Dict[str, Any]], job_skills: List[str]) -> List[Dict[str, Any]]:
        job_skills_measure = 'Skills job matching'

        for i, candidate in enumerate(candidates):
            candidate_skills = candidate.get('skills', [])
            if not candidate_skills:
                candidates[i][job_skills_measure] = 0.0
                continue

            score = 0
            for job_skill in job_skills:
                if job_skill in candidate_skills:
                    score += 1
                else:
                    similarity_scores = [self.semantic_similarity(job_skill, candidate_skill) for candidate_skill in candidate_skills]
                    max_similarity = max(similarity_scores, default=0.0)
                    score += max_similarity

            avg_score = score / len(job_skills) if job_skills else 0
            candidates[i][job_skills_measure] = avg_score
        return candidates

    def matching_score_by_job(self, candidates: List[Dict[str, Any]], job_description: str, job_degrees: List[str], job_id: int) -> List[Dict[str, Any]]:
        candidates = self.degree_matching(candidates, job_degrees)
        job_skills = job_description.split()  # Extract skills from job description for simplicity
        candidates = self.skills_matching(candidates, job_skills)
        matching_score_key = "Matching score job"

        for i, candidate in enumerate(candidates):
            degree_score = candidate.get('Degree job matching', 0)
            skills_score = candidate.get('Skills job matching', 0)
            candidates[i][matching_score_key] = round(0.2 * degree_score + 0.8 * skills_score, 2)

        # Return only required fields
        return [{
            "idCandidate": candidate.get("candidateId", ""),
            "idJob": job_id,
            "matchingScore": candidate[matching_score_key]
        } for candidate in candidates]

    def matching_score_by_candidates(self, jobs: List[Dict[str, Any]], candidate_skills: List[str], candidate_degrees: List[str], candidate_id: int) -> List[Dict[str, Any]]:
        candidate_data = [{'skills': candidate_skills, 'educations': candidate_degrees, 'candidateId': candidate_id}]
        matching_jobs = []

        for job in jobs:
            job_description = job['description']
            job_degrees = job['degrees']
            job_id = job.get("id", 0)
            matched_candidate = self.matching_score_by_job(candidate_data, job_description, job_degrees, job_id)[0]
            matching_jobs.append({
                "idJob": job_id,
                "idCandidate": matched_candidate["idCandidate"],
                "matchingScore": matched_candidate["matchingScore"]
            })

        return matching_jobs


@router.post("/match_resumes/")
async def match_resumes(job_request: JobRequest):
    try:
        candidates_data = [
            {"candidateId": candidate.candidateId, "skills": candidate.skills, "educations": candidate.educations}
            for candidate in job_request.candidatesDetails
        ]
        job_description = job_request.jobDescription
        job_degrees = job_request.degrees
        job_id = job_request.jobId
        result = matcher.matching_score_by_job(candidates_data, job_description, job_degrees, job_id)
        return result
    except Exception as e:
        logging.error(f"Error matching resumes: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/match_jobs/")
async def match_jobs(candidate_request: CandidateRequest):
    try:
        candidate_skills = candidate_request.skills
        candidate_degrees = candidate_request.educations
        candidate_id = candidate_request.candidateId
        jobs_data = candidate_request.jobsDetails
        result = matcher.matching_score_by_candidates(jobs_data, candidate_skills, candidate_degrees, candidate_id)
        return result
    except Exception as e:
        logging.error(f"Error matching jobs: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
