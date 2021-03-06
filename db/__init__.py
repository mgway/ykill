import oursql

from config import db as dbconfig

conn = oursql.connect(host=dbconfig.host, db=dbconfig.database, user=dbconfig.user, passwd=dbconfig.password, autoreconnect=True)

def cursor():
	return conn.cursor(oursql.DictCursor)

def execute(cursor, sql, *values):
	cursor.execute(sql, values)

def query(cursor, sql, *values):
	execute(cursor, sql, *values)
	return cursor.fetchall()

class NoRowsException(Exception): pass
class MultipleRowsException(Exception): pass

def get(cursor, sql, *values):
	execute(cursor, sql, *values)
	result = cursor.fetchone()
	if result is None:
		raise NoRowsException('no rows returned', sql, values)
	if cursor.fetchone() is not None:
		raise MultipleRowsException('multiple results returned', sql, values)
	return result
