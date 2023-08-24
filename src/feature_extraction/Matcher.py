import ast 
from sentence_transformers import SentenceTransformer, util
import numpy as np


class Matcher:
    
    def __init__(self, resumes, DEGREE_IMPORTANCE, jobs):
        self.resumes = resumes
        self.jobs = jobs
        self.degree_importance = DEGREE_IMPORTANCE

    @staticmethod
    def modify_data_type(data):
        for key in ["degrees", "skills", "experiences"]:
            data[key] = [ast.literal_eval(item) for item in data[key]]
        data['job_title'] = ast.literal_eval(data['job_title'])
        return data

    def modify_type_resume(self):
        for i in range(len(self.resumes)):
            self.resumes[i] = self.modify_data_type(self.resumes[i])
        return self.resumes

    def modify_type_job(self):
        for i in range(len(self.jobs)):
            self.jobs[i] = self.modify_data_type(self.jobs[i])
        return self.jobs

    def semantic_similarity(self, job_feature, resume_feature):
        model = SentenceTransformer("model_name") # still have to choose the best model for the task
        
        # Create sentence embeddings:
        job_embeddings = self.model.encode(job_feature, convert_to_tensor=True)
        resume_embeddings = self.model.encode(resume_feature, convert_to_tensor=True)

        # Calculate the cosine similarity
        cosine_scores = util.pytorch_cos_sim(job_embeddings, resume_embeddings)

        # Calculate the mean:
        similarity_score = np.mean(cosine_scores.cpu().numpy())
        return similarity_score

    def degree_matching(self, resumes, jobs, job_index):
        # Find the minimum required degree in the job:
        job_degrees = jobs["degrees"][job_index]
        min_required_degree = min(job_degrees, key=lambda degree: self.degree_importance[degree])

        # Create a new column to store the degree measure
        degree_measure_column = 'Degree job ' + str(job_index) + ' matching'
        resumes[degree_measure_column] = 0

        # Iterate through resumes and calculate the degree measure
        for i, resume in resumes.iterrows():
            resume_degrees = resume['degrees']
            max_resume_degree = max(resume_degrees, key=lambda degree: self.degree_importance.get(degree, 0))
            
            if self.degree_importance.get(max_resume_degree, 0) >= self.degree_importance[min_required_degree]:
                resumes.at[i, degree_measure_column] = 1

        return resumes


    def job_title_matching(self, resumes, jobs, job_index):
        job_job_title = jobs['job_title'][job_index]
        job_title_measure_column = 'Job title job ' + str(job_index) + ' matching'

        resumes[job_title_measure_column] = resumes['job_title'].apply(lambda resume_job_title: semantic_similarity(resume_job_title, job_job_title))

        return resumes

    @staticmethod
    def calculate_experience_similarity(job_exp, resume_experiences):
        max_similarity = max(semantic_similarity(job_exp, exp) for exp in resume_experiences)
        return max_similarity

    def experiences_matching(self, resumes, jobs, job_index):
        # Still didn't figure out how to take into consideration both years of exp and domaine of exp

        job_required_experiences = jobs['experiences'][job_index]
        job_experience_measure_column = 'Experiences job ' + str(job_index) + ' matching'
        for i, resume in resumes.iterrows():
            resume_experiences = resume['experiences']
            total_similarity = sum(
                self.calculate_experience_similarity(job_exp, resume_experiences)
                for job_exp in job_required_experiences
            )
            avg_similarity = total_similarity / len(job_required_experiences)
            resumes.at[i, job_experience_measure_column] = avg_similarity
        return resumes

    def skills_matching(self, resumes, jobs, job_index):
        job_required_skills = jobs['skills'][job_index]
        job_skills_measure_column = 'Skills job ' + str(job_index) + ' matching'
        job_skills = set(job_required_skills) # remove duplicates

        for i, resume in resumes.iterrows():
            resume_skills = set(resume['skills']) # remove duplicates
            score = sum(1 if skill in resume_skills else max(semantic_similarity(skill, resume_skill) for resume_skill in resume_skills) for skill in job_skills)
            avg_score = score / len(job_skills)
            resumes.at[i, job_skills_measure_column] = avg_score
        return resumes

    def matching_score(self, resumes, jobs, job_index):
        # Matching degrees, job_title, skills, and experiences
        resumes = self.degree_matching(resumes, jobs, job_index)
        resumes = self.job_title_matching(resumes, jobs, job_index)
        resumes = self.skills_matching(resumes, jobs, job_index)
        resumes = self.experiences_matching(resumes, jobs, job_index)

        job_title_col = 'Job title job ' + str(job_index) + ' matching'
        skills_col = 'Skills job ' + str(job_index) + ' matching'
        degree_col = 'Degree job ' + str(job_index) + ' matching'
        experiences_col = 'Experiences job ' + str(job_index) + ' matching'
        matching_score_col = "Matching score job " + str(job_index)

        resumes[matching_score_col] = (
            0.2 * resumes[degree_col] +
            0.3 * resumes[skills_col] +
            0.3 * resumes[experiences_col] +
            0.2 * resumes[job_title_col]
        ).round(3)

        return resumes



