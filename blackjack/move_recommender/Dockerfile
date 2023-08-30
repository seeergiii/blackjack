FROM python:3.10.6
COPY move_recommender /move_recommender
COPY recommender.py /recommender.py
COPY setup.py setup.py
COPY requirements_prod.txt requirements.txt
COPY api.py /api.py

RUN pip install -r requirements.txt
CMD uvicorn move_recommender.api.fast:app --host 0.0.0.0 --port 8000
