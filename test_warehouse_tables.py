from src.warehouse import get_connection

con = get_connection()

print(con.execute("SHOW TABLES").fetchall())

con.close()