ARG PYTHON_VERSION
FROM python:3.11

# Set working directory
WORKDIR /app

COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Set environment variable for debug mode
ENV DEBUG_MODE=true

# Install ptvsd if DEBUG_MODE is true
RUN if [ "$DEBUG_MODE" = "true" ]; then pip install ptvsd ; fi

# Expose port for backend service
EXPOSE 777

# Default command
CMD ["uvicorn", "ui.backend.api:app", "--host", "0.0.0.0", "--port", "8099", "--reload"]
