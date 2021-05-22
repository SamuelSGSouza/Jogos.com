import MySQLdb

conn = MySQLdb.connect(
    user='root',
    password='admin',
    db='jogoteca',
)
cursor = conn.cursor()
cursor.execute('INSERT VALUES INTO usuario (id, nome, senha'
               'VALUES (%s, %s, %s',
               ('samuel', 'samuel santos', 'trabalhos1'))
conn.commit()
