import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_jobs(resume_text, job_df, top_n=10):
    job_df["combined"] = job_df["title"] + " " + job_df["tags"].apply(lambda x: " ".join(eval(x)))
    documents = [resume_text] + job_df["combined"].tolist()
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    cos_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
    job_df["score"] = cos_sim[0]
    return job_df.sort_values(by="score", ascending=False).head(top_n)
