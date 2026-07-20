import os
import sys
import json

# Project Root
# -------------------------------------------------
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
import streamlit as st
import pandas as pd
from reports.pdf_report import generate_pdf
from visualization.ats_gauge import ats_gauge
from visualization.radar_chart import skill_radar
from analysis.decision_panel import recruiter_decision
from analysis.candidate_comparison import candidate_comparison
from database.database import (
    create_table,
    save_results,
    load_history,
)

# -------------------------------------------------
# Imports
# -------------------------------------------------
from file_utils import save_uploaded_file

from resume_parser.resume_parser import parse_resume_folder
from extraction.extractor import extract_resume_data
from similarity.ranking import rank_candidates
from visualization.pie_chart import recommendation_chart
from exports.csv_export import export_csv
from exports.json_export import export_json

from analysis.recruiter_report import generate_report
from visualization.charts import score_chart

# -------------------------------------------------
# Streamlit Page
# -------------------------------------------------
st.set_page_config(
    page_title="AI Resume Screening Agent",
    page_icon="🤖",
    layout="wide",
)
create_table()
# =====================================
# Sidebar
# =====================================

st.sidebar.title("🤖 AI Resume Screening")

st.sidebar.markdown("---")

st.sidebar.info("""
### Features

✅ Resume Parsing

✅ Skill Extraction

✅ Semantic Similarity

✅ ATS Score

✅ Resume Ranking

✅ Recruiter Analysis

✅ CSV Export

✅ JSON Export
""")

st.sidebar.markdown("---")

st.sidebar.success("Version 1.0")

st.sidebar.caption("Developed using Python, NLP & Machine Learning")

st.title("🤖 AI Resume Screening Agent")

st.markdown("""
Upload multiple resumes and compare them against a Job Description using
AI-powered semantic similarity and hybrid scoring.
""")

st.divider()

