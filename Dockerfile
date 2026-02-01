FROM public.ecr.aws/x8v8d7g8/mars-base:latest

WORKDIR /app

COPY mcp-obsidian/pyproject.toml mcp-obsidian/README.md ./
COPY mcp-obsidian/src/ ./src/
COPY mcp-obsidian/tests/ ./tests/

RUN pip install --no-cache-dir -e . && \
    pip install --no-cache-dir pytest

CMD ["/bin/bash"]
