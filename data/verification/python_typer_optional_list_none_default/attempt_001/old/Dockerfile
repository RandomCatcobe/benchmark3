FROM python:3.12-slim
WORKDIR /case
# Candidate: typer-optional-list-none-default
# Side: old
# Intended dependency: typer==0.9.4
RUN python -m pip install click==8.1.7 typer==0.9.4
COPY client.py /case/client.py
CMD ["python", "/case/client.py"]
