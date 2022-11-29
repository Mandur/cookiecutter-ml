FROM python:3.10
COPY main.py main.py
COPY model.pkl model.pkl
COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt
EXPOSE 5000
CMD ["python3","main.py"]