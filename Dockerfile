FROM python:3

ADD /register_database_api /app
WORKDIR /app
ENV DATABASE_URL '<database_uri>'
COPY requirments.txt /app
RUN pip install --no-cache-dir -r requirments.txt

CMD [ "python", "./api.py" ]