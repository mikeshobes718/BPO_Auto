import mysql.connector
from sshtunnel import SSHTunnelForwarder

ssh_host = 'ssh.example.com'
<<<<<<< HEAD
=======
ssh sftp_live_gWGwD@35.184.185.194 -p 55206
>>>>>>> 0980bf6 (Description of your changes)
ssh_username = 'ssh_username'
ssh_password = 'ssh_password'
remote_bind_address = ('127.0.0.1', 3306)
db_user = 'db_username'
db_password = 'db_password'

with SSHTunnelForwarder(
    (ssh_host, 22),
    ssh_username=ssh_username,
    ssh_password=ssh_password,
    remote_bind_address=remote_bind_address
) as tunnel:
    connection = mysql.connector.connect(
        user=db_user,
        password=db_password,
        host='127.0.0.1',
        port=tunnel.local_bind_port,
        database='your_database'
    )

    cursor = connection.cursor()
    cursor.execute("SHOW DATABASES;")
    for db in cursor:
        print(db)

    cursor.close()
    connection.close()
