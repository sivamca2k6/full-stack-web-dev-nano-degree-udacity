import psycopg2

connection = psycopg2.connect('dbname=example user=postgres password=admin')

cursor = connection.cursor()

cursor.execute('DROP TABLE IF EXISTS table2;')

cursor.execute('''
  CREATE TABLE table2 (
    id INTEGER PRIMARY KEY,
    completed BOOLEAN NOT NULL DEFAULT False
  );
''')

cursor.execute('INSERT INTO table2 (id, completed) VALUES (%s, %s);', (1, True))
cursor.execute('INSERT INTO table2 (id, completed) VALUES (%s, %s);', (3, True))
cursor.execute('INSERT INTO table2 (id, completed) VALUES (%s, %s);', (4, True))

SQL = 'INSERT INTO table2 (id, completed) VALUES (%(id)s, %(completed)s);'

data = {
  'id': 2,
  'completed': False
}
cursor.execute(SQL, data)

cursor.execute('select * from table2') # this holdd result set
res = cursor.fetchall() # take all the results from result set
print(res)
res = cursor.fetchone()
print(res) # it return nothing

cursor.execute('select * from table2') # this holdd result set
res = cursor.fetchmany(2) # take all the results from result set
print(res)
res = cursor.fetchone()
print(res) # it return nothing

connection.commit()

connection.close()
cursor.close()