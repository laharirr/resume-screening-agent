from resume_parser.resume_parser import parse_resume_folder
from similarity.ranking import rank_candidates

# Read resumes
resumes = parse_resume_folder("data/resumes")

# Read JD
with open("data/jd/job_description.txt", "r", encoding="utf-8") as f:
    jd = f.read()

# Rank candidates
results = rank_candidates(jd, resumes)

print("\n===== Candidate Rankings =====\n")

for candidate in results:
    print(
        f"{candidate['candidate']}  -->  {candidate['score']:.2f}%"
    )