# -------------------------------------------------
# Upload Section
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

    # ---------------- Validation ----------------

    if not uploaded_files:
        st.error("Please upload resumes.")
        st.stop()

    if job_description.strip() == "":
        st.error("Please enter Job Description.")
        st.stop()

    upload_folder = "data/uploads"

    os.makedirs(upload_folder, exist_ok=True)

    # Delete old resumes
    for file in os.listdir(upload_folder):
        path = os.path.join(upload_folder, file)

        if os.path.isfile(path):
            try:
                os.remove(path)
            except:
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

        st.write("Number of resumes found:", len(resumes))

        if len(resumes) == 0:
            st.error("No resumes found.")
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
    # Export Files
    # -------------------------------------------------

    export_csv(results)
    export_json(results)
    pdf_path = generate_pdf(results)
    # -------------------------------------------------
    # Dashboard Statistics
    # -------------------------------------------------

    total_candidates = len(results)

    best_score = max(candidate["final_score"] for candidate in results)

    average_score = round(
        sum(candidate["final_score"] for candidate in results) / total_candidates,
        2
    )

    recommended = sum(
        1
        for candidate in results
        if candidate["recommendation"] == "Recommended"
    )

    st.header("📊 Dashboard Statistics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Candidates",
        total_candidates,
    )

    col2.metric(
        "Best Score",
        f"{best_score:.2f}",
    )

    col3.metric(
        "Average Score",
        f"{average_score:.2f}",
    )

    col4.metric(
        "Recommended",
        recommended,
    )

    st.divider()
    # -------------------------------------------------
    # Recruiter Dashboard
    # -------------------------------------------------

    st.header("📊 Recruiter Dashboard")

    total_candidates = len(results)

    average_score = round(
        sum(c["final_score"] for c in results) / total_candidates,
        2
    )

    highest_score = max(
        c["final_score"] for c in results
    )

    lowest_score = min(
        c["final_score"] for c in results
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
        "Highest Score",
        highest_score
    )

    col3.metric(
        "Average Score",
        average_score
    )

    col4.metric(
        "Recommended",
        recommended
    )

    st.divider()
    # -------------------------------------------------
    # Best Candidate
    # -------------------------------------------------

    winner = results[0]
    st.header("ATS Score")

    gauge = ats_gauge(
        winner["final_score"]
    )
    if winner["final_score"] >= 85:
        st.success("Excellent ATS Match")

    elif winner["final_score"] >= 70:
        st.info("Good ATS Match")

    elif winner["final_score"] >= 50:
        st.warning("Average ATS Match")

    else:
        st.error("Low ATS Match")

    st.plotly_chart(
        gauge,
        use_container_width=True
    )

    st.success("🏆 Best Candidate")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Candidate",
        winner["candidate"]
    )

    col2.metric(
        "Final Score",
        winner["final_score"]
    )

    col3.metric(
        "Recommendation",
        winner["recommendation"]
    )

    st.divider()

    # -------------------------------------------------
    # Score Chart
    # -------------------------------------------------

    chart = score_chart(results)

    st.plotly_chart(
        chart,
        use_container_width=True
    )

    st.divider()

    chart = score_chart(results)

    st.plotly_chart(
        chart,
        use_container_width=True
    )

    # -------------------------------------------------
    # Recruiter Report
    # -------------------------------------------------

    st.header("Candidate Analysis")

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
    search = st.text_input(
    "🔍 Search Candidate"
    )
    filtered = results

    if search:
        filtered = [
            c for c in results
            if search.lower() in c["candidate"].lower()
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
                        file_name=candidate["candidate"]
                    )
            except:
                st.warning("Resume not found.")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(f"## 👤 {candidate['candidate']}")
            st.write("Semantic Score:", candidate["semantic_score"])
            st.write("Semantic Score")
            st.progress(candidate["semantic_score"] / 100)
            st.write(f"{candidate['semantic_score']:.2f}")
            st.write("Final Score:", candidate["final_score"])
            st.write("Recommendation:", candidate["recommendation"])
            st.write("### ATS Match")

            st.progress(candidate["final_score"] / 100)

            st.write(
                f"ATS Match Percentage: {candidate['final_score']:.2f}%"
            )
            st.write("Final Score:", candidate["final_score"])

            st.write("### ATS Match")

            st.progress(candidate["final_score"] / 100)

            st.write(
                f"ATS Match Percentage: {candidate['final_score']:.2f}%"
            )

            # ---------- ADD STEP 3 HERE ----------
            if candidate["final_score"] >= 90:
                strength = "🟢 Excellent Resume"

            elif candidate["final_score"] >= 75:
                strength = "🟢 Strong Resume"

            elif candidate["final_score"] >= 60:
                strength = "🟡 Average Resume"

            else:
                strength = "🔴 Needs Improvement"

            st.success(strength)
