echo "[INFO] Carregando dados iniciais"
psql     -h localhost -p 5432 -U postgres -d scpi --password -f database.sql
