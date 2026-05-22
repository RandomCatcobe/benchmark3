FROM python:3.12-slim
WORKDIR /case
# Candidate: typer-optional-list-none-default
# Side: new
# Intended dependency: typer==0.10.0
RUN python -m pip install click==8.1.7 typer==0.10.0
COPY client.py /case/client.py
CMD ["python", "/case/client.py"]
