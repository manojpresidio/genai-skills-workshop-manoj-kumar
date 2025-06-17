# Use Python 3.9 as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Copy streamlit config
COPY .streamlit .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY src/ .

# Set environment variables
ENV PORT=8080

# Expose the port that Streamlit will run on
EXPOSE 8080

# Command to run the application
CMD streamlit run chatbot_ui.py --server.port=$PORT --server.address=0.0.0.0
