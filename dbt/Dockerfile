FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install dbt and PostgreSQL adapter
RUN pip install --no-cache-dir \
    dbt-core==1.7.4 \
    dbt-postgres==1.7.4 \
    psycopg2-binary

# Set working directory
WORKDIR /opt/dbt

# Copy dbt project files
COPY . /opt/dbt/

# Set dbt environment variables
ENV DBT_PROFILES_DIR=/opt/dbt/profiles
ENV DBT_PROJECT_DIR=/opt/dbt

# Default command
CMD ["dbt", "--help"]
