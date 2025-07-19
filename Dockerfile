FROM python:3.10-slim-bookworm

# Voorkom interactieve prompts tijdens apt installaties
ENV DEBIAN_FRONTEND=noninteractive

# Werkdir in container
WORKDIR /app

# Upgrade pip en installeer build dependencies, daarna verwijder build dependencies
# Dit zorgt voor een kleinere image door onnodige build tools te verwijderen na installatie.
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    apt-get update && apt-get install -y --no-install-recommends build-essential && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y --auto-remove build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Maak een niet-root gebruiker aan voor betere beveiliging
RUN adduser --system --group appuser

# Kopieer de rest van je code naar de container
# De --chown vlag zorgt ervoor dat de gekopieerde bestanden eigendom worden van de 'appuser'
COPY --chown=appuser:appuser . .

# Schakel over naar de niet-root gebruiker
USER appuser

# Start je applicatie. Pas 'main.py' aan als je een ander startscript hebt.
CMD ["python", "main.py"]

