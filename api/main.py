import os
import sys
import shutil

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from resume_parser.resume_parser import parse_resume_folder
from extraction.extractor import extract_resume_data
from similarity.ranking import rank_candidates


app = FastAPI(
    title="AI Resume Screening Agent API",
    description="Resume Ranking using NLP and Machine Learning",
    version="1.0.0",
)


UPLOAD_FOLDER = "data/uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class ResumeRequest(BaseModel):
    job_description: str



@app.get("/")
def home():
    return {
        "project": "AI Resume Screening Agent",
        "status": "Running",
        "version": "1.0"
    }


@app.get("/health")
def health():
    return {
        "status": "Healthy"
    }


@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "status": "Uploaded Successfully"
    }



@app.post("/rank")
def rank_resume(request: ResumeRequest):

    resumes = parse_resume_folder(UPLOAD_FOLDER)

    if len(resumes) == 0:
        raise HTTPException(
            status_code=404,
            detail="No resumes uploaded."
        )

    extracted = {}

    for filename, text in resumes.items():
        extracted[filename] = extract_resume_data(text)

    results = rank_candidates(
        request.job_description,
        resumes,
        extracted,
    )

    response = []

    for candidate in results:

        response.append(
            {
                "candidate": candidate["candidate"],
                "semantic_score": candidate["semantic_score"],
                "skill_score": candidate["skill_score"],
                "education_score": candidate["education_score"],
                "experience_score": candidate["experience_score"],
                "certification_score": candidate["certification_score"],
                "completeness_score": candidate["completeness_score"],
                "final_score": candidate["final_score"],
                "recommendation": candidate["recommendation"],
            }
        )

    return {
        "total_candidates": len(response),
        "results": response
    }