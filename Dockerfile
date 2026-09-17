FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    CLASSICMAC_MCP_TRANSPORT=streamable-http \
    CLASSICMAC_MCP_HOST=0.0.0.0 \
    CLASSICMAC_MCP_PORT=8000 \
    CLASSICMAC_KB_ROOT=/srv/classicmac/kb \
    CLASSICMAC_KB_DB=/srv/classicmac/data/classicmac.sqlite

RUN addgroup --system --gid 10001 classicmac \
    && adduser --system --uid 10001 --ingroup classicmac --home /nonexistent --no-create-home classicmac

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src

RUN python -m pip install --no-cache-dir .

USER classicmac:classicmac

EXPOSE 8000

ENTRYPOINT ["classicmac-mcp"]
CMD ["--transport", "streamable-http", "--host", "0.0.0.0", "--port", "8000"]
