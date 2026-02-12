FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .

# Install all dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code and set the correct owner.
COPY . .

# Expose the port that the application will run on.
EXPOSE 80

# The command to run the application.
CMD ["python", "app.py"]
