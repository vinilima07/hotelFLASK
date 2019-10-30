echo "[INFO] Iniciando servidor WEB"
source venv/bin/activate
gunicorn app:app --reload
