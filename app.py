from resume_parser.resume_parser import parse_resume_folder
from extraction.extractor import extract_resume_data

resumes = parse_resume_folder("data/resumes")

for filename, text in resumes.items():

    print("\n" + "=" * 60)
    print(filename)
    print("=" * 60)

    data = extract_resume_data(text)

    for key, value in data.items():
        print(f"{key}: {value}")