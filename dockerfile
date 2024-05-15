FROM python:3.10.6

WORKDIR /app

COPY requirements.txt ./
# Install gunicorn first, since is not included
RUN pip install gunicorn
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "moonlitBackend.wsgi:application"]