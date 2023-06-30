FROM python:3.9-slim-bullseye

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Run the application:
COPY . app/impossible_tictactoe.py
CMD ["python", "impossible_tictactoe.py"]

