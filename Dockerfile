FROM public.ecr.aws/x8v8d7g8/mars-base:latest

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src/ ./src/
COPY tests/ ./tests/

RUN pip install --no-cache-dir -e . && \
    pip install --no-cache-dir pytest

CMD ["/bin/bash"]
