
# syntax=docker/dockerfile:1.7
FROM python:3.12-slim

# Variáveis úteis para dev
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    FLASK_ENV=development \
    FLASK_DEBUG=1 \
    PORT=5000

# Dependências de sistema mínimas (adicione libs se algum pacote Python nativo exigir)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instala dependências Python
# (mantém cache eficiente: copia só o requirements primeiro)
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Pacotes úteis em dev (hot-reload e debug)
# watchdog -> detecta mudanças de arquivos; debugpy -> depuração remota/VSCode
RUN pip install watchdog==4.* debugpy==1.*

# Copia o código (em dev, pode preferir volume no compose)
COPY . /app

# Exponha a porta do Flask (ajuste se usar outra)
EXPOSE ${PORT}

# CMD para desenvolvimento:
# 1) Se seu app roda pelo app.py (app.run(...)):
#    usa o reloader do Flask por padrão em FLASK_ENV=development.
# 2) Caso precise depurar, descomente o debugpy (ver abaixo).
CMD ["python", "app.py"]

# --- Execução com depuração remota (opcional) ---
# Para usar debugpy, comente o CMD acima e descomente este:
# CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "app"]
# EXPOSE 5678
