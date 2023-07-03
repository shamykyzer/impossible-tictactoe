FROM python:3.9-slim-bullseye

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install pygame
RUN /opt/venv/bin/pip install pygame

# Set the working directory to /app
WORKDIR /app

# Copy the application to the Docker image:
COPY app/tictactoe.py .

# Set the entry point to the Python file
CMD ["python", "tictactoe.py"]
