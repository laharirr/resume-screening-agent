import os
import sys
import json

# -------------------------------------------------
# Project Root
# -------------------------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd

# -------------------------------------------------
# Reports
# -------------------------------------------------

from reports.pdf_report import generate_pdf

# -------------------------------------------------
# Visualizations
# -------------------------------------------------

from visualization.charts import score_chart
from visualization.ats_gauge import ats_gauge
from visualization.radar_chart import skill_radar
from visualization.pie_chart import recommendation_chart

# -------------------------------------------------
# Analysis
# -------------------------------------------------

from analysis.recruiter_report import generate_report
from analysis.decision_panel import recruiter_decision
from analysis.candidate_comparison import candidate_comparison

# -------------------------------------------------
# Database
# -------------------------------------------------

from database.database import (
    create_table,
    save_results,
    load_history,
)

# -------------------------------------------------
# Resume Processing
# -------------------------------------------------

from file_utils import save_uploaded_file

from resume_parser.resume_parser import parse_resume_folder
from extraction.extractor import extract_resume_data
from similarity.ranking import rank_candidates

# -------------------------------------------------
# Export
# -------------------------------------------------

from exports.csv_export import export_csv
from exports.json_export import export_json

# -------------------------------------------------
# Streamlit
# -------------------------------------------------

st.set_page_config(
    page_title="AI Resume Screening Agent",
    page_icon="🤖",
    layout="wide",
)

create_table()

# -------------------------------------------------
# Sidebar
# -------------------------------------------------

st.sidebar.title("🤖 AI Resume Screening")

st.sidebar.markdown("---")

st.sidebar.info(
"""
### Features

✅ Resume Parsing

✅ Skill Extraction

✅ Semantic Similarity

✅ ATS Score

✅ Resume Ranking

✅ Recruiter Analysis

✅ CSV Export

✅ JSON Export

✅ PDF Export

✅ Dashboard Analytics
"""
)

st.sidebar.markdown("---")

st.sidebar.success("Version 1.0")

st.sidebar.caption(
    "Developed using Python • NLP • Machine Learning"
)

# -------------------------------------------------
# Title
# -------------------------------------------------

st.title("🤖 AI Resume Screening Agent")

st.markdown(
"""
Upload multiple resumes and compare them against a Job Description using
AI-powered semantic similarity and hybrid scoring.
"""
)

st.divider()

# -------------------------------------------------
# Upload
# -------------------------------------------------

uploaded_files = st.file_uploader(
    "Upload Resumes",
    type=["pdf", "docx"],
    accept_multiple_files=True,
)

job_description = st.text_area(
    "Paste Job Description",
    height=220,
)

# -------------------------------------------------
# Rank Button
# -------------------------------------------------

