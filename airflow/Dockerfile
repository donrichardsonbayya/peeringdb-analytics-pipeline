FROM apache/airflow:2.9.1

COPY requirements.txt /requirements.txt

# Switch to airflow user (default in official image) and install requirements
RUN pip install --no-cache-dir -r /requirements.txt
