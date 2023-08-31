FROM python:3.10.6-buster
COPY move_recommender /move_recommender
COPY setup.py setup.py
COPY requirements.txt requirements.txt
RUN pip install -e .
CMD uvicorn move_recommender.api.fast:app --host 0.0.0.0 --port $PORT
