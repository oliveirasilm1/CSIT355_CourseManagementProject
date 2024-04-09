# config.py

# MySQL Configuration (Replace with your database details)
# Change to the same config in docker-compose.yml if using docker compose
class MySQLConfig:
    HOST = '172.29.128.1'   # ip address if remote server; service name (db) if using docker compose
    USER = 'oliveirasilm1'
    PASSWORD = 'csit355silm1'
    DATABASE = 'csit355'
