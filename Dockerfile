FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PLAYWRIGHT_BROWSERS_PATH=/opt/browsers HERMES_HOME=/data/hermes
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates && rm -rf /var/lib/apt/lists/*
# Windows/Linux route: embed upstream Hermes, no Plow Chat/Mac requirement.
# SDK inspected at this exact revision. Live integration validation is still required.
ARG HERMES_SHA=10652c93451fb760435d39d1ce4fd8a9441d18b9
RUN git init /opt/hermes && cd /opt/hermes && git remote add origin https://github.com/NousResearch/hermes-agent.git && git fetch --depth 1 origin "$HERMES_SHA" && git checkout --detach FETCH_HEAD && pip install --no-cache-dir -e .
COPY pyproject.toml README.md LICENSE /app/
COPY src /app/src
RUN pip install --no-cache-dir . && python -m playwright install --with-deps chromium
COPY scripts /app/scripts
COPY examples /app/examples
RUN python scripts/fetch_index_client.py && useradd --create-home --uid 10001 runner && mkdir -p /data/hermes /app/runs && chown -R runner:runner /data /app/runs
USER runner
VOLUME ["/data/hermes", "/app/runs"]
ENTRYPOINT ["proofrunner"]
CMD ["demo"]
