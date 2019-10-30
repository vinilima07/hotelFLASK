# Script para recuperacao de senha do PostgreSQL
echo "Script para recuperacao de senha do PostgreSQL"
sudo passwd postgres
su - postgres -c "psql postgres --command \"\\password postgres\""

