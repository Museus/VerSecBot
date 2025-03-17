FROM python:3.12-slim

# Use Bash as shell
SHELL ["/bin/bash", "-c"]

# silence Dialog TERM not set errors in apt-get install
ENV DEBIAN_FRONTEND=noninteractive

# Set Containerized environment variable for conditional behavior in application
ENV IS_CONTAINER=true

# Install all Python requirements
COPY ./python-requirements.txt ./python-requirements.txt
RUN python3 -m venv venv && \
    source venv/bin/activate && \
    pip install --upgrade pip && \
    pip install --ignore-installed -r python-requirements.txt

# Copy application
COPY ./app /app

# Set context for entrypoint
WORKDIR /app

# Set metadata as specified by https://github.com/opencontainers/image-spec/blob/main/annotations.md
ARG BUILD_TIMESTAMP="unknown"
ARG BUILD_VERSION="unknown"

LABEL org.opencontainers.image.created="${BUILD_TIMESTAMP}"
LABEL org.opencontainers.image.authors="Museus <versecbot@museus.dev>"
LABEL org.opencontainers.image.url=""
LABEL org.opencontainers.image.documentation=""
LABEL org.opencontainers.image.source="https://github.com/Museus/VerSecBot"
LABEL org.opencontainers.image.version="${BUILD_VERSION}"
LABEL org.opencontainers.image.vendor="Museus"
LABEL org.opencontainers.image.title="VerSecBot"
LABEL org.opencontainers.image.description="An extendable Discord Bot to manage common moderation tasks."

ENTRYPOINT ["bash", "-c", "./start.sh"]