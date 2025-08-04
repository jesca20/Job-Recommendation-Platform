import os
from pathlib import Path
import streamlit as st
import pandas as pd

from resume_parser.parse_resume import extract_text_from_pdf, extract_skills
from matcher.match_engine import match_jobs
from analytics.analytics import render_analytics_dashboard
from tracker.tracker import save_application, get_applications

# Folders
os.makedirs("data/resumes", exist_ok=True)

st.set_page_config(page_title="Job Recommendation System", layout="wide")
st.title("💼 Job Recommendation System")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📤 Upload Resume", "🎯 Job Matches", "ℹ️ About", "📊 Analytics", "📌 Application Tracker"
])

# ===== TAB 1: Upload Resume =====
with tab1:
    uploaded_file = st.file_uploader("Upload your Resume (PDF)", type="pdf")

    if uploaded_file:
        safe_filename = Path(uploaded_file.name).name
        resume_path = os.path.join("data/resumes", safe_filename)

        with open(resume_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("✅ Resume uploaded successfully!")

        with st.spinner("🔍 Extracting content and skills..."):
            try:
                resume_text = extract_text_from_pdf(resume_path)
                skills = extract_skills(resume_text)
                st.session_state['resume_text'] = resume_text
                st.session_state['skills'] = skills
            except Exception as e:
                st.error(f"❌ Error processing resume: {e}")
                st.stop()

        st.markdown("### 🧠 Extracted Skills:")
        st.write(", ".join(skills))

# ===== TAB 2: Job Matches =====
with tab2:
    st.subheader("🎯 Top Job Matches")

    if 'resume_text' not in st.session_state:
        st.info("Please upload a resume in the first tab to view job matches.")
    else:
        try:
            jobs = pd.read_csv("data/jobs.csv")
            matched = match_jobs(st.session_state['resume_text'], jobs)
        except Exception as e:
            st.error(f"❌ Failed to load or process job data: {e}")
            st.stop()

        if matched.empty:
            st.info("No matching jobs found.")
        else:
            st.success(f"🔎 Found {len(matched)} matching jobs!")

            companies = matched['company'].unique().tolist()
            company_filter = st.selectbox("🔍 Filter by Company", ["All"] + companies)

            if company_filter != "All":
                matched = matched[matched['company'] == company_filter]

            for _, row in matched.iterrows():
                with st.container():
                    st.markdown(f"### {row['title']} at *{row['company']}*")
                    st.markdown(f"🛠️ **Skills:** {', '.join(eval(row['tags']))}")
                    st.markdown(f"[🔗 Apply Here]({row['url']})")

                    status = st.selectbox(f"Update status for {row['title']}",
                                          ["Not Applied", "Applied", "Interviewing", "Offer", "Rejected"],
                                          key=row['url'])

                    if status != "Not Applied":
                        if st.button(f"Save Status for {row['title']}", key="save_"+row['url']):
                            save_application(row, status, row['score'])
                            st.success("Status updated!")
                    st.markdown("---")

# ===== TAB 3: About =====
with tab3:
    st.markdown("""
        ## ℹ️ About This App
        This is a job recommendation system that:
        
        - ✅ Accepts your resume as PDF
        - 🧠 Extracts your skills
        - 🔎 Matches you with job listings
        - 🎯 Ranks jobs based on relevance
        - 📌 Tracks your application progress
        - 📊 Provides insights & analytics
    """)

# ===== TAB 4: Analytics =====
with tab4:
    applications_df = get_applications()
    if 'resume_text' in st.session_state:
        render_analytics_dashboard(matched if 'matched' in locals() else pd.DataFrame(),
                                   st.session_state['skills'],
                                   applications_df)
    else:
        st.info("Upload a resume and view matches to see analytics.")

# ===== TAB 5: Application Tracker =====
with tab5:
    st.subheader("📌 Your Application Progress")
    if applications_df.empty:
        st.info("No applications tracked yet.")
    else:
        status_filter = st.selectbox("Filter by Status", ["All"] + applications_df['status'].unique().tolist())
        if status_filter != "All":
            applications_df = applications_df[applications_df['status'] == status_filter]
        st.dataframe(applications_df)
