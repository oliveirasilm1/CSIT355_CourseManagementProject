# config.py

# MySQL Configuration (Replace with your database details)
# Change to the same config in docker-compose.yml if using docker compose
class MySQLConfig:
    HOST = '192.168.1.156'   # ip address if remote server; service name (db) if using docker compose
    USER = 'oliveirasilm1'
    PASSWORD = 'csit355silm1'
    DATABASE = 'csit355'
