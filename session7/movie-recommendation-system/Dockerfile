FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    MPLCONFIGDIR=/tmp \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

WORKDIR /app

# Only what the app needs (no jupyter/pytest)
RUN pip install --upgrade pip && pip install \
    "pandas>=2.0.0" "numpy>=1.24.0" "scipy>=1.10.0" "scikit-learn>=1.3.0" \
    "matplotlib>=3.7.0" "seaborn>=0.12.0" "joblib>=1.3.0" "streamlit>=1.30.0" pillow

COPY . .

# Build the model inside the image so it matches the library versions installed here
RUN rm -f models/recommender_model.joblib && python -m src.model_training

RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8501/_stcore/health')" || exit 1

CMD ["streamlit", "run", "app/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
