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


    # df --> dictionary and the values as lists.
    def degree_matching(self, resumes, job, job_index):
        pass

    def major_matching(self, resumes, jobs, job_index):
        pass

    def skills_matching(self, resume, jobs, job_index):
        pass
#    job_index : int = Field()
    # degrees_matching : float = Field()
    # job_title_matching : float = Field()
    # skills_matching :float = Field()
    # experiences_matching

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



