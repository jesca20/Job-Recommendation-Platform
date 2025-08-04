import streamlit as st
import plotly.express as px
from collections import Counter
import pandas as pd

def render_analytics_dashboard(jobs_df, resume_skills, applications_df=None):
    st.subheader("📊 Analytics Dashboard")

    # 1️⃣ Match Score Distribution
    if not jobs_df.empty and "score" in jobs_df.columns:
        st.markdown("### 📈 Match Score Distribution")
        fig1 = px.histogram(jobs_df, x="score", nbins=10, title="Match Score Histogram")
        st.plotly_chart(fig1)

    # 2️⃣ Top Skills in Job Market
    if not jobs_df.empty:
        all_tags = []
        for tags in jobs_df['tags']:
            try:
                all_tags.extend(eval(tags))
            except:
                continue
        skill_counts = Counter(all_tags).most_common(10)
        skills_df = pd.DataFrame(skill_counts, columns=["Skill", "Count"])
        st.markdown("### 🔝 Top 10 In-Demand Skills")
        fig2 = px.bar(skills_df, x="Skill", y="Count", title="Top Skills in Job Market")
        st.plotly_chart(fig2)

    # 3️⃣ Resume Skills vs Job Market
    st.markdown("### ✅ Your Skills vs Job Market")
    if resume_skills:
        skill_match_data = {
            "Skill": resume_skills,
            "In Demand?": ["Yes" if skill in dict(skill_counts) else "No" for skill in resume_skills]
        }
        st.table(skill_match_data)

    # 4️⃣ Application Insights
    if applications_df is not None and not applications_df.empty:
        st.markdown("### 📌 Application Insights")
        total_apps = len(applications_df)
        st.metric("Total Applications", total_apps)

        # Applications by Status
        status_counts = applications_df['status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        fig3 = px.pie(status_counts, names='Status', values='Count', title="Applications by Status")
        st.plotly_chart(fig3)

        # Top Companies Applied
        top_companies = applications_df['company'].value_counts().reset_index().head(5)
        top_companies.columns = ['Company', 'Applications']
        fig4 = px.bar(top_companies, x="Company", y="Applications", title="Top Companies You Applied To")
        st.plotly_chart(fig4)

        # Match Score by Status
        if 'score' in applications_df.columns:
            fig5 = px.box(applications_df, x='status', y='score', title="Match Score Distribution by Status")
            st.plotly_chart(fig5)
