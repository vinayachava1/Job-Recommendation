# Job Recommendation System

## Overview
This Python-based job recommendation system utilizes machine learning techniques to recommend job postings to users based on their previously liked jobs. The system uses a TF-IDF Vectorizer for natural language processing and cosine similarity for measuring the similarity between job postings. The data for job postings is sourced from a CSV file and user-specific data is managed using Firebase Firestore.

## System Requirements
- Python 3.8 or higher
- Pandas
- NumPy
- scikit-learn
- Firebase Admin SDK
- Internet connection to access Firestore database

## Setup Instructions
1. **Install Python Libraries:**

2. **Firebase Configuration:**
- Download your Firebase Admin SDK JSON file.
- Ensure the path in the code matches the location of your JSON file.

3. **Data Files:**
- Ensure the job postings CSV file is available at the specified path in the code.

4. **Environment Setup:**
- It's recommended to set up a virtual environment to manage dependencies:
  ```
  python -m venv env
  env\Scripts\activate  # For Windows
  source env/bin/activate  # For Unix or MacOS
  ```

## Usage
- **Running the Script:**
Execute the main script using Python:

- **Functionality:**
- `get_user_liked_jobs(user_id)`: Fetches the indices of jobs liked by a specific user.
- `recommend_jobs(user_id, num_recommendations=5)`: Generates job recommendations for the user.

- **Customizing Recommendations:**
Modify `num_recommendations` parameter in the `recommend_jobs` function to change the number of job recommendations returned.

## Note
Ensure the Firestore rules allow read/write access as per your application's requirements. Proper error handling and security configurations are crucial for production deployment.
