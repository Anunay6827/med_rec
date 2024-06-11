The code uses Flask in the backend and HTML for the website's frontend.
For that, you need to install the libraries: Flask, pandas, scikit-learn, PIL, google's generativeai

Installation commands:
pip install Flask

pip install pandas

pip install scikit-learn

pip install PIL

pip install -U google-generativeai


You also need to put all the necessary files in the same folder.
The necessary files namely: kmeans_model.joblib (preloaded model), medicine.csv

The API key for gemini's ocr is already present in the code.

Change the paths for the preloaded model and dataset in lines: 18,19

Pre-processed ML model at: https://drive.google.com/file/d/1Lr2epKHlHEwoX9tXcrS-6V_sxxawHNnD/view?usp=drive_link
