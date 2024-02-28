import sqlite3

connection = sqlite3.connect('student.db')

cursor = connection.cursor()

table_info = """
CREATE table STUDENT(NAME VARCHAR(30), CLASS VARCHAR(30),
SECTION VARCHAR(25), MARKS INT);

"""

cursor.execute(table_info)

cursor.execute("INSERT INTO STUDENT VALUES('S', 'AI', 'A', 77)")
cursor.execute("INSERT INTO STUDENT VALUES('K', 'DS', 'B', 78)")
cursor.execute("INSERT INTO STUDENT VALUES('S', 'DS', 'A', 77)")
cursor.execute("INSERT INTO STUDENT VALUES('Z', 'ML', 'B', 79)")

data = cursor.execute("""SELECT * FROM STUDENT""")

for row in data:
    print(row)
    
    
connection.commit()
connection.close()