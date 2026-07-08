from resume_parser.resume_parser import parse_resume_folder
from similarity.ranking import rank_candidates

# Parse resumes
resumes = parse_resume_folder("data/resumes")

# Read job description
with open("data/jd/job_description.txt", "r", encoding="utf-8") as file:
    job_description = file.read()

# Rank candidates
results = rank_candidates(job_description, resumes)

print("\n===== Resume Ranking =====\n")

for candidate in results:
    print(candidate)