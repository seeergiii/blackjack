FROM python:3.10.6-buster
COPY move_recommender /move_recommender
COPY setup.py setup.py
<<<<<<< HEAD
COPY requirements.txt requirements.txt
RUN pip install -e .
CMD uvicorn move_recommender.api.fast:app --host 0.0.0.0 --port $PORT
=======
COPY requirements_prod.txt requirements.txt
COPY api.py /api.py

RUN pip install -r requirements.txt
CMD uvicorn move_recommender.api.fast:app --host 0.0.0.0 --port 8000
>>>>>>> b0bcf309af58fc15775f0128d977222c7ea05278
