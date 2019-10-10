import sys
PATH_ORACLE = 'C:\Oracle\Client\product\12.2.0\client_1\bin'
sys.path.append(PATH_ORACLE)
import cx_Oracle
from Config import mdp,nom

class Connexion():
	def __init__(self):

		dns_tns = cx_Oracle.makedsn('delta',1521,'decinfo')
		chaineConnexion = nom +'/' + mdp + '@' + dns_tns
		
		self.connexion = cx_Oracle.connect(chaineConnexion)
		self.curseur = self.connexion.cursor()
		
	def getMot(self,index):
		query = "SELECT chaine FROM mot WHERE id = :1"
		self.curseur.execute(query,(index))
		
		rep = None
		for rangee in curseur.fetchall():
			rep = rangee
			
		return rep

	def getMots(self):
		query = "SELECT chaine, id FROM mot"
		self.curseur.execute(query)

		return self.curseur.fetchall()

	def getConcurranceMat(self, fenetre):
		#query = "SELECT * FROM Concurrence WHERE fenetre = :1"
		query = "SELECT * FROM Concurrence WHERE fenetre = :fen"
		#self.curseur.execute(query, (fenetre))
		self.curseur.execute(query, {"fen":fenetre})
		return self.curseur.fetchall()

	def getIndex(self,mot):
		query = "SELECT id FROM mot WHERE chaine = :1"
		self.curseur.execute(query,(mot))
		
		rep = None
		for rangee in curseur.fetchall():
			rep = rangee
			
		return rep
		
	def close(self):
		self.connexion.close()
		
	def findIfTablesExist(self):

		self.curseur.execute('select tablespace_name, table_name from user_tables')
		tablesTuples = self.curseur.fetchall()
		motSuccess = False
		ConcurrenceSucces = False

		for tableSpace, tableName in tablesTuples:
			if tableName == 'MOT':
				motSuccess = True
			if tableName == 'CONCURRENCE':
				ConcurrenceSucces = True
		return motSuccess and ConcurrenceSucces

	def buildScript(self, path):

		try:
			self.curseur.execute('Drop Table Concurrence')
			self.curseur.execute('Drop Table Mot')
		except cx_Oracle.DatabaseError:
			print("Drop error - ", "Tables don't seem to exist yet - ", "Building Tables...")
		
		f = open(path)

		full_sql = f.read()
		sql_commands = full_sql.split(';')

		for sql_command in sql_commands:
			if sql_command != '':
				self.curseur.execute(sql_command)

		print("Tables Created")

		
		