if st.button("🚀 Rank Candidates"):

    if not uploaded_files:
        st.error("Please upload resumes.")
        st.stop()

    if job_description.strip() == "":
        st.error("Please enter the Job Description.")
        st.stop()

    upload_folder = "data/uploads"

    os.makedirs(upload_folder, exist_ok=True)

    # Remove previous resumes
    for file in os.listdir(upload_folder):

        path = os.path.join(upload_folder, file)

        if os.path.isfile(path):
            try:
                os.remove(path)
            except PermissionError:
                pass

    # Save uploaded resumes
    for file in uploaded_files:
        save_uploaded_file(file)

    st.success("✅ Resumes Uploaded Successfully")

    # -------------------------------------------------
    # Ranking
    # -------------------------------------------------

    with st.spinner("Analyzing Resumes..."):

        resumes = parse_resume_folder(upload_folder)

        st.write("Number of resumes:", len(resumes))

        if len(resumes) == 0:
            st.error("No valid resumes found.")
            st.stop()

        extracted = {}

        for filename, text in resumes.items():
            extracted[filename] = extract_resume_data(text)

        try:

            print("=" * 60)
            print("Starting Ranking")

            results = rank_candidates(
                job_description,
                resumes,
            )

            save_results(results)

            print(results)

            print("=" * 60)

        except Exception as e:

            st.error(f"Ranking Error:\n{e}")

            raise e

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    export_csv(results)
    export_json(results)

    pdf_path = generate_pdf(results)
    # -------------------------------------------------
    # Dashboard Statistics
    # -------------------------------------------------

    st.header("📊 Dashboard Statistics")

    total_candidates = len(results)

    best_score = max(c["final_score"] for c in results)

    average_score = round(
        sum(c["final_score"] for c in results) / total_candidates,
        2
    )

    recommended = sum(
        1
        for c in results
        if c["recommendation"] == "Recommended"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Candidates",
        total_candidates
    )

    col2.metric(
        "Best Score",
        f"{best_score:.2f}"
    )

    col3.metric(
        "Average Score",
        f"{average_score:.2f}"
    )

    col4.metric(
        "Recommended",
        recommended
    )

    st.divider()

    # -------------------------------------------------
    # ATS Score
    # -------------------------------------------------

    winner = results[0]

    st.header("🎯 ATS Score")

    gauge = ats_gauge(
        winner["final_score"]
    )

    st.plotly_chart(
        gauge,
        width="stretch",
        key="ats_gauge"
    )

    if winner["final_score"] >= 85:
        st.success("Excellent ATS Match")

    elif winner["final_score"] >= 70:
        st.info("Good ATS Match")

    elif winner["final_score"] >= 50:
        st.warning("Average ATS Match")

    else:
        st.error("Low ATS Match")

    st.divider()

    # -------------------------------------------------
    # Best Candidate
    # -------------------------------------------------

    st.header("🏆 Best Candidate")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Candidate",
        winner["candidate"]
    )

    col2.metric(
        "Final Score",
        f"{winner['final_score']:.2f}"
    )

    col3.metric(
        "Recommendation",
        winner["recommendation"]
    )

    st.divider()

    # -------------------------------------------------
    # Candidate Ranking Chart
    # -------------------------------------------------

    st.header("📈 Candidate Ranking")

    ranking_chart = score_chart(results)

    st.plotly_chart(
        ranking_chart,
        width="stretch",
        key="candidate_ranking_chart"
    )

    st.divider()

    # -------------------------------------------------
    # Recommendation Distribution
    # -------------------------------------------------

    st.header("📊 Recommendation Distribution")

    pie_chart = recommendation_chart(results)

    st.plotly_chart(
        pie_chart,
        width="stretch",
        key="recommendation_pie_chart"
    )

    st.divider()

    # -------------------------------------------------
    # Candidate Search
    # -------------------------------------------------

    search = st.text_input(
        "🔍 Search Candidate"
    )

    filtered = results

    if search:

        filtered = [

            c

            for c in results

            if search.lower() in c["candidate"].lower()

        ]
    # -------------------------------------------------
    # Candidate Analysis
    # -------------------------------------------------

    st.header("📋 Candidate Analysis")

    jd_skills = [
        "Python",
        "SQL",
        "Machine Learning",
        "FastAPI",
        "Docker",
        "Git",
        "GitHub",
        "PostgreSQL",
        "LangChain",
    ]

    for i, candidate in enumerate(filtered, start=1):

        if i == 1:
            badge = "🥇 Gold Candidate"
        elif i == 2:
            badge = "🥈 Silver Candidate"
        elif i == 3:
            badge = "🥉 Bronze Candidate"
        else:
            badge = f"Rank #{i}"

        st.subheader(badge)

        resume_path = os.path.join(
            "data/uploads",
            candidate["candidate"]
        )

        with st.expander("📄 Resume Preview"):

            try:
                with open(resume_path, "rb") as f:

                    st.download_button(
                        "Download Resume",
                        data=f,
                        file_name=candidate["candidate"],
                        key=f"resume_{i}"
                    )

            except:
                st.warning("Resume not found.")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(f"## 👤 {candidate['candidate']}")

            st.write("Semantic Score")

            st.progress(candidate["semantic_score"] / 100)

            st.write(f"{candidate['semantic_score']:.2f}")

            st.write("Skill Score")

            st.progress(candidate["skill_score"] / 100)

            st.write(f"{candidate['skill_score']:.2f}")

            st.write("Final Score")

            st.progress(candidate["final_score"] / 100)

            st.write(f"{candidate['final_score']:.2f}")

            if candidate["final_score"] >= 90:
                st.success("🟢 Excellent Resume")

            elif candidate["final_score"] >= 75:
                st.success("🟢 Strong Resume")

            elif candidate["final_score"] >= 60:
                st.warning("🟡 Average Resume")

            else:
                st.error("🔴 Needs Improvement")

        with col2:

            report = generate_report(
                extracted[candidate["candidate"]],
                jd_skills,
                candidate["recommendation"]
            )

            st.write("### Recruiter Report")

            st.success(f"Matched Skills\n\n{report['Matched Skills']}")

            st.warning(f"Missing Skills\n\n{report['Missing Skills']}")

            st.info(f"Skill Match : {report['Match Percentage']}%")

            st.write("Recommendation")

            st.success(candidate["recommendation"])

            radar = skill_radar(
                extracted[candidate["candidate"]]["skills"],
                jd_skills
            )

            st.plotly_chart(
                radar,
                width="stretch",
                key=f"radar_{i}"
            )

        st.divider()

    # -------------------------------------------------
    # AI Recruiter Decision
    # -------------------------------------------------

    st.header("🤖 AI Recruiter Decision")

    decision = recruiter_decision(
        results[0],
        generate_report(
            extracted[results[0]["candidate"]],
            jd_skills,
            results[0]["recommendation"]
        )
    )

    col1, col2 = st.columns(2)

    with col1:

        st.success(
            f"Decision : {decision['Decision']}"
        )

        st.write(
            f"Interview : {decision['Interview']}"
        )

    with col2:

        st.write(
            f"Strength : {decision['Strength']}"
        )

        st.write(
            f"Weakness : {decision['Weakness']}"
        )

    st.info(
        f"ATS Compatibility : {decision['ATS']:.2f}%"
    )

    st.divider()

    # -------------------------------------------------
    # Ranking Table
    # -------------------------------------------------

    st.header("📊 Ranking Table")

    df = pd.DataFrame(results)

    st.dataframe(
        df,
        width="stretch"
    )

    st.divider()

    # -------------------------------------------------
    # Recruiter Filters
    # -------------------------------------------------

    st.header("🔍 Recruiter Filters")

    recommendation_filter = st.selectbox(
        "Recommendation",
        ["All", "Recommended", "Not Recommended"]
    )

    minimum_score = st.slider(
        "Minimum Final Score",
        0,
        100,
        0
    )

    filtered_df = df.copy()

    if recommendation_filter != "All":

        filtered_df = filtered_df[
            filtered_df["recommendation"] == recommendation_filter
        ]

    filtered_df = filtered_df[
        filtered_df["final_score"] >= minimum_score
    ]

    st.dataframe(
        filtered_df,
        width="stretch"
    )

    st.divider()

    # -------------------------------------------------
    # Candidate Comparison
    # -------------------------------------------------

    st.header("📈 Candidate Comparison")

    comparison_df = candidate_comparison(results)

    st.dataframe(
        comparison_df,
        width="stretch"
    )

    st.divider()

    # -------------------------------------------------
    # Screening History
    # -------------------------------------------------

    st.header("🗂 Previous Screening History")

    history = load_history()

    st.dataframe(
        history,
        width="stretch"
    )

    st.divider()

    # -------------------------------------------------
    # Downloads
    # -------------------------------------------------

    st.header("📥 Download Reports")

    csv = df.to_csv(index=False)

    st.download_button(
        "📄 Download CSV",
        csv,
        "ranked_candidates.csv",
        "text/csv"
    )

    json_data = json.dumps(
        results,
        indent=4
    )

    st.download_button(
        "📄 Download JSON",
        json_data,
        "ranked_candidates.json",
        "application/json"
    )

    with open(pdf_path, "rb") as pdf:

        st.download_button(
            "📄 Download PDF Report",
            pdf,
            "Recruiter_Report.pdf",
            "application/pdf"
        )

    st.success("✅ Analysis Completed Successfully")

    st.divider()

    st.header("📌 Project Summary")

    st.info("""
    ✅ Resume Parsing

    ✅ Resume Information Extraction

    ✅ Job Description Parsing

    ✅ Semantic Similarity

    ✅ Hybrid Candidate Ranking

    ✅ ATS Score

    ✅ Candidate Comparison

    ✅ Recruiter Decision Panel

    ✅ Dashboard Analytics

    ✅ SQLite History

    ✅ CSV Export

    ✅ JSON Export

    ✅ PDF Report

    ✅ Interactive Charts
    """)

    st.caption(
        "AI Resume Screening Agent | Python • Streamlit • NLP • Sentence Transformers • FastAPI"
    )