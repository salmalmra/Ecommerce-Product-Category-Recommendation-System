# E-commerce Product Category Recommendation System

This project builds a recommender system that suggests product categories for e-commerce users based on similar users’ profiles and preferences.

## Project Overview

The goal of this project is to help an online store understand which product categories are most relevant for each user. The app uses a K-Nearest Neighbors (KNN)-style approach: it finds users with similar demographic and behavioral profiles, then recommends the categories that these “neighbors” like the most.

## Dataset

- 1,000 synthetic users with:
  - Demographics: age, gender, income, location  
  - Behavioral features: purchase frequency, total spending, pages viewed  
  - Preference features: main interests and current favorite product category  
- The dataset is used only for educational and demonstration purposes.
  - Link dataset from Kaagle: https://www.kaggle.com/datasets/kartikeybartwal/ecommerce-product-recommendation-collaborative/data

## Methodology

1. Preprocess the user dataset (encode categorical features and scale numeric features).  
2. Compute similarity between users in the feature space.  
3. For a selected user, find the K most similar users (neighbors).  
4. Aggregate neighbors’ favorite categories and rank them by frequency / proportion to generate recommendations.

## Streamlit App

The Streamlit web app provides an interactive demo of the recommendation system.

**Main features:**

- Sidebar controls  
  - Select a user ID  
  - Choose the number of neighbors (K)  
  - Choose how many top categories to display  

- User profile section  
  - Shows demographic, behavioral, and preference information for the selected user  

- Recommendation section  
  - Displays recommended product categories with neighbor counts and proportions  

- Nearest neighbors section  
  - Lists the most similar users, their key attributes, and similarity scores as an explanation of the recommendations  

## How to Run

1. Clone this repository and move into the project folder:
  git clone https://github.com/your-username/your-repo-name.git
2. (Optional) Create and activate a virtual environment.
3. Install the required packages:
   pip install -r requirements.txt
4. Run the Streamlit app:
   streamlit run app_porto3.py
5. Open the URL shown in the terminal (usually `http://localhost:8501`) in your browser.
