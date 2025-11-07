# Choose an appropriate Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
# Ensure this requirements.txt is in your GitHub repo and lists streamlit, requests, python-dotenv
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code (app.py and any other needed files) into the container
COPY . .

# Expose the port Streamlit runs on (default is 8501)
EXPOSE 8501

# Command to run your Streamlit application
# Ensure HUGGING_FACE_API_TOKEN is set as a secret in your HF Space settings
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]