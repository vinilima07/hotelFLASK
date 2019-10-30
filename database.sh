echo "[INFO] Instalando PostgreSQL"
sudo apt-get install -y postgresql postgresql-contrib
service postgresql start

echo "[INFO] Configurando banco de dados"
read -p "Nome para novo banco de dados: " name
read -p "Usuário PostgreSQL (dica: postgres): " user
read -p "Senha: " password
read -p "Host (dica: localhost): " host
read -p "Port (dica: 5432): " port

cat <<- EOF > settings.json
{
    "database": {
        "name"     : "$name",
        "user"     : "$user",
        "password" : "$password",
        "host"     : "$host",
        "port"     : "$port"
    }
}
EOF

echo "[INFO] Criando banco de dados"
createdb -h $host -p $port -U $user $name --password

echo "[INFO] Carregando dados iniciais"
psql     -h $host -p $port -U $user -d $name --password -f database.sql
