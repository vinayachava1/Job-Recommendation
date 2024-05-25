import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

if not firebase_admin._apps:
    cred = credentials.Certificate('C:/Users/vinay/OneDrive\Desktop/acm-24-firebase-adminsdk-iwxt4-146368c715.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()

job_data = pd.read_csv('C:/Users/vinay/OneDrive/Documents/updated_yearly_salaries_job_postings_with_companies (1).csv')
job_columns = ['title', 'location', 'min_salary', 'max_salary', 'job_posting_url', 'company']
job_data = job_data[job_columns]

# Handle missing data
job_data.fillna('', inplace=True)
job_data['combined_info'] = job_data['title'] + ' ' + job_data['location'] + ' ' + job_data['company']

# Vectorize the combined information for similarity computation
vectorizer = TfidfVectorizer(stop_words='english')
job_vectors = vectorizer.fit_transform(job_data['combined_info'])

def get_user_liked_jobs(user_id):
    liked_indices = []
    # Reference to the user's liked_jobs subcollection
    jobs_ref = db.collection(u'users').document(user_id).collection(u'liked_jobs')
    jobs = jobs_ref.stream()  # Fetch all job documents in the subcollection

    for job_doc in jobs:
        job_dict = job_doc.to_dict()  # Convert DocumentSnapshot to dictionary
        job_title = job_dict['title']  # Assuming 'title' is the key for job title in Firestore

        # Find indices in the job DataFrame that match the job title from Firestore
        matching_indices = job_data[job_data['title'] == job_title].index.tolist()
        if matching_indices:
            liked_indices.extend(matching_indices)  # Append all matching indices

    if liked_indices:
        return liked_indices
    else:
        print(f"No liked jobs found or user ID {user_id} does not exist.")
        return []
    
def recommend_jobs(user_id, num_recommendations=5):
    liked_indices = get_user_liked_jobs(user_id)
    if not liked_indices:  # No liked jobs or could not fetch liked jobs
        return pd.DataFrame()  # Return an empty DataFrame
   
    job_similarities = np.mean(cosine_similarity(job_vectors[liked_indices], job_vectors), axis=0)
    recommended_indices = np.argsort(job_similarities)[::-1][:num_recommendations + len(liked_indices)]
    final_recommendations = [idx for idx in recommended_indices if idx not in liked_indices][:num_recommendations]
   
    if final_recommendations:  # Check if there are any final recommendations
        return job_data.iloc[final_recommendations]
    else:
        return pd.DataFrame()
    