# ------------------------------------

        with col2:

            report = generate_report(
                extracted[candidate["candidate"]],
                jd_skills,
                candidate["recommendation"],
            )
            decision = recruiter_decision(
                candidate,
                report
            )
            radar = skill_radar(
                extracted[candidate["candidate"]]["skills"],
                jd_skills
            )

            st.plotly_chart(
                radar,
                use_container_width=True
            )

            st.write("### Recruiter Report")

            st.success(
                f"Matched Skills: {report['Matched Skills']}"
            )

            st.warning(
                f"Missing Skills: {report['Missing Skills']}"
            )

            st.info(
                f"Match Percentage: {report['Match Percentage']}%"
            )

        st.divider()
    st.subheader("🤖 AI Recruiter Decision")

    col1, col2 = st.columns(2)

    with col1:
        st.success(f"Decision: {decision['Decision']}")
        st.write(f"Interview: {decision['Interview']}")

    with col2:
        st.write(f"Strengths: {decision['Strength']}")
        st.write(f"Weaknesses: {decision['Weakness']}")

    st.info(f"ATS Compatibility: {decision['ATS']:.2f}%")
    # -------------------------------------------------
    # Ranking Table
    # -------------------------------------------------

    st.header("Ranking Table")
    # Create DataFrame
    df = pd.DataFrame(results)
        # Number of candidates
    st.info(f"Candidates Found: {len(df)}")

    # Display table
    st.dataframe(
        df,
        use_container_width=True
    )
    st.header("Recruiter Filters")

    search_name = st.text_input(
        "Search Candidate"
    )

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

    sort_order = st.selectbox(
        "Sort Final Score",
        ["Highest First", "Lowest First"]
    )
    # Search Candidate
    if search_name:

        df = df[
            df["candidate"].str.contains(
                search_name,
                case=False
            )
        ]

    # Recommendation Filter
    if recommendation_filter != "All":

        df = df[
            df["recommendation"] == recommendation_filter
        ]

    # Minimum Score Filter
    df = df[
        df["final_score"] >= minimum_score
    ]

    # Sort
    ascending = sort_order == "Lowest First"

    df = df.sort_values(
        by="final_score",
        ascending=ascending
    )



    comparison_df = candidate_comparison(results)

    st.dataframe(
        comparison_df,
        use_container_width=True,
    )
    top = comparison_df.iloc[0]

    st.success(
        f"""
    🏆 Top Candidate

    Name: {top['candidate']}

    Final Score: {top['final_score']}

    Recommendation: {top['recommendation']}
    """
    )
    st.subheader("Recommendation Distribution")

    recommended = len(
        comparison_df[
            comparison_df["recommendation"] == "Recommended"
        ]
    )

    not_recommended = len(comparison_df) - recommended

    st.write("Recommended:", recommended)
    st.write("Not Recommended:", not_recommended)
    df = pd.DataFrame(results)
    st.subheader("Average Scores")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Avg Semantic",
        round(comparison_df["semantic_score"].mean(), 2)
    )

    col2.metric(
        "Avg Skill",
        round(comparison_df["skill_score"].mean(), 2)
    )

    col3.metric(
        "Avg Final",
        round(comparison_df["final_score"].mean(), 2)
    )

    st.dataframe(
        df,
        use_container_width=True
    )
    st.header("Previous Screening History")

    history = load_history()

    st.dataframe(
        history,
        use_container_width=True,
    )
    # -------------------------------------------------
    # Downloads
    # -------------------------------------------------

    st.header("Download Results")

    csv = df.to_csv(index=False)

    st.download_button(
        "📥 Download CSV",
        csv,
        "ranked_candidates.csv",
        "text/csv",
    )

    json_data = json.dumps(
        results,
        indent=4,
    )

    st.download_button(
        "📥 Download JSON",
        json_data,
        "ranked_candidates.json",
        "application/json",
    )
    with open(pdf_path, "rb") as pdf:
        st.download_button(
        label="📄 Download PDF Report",
        data=pdf,
        file_name="Recruiter_Report.pdf",
        mime="application/pdf"
    )

    st.success("✅ Analysis Completed Successfully")

    st.markdown("---")

    st.caption(
        "AI Resume Screening Agent | Built using Python • Streamlit • NLP • Sentence Transformers • FastAPI"
    )
    # -------------------------------
    # Project Summary
    # -------------------------------

    st.divider()

    st.header("📌 Project Summary")

    st.info("""
    This AI Resume Screening Agent performs:

    ✅ Resume Parsing (PDF & DOCX)

    ✅ Information Extraction

    ✅ Job Description Skill Extraction

    ✅ Semantic Similarity using Sentence Transformers

    ✅ Hybrid Candidate Scoring

    ✅ Resume Ranking

    ✅ Recruiter Analysis

    ✅ Interactive Dashboard

    ✅ CSV & JSON Export

    ✅ FastAPI Backend Support
    """)

    st.caption("Developed using Python • Streamlit • FastAPI • Sentence Transformers • Plotly")