# Phishing URL Detector - Backend

This is the backend of the Phishing URL Detector webapp. It handles URL classification using a trained machine learning model. It helps detect URLs as **Phishing** or **Legitimate**, and tracks counts/percentages of checks.

## Features
- Classify URLs as phishing or legitimate
- Trained model stored in `model.pkl`
- Text vectorizer stored in `vectorizer.pkl`
- Provides API endpoints for the frontend to use

## Requirements
- Python 3.x
- pip

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Tulasi-c/Phishing-URL-Detection-backend.git
   cd Phishing-URL-Detection-backend

## create and activate virtual environment
python -m venv venv
# On Windows (PowerShell)
venv\Scripts\Activate.ps1
# On Windows (cmd)
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate

## install dependencies
pip install -r requirements.txt

## run the app
python app.py

## folder structure
app.py
model.pkl
vectorizer.pkl
data/
prepare_dataset.py
requirements.txt
train_model.py
raw_urls.csv
model/
venv/
README.md

## API Endpoints

- POST /predict — Accepts JSON or form data with a URL and returns whether it's phishing or legitimate.
