FROM python:3.11-slim
WORKDIR /code
# Install dependencies
RUN pip install flask redis
COPY . .
CMD ["python", "app.py"]