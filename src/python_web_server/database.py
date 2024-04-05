import psycopg2


# connect to the db
con = psycopg2.connect(
    host="localhost",
    database="db01",
    user="postgres",
    password="posgtres",
)

# do stuff to the db
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS students (name TEXT, age INT);")
cur.execute("INSERT INTO students (name, age) VALUES ('Alice', 20);")

# commit the changes
con.commit()

cur.execute("SELECT * FROM students;")
rows = cur.fetchall()
for row in rows:
    print(row)


# close the cursor
cur.close()

# close the connection
con.close()
