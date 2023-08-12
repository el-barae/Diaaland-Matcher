import ast 
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from resources import DEGREE_IMPORTANCE


class Matcher:
    
    def __init__(self, labels, resume, job):
        self.labels = labels
        self.resume = resume
        self.job = job
        self.degree_importance = DEGREE_IMPORTANCE

    def modifying_type_resume(self, resume):
        for i in range(len(resume["degrees"])):
            resume["degrees"][i] = ast.literal_eval(resume["degrees"][i])
        for i in range(len(resume["skills"])):
            resume["skills"][i] = ast.literal_eval(resume["skills"][i])
        for i in range(len(resume["experiences"])):
            resume["experiences"][i] = ast.literal_eval(resume["experiences"][i])
        resume['job_title'][i] = ast.literal_eval(resume['job_title'])
        return resume

    def job(self, job):
        for i in range(len(jon["degrees"])):
            job["degrees"][i] = ast.literal_eval(job["degrees"][i])
        for i in range(len(resume["skills"])):
            job["skills"][i] = ast.literal_eval(job["skills"][i])
        for i in range(len(resume["experiences"])):
            job["experiences"][i] = ast.literal_eval(job["experiences"][i])
        job['job_title'][i] = ast.literal_eval(job['job_title'])
        return job

    @staticmethod
    def unique_skills(jobs, job_index):
        pass

    # df --> dictionary and the values as lists.
    def degree_matching(self, resumes, jobs, job_index):
        # Find the minimum required degree in the job:
        job_degree = self.degree_importance[min([jobs["degrees"][job_index][i] for i in range(len(jobs["degree"][job_index]))])]
        resumes['Degree measure' + str(job_index)] = 0
        for i, resume in resumes.iterrows():
            resume_degree = self.degree_importance(max([resume['degrees'][i] for i in range(len(resume['degrees'][i]))]))
            if resume_degree >= job_degree:
                resumes.loc[i, 'Degree measure ' + str(job_index)] = 1
        return resumes

    def job_title_matching(self, resumes, jobs, job_index):
        job_job_title = jobs['job_title'][job_index]
        resumes['Job title measure ' + str(job_index)] = 0
        for i, resume in resumes.iterrows():
            resume_job_title = resume['job_title']
            resumes.loc[i, 'Job title measure ' + str(job_index)] = semantic_similarity(resume_job_title, job_job_title)
        return resumes

    def experiences_matching(self, resumes, jobs, job_index):
        job_required_experiences = jobs['experiences'][job_index]
        resumes['Experiences measure ' + str(job_index)] = 0
        for i, resume in resumes.iterrows():
            resume_experiences = resume['experiences']
            score = 0
            for job_exp in job_required_experiences:
                temp = 0
                for resume_exp in resumes_experiences:
                    temp = max(temp, semantic_similarity(job_exp, resume_exp))
                score += temp
            resumes.loc[i, 'Experiences measure ' + str(job_index)] = score / len(job_exp)
        return resumes

    def skills_matching(self, resume, jobs, job_index):
        pass

    def matching_score(self, resumes, jobs, job_index):
        # matching degrees:
        resumes = self.degree_matching(resumes, jobs, job_index)
        # matching job_title:
        resumes = self.job_title_matching(resumes, jobs, job_index)
        # matching skills:
        resumes = self.skills_matching(resumes, jobs, job_index)
        # matching experiences
        resumes = self.experiences_matching(resumes, jobs, job_index)

        for i, row in self.resumes.iterrows():
            skills_score = resumes['Skills job ' + str(job_index) + ' matching'][i]
            degree_score = resumes['Degree job ' + str(job_index) + ' matching'][i]
            jobtitle_score = resumes['Job title job ' + str(job_index) + ' matching'][i]
            experiences_score = resumes['Experiences job ' + str(job_index) + ' matching'][i]
            final_score = (0.2 * degree_score + 0.3 * skills_score + 0.3 * experiences_score + 0.2 * jobtitle_score)
            resumes.loc[i, "matching score job " + str(job_index)] = round(final_score, 3)

        return resumes



