@echo off
echo Lancement TNessnisa Dashboard...
pip install -r requirements.txt -q
streamlit run app.py
pause
