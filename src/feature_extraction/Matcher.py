import ast 
from sentence_transformers import SentenceTransformer, util
import numpy as np

# get data from the data base as a list of dictionaries and then get the elements of the dictionary one by one from different tables in the database

class Matcher:
    
    def __init__(self, resumes, DEGREE_IMPORTANCE, job_entities):
        self.resumes = resumes
        self.job_entities = job_entities
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
        self.job_entities = self.modify_data_type(self.job_entities)
        return self.job

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

    def degree_matching(self, resumes, job_entities):
        # Find the minimum required degree in the job:
        job_degrees = job_entities['degrees']
        min_required_degree = min(job_degrees, key=lambda degree: self.degree_importance[degree])

        # Create a new key:value pair to store the degree measure
        degree_measure = 'Degree job ' + str(job_index) + ' matching'

        # Iterate through resumes and calculate the degree measure
        for i, resume in enumerate(resumes):
            resume_degrees = resume['degrees']
            max_resume_degree = max(resume_degrees, key=lambda degree: self.degree_importance.get(degree, 0))
            
            if self.degree_importance.get(max_resume_degree, 0) >= self.degree_importance[min_required_degree]:
                resumes[i][degree_measure] = 1

        return resumes


    def job_title_matching(self, resumes, job_entities):
        job_job_title = job_entities['job_title']
        job_title_measure = 'Job title job ' + str(job_index) + ' matching'
        
        for i, resume in enumerate(resumes):
            resumes[i][job_title_measure] = semantic_similarity(resume['job_title'], job_job_title)

        return resumes

    @staticmethod
    def calculate_experience_similarity(job_exp, resume_experiences):
        max_similarity = max(semantic_similarity(job_exp, exp) for exp in resume_experiences)
        return max_similarity

    def experiences_matching(self, resumes, job_entities):
        # Still didn't figure out how to take into consideration both years of exp and domaine of exp

        job_required_experiences = job_entities['experiences']
        job_experience_measure = 'Experiences job ' + str(job_index) + ' matching'
        for i, resume in enumerate(resumes):
            resume_experiences = resume['experiences']
            total_similarity = sum(
                self.calculate_experience_similarity(job_exp, resume_experiences)
                for job_exp in job_required_experiences
            )
            avg_similarity = total_similarity / len(job_required_experiences)
            resumes[i][job_experience_measure] = avg_similarity
        return resumes

    def skills_matching(self, resumes, job_entities):
        job_required_skills = job_entities['skills']
        job_skills_measure = 'Skills job ' + str(job_index) + ' matching'
        job_skills = set(job_required_skills) # remove duplicates

        for i, resume in enumerate(resumes):
            resume_skills = set(resume['skills']) # remove duplicates
            score = sum(1 if skill in resume_skills else max(semantic_similarity(skill, resume_skill) for resume_skill in resume_skills) for skill in job_skills)
            avg_score = score / len(job_skills)
            resumes[i][job_skills_measure] = avg_score
        return resumes

    def matching_score(self, resumes, job_entities):
        # Matching degrees, job_title, skills, and experiences
        resumes = self.degree_matching(resumes, job_entities)
        resumes = self.job_title_matching(resumes, job_entities)
        resumes = self.skills_matching(resumes, job_entities)
        resumes = self.experiences_matching(resumes, job_entities)

        job_title = 'Job title job ' + str(job_index) + ' matching'
        skills = 'Skills job ' + str(job_index) + ' matching'
        degree = 'Degree job ' + str(job_index) + ' matching'
        experiences = 'Experiences job ' + str(job_index) + ' matching'
        matching_score = "Matching score job " + str(job_index)

        for i, resume in enumerate(resumes):
            resumes[i][matching_score] = (
                0.2 * resume[degree] +
                0.3 * resume[skills] +
                0.3 * resume[experiences] +
                0.2 * resume[job_title]
            ).round(3)

        return resumes



