from mysql.connector import MySQLConnection
from config.config import config

_INSERT = 'INSERT'
_UPDATE = 'UPDATE'
_SELECT = 'SELECT'

statements = {_SELECT : 'SELECT {selector} FROM {table} WHERE {keys}',
			  _UPDATE : 'UPDATE {table} SET {updaters} WHERE {keys}',
			  _INSERT : 'INSERT INTO {table}({keys}) VALUES({values})'
			  }

class Mysql():

	def __init__(self):
		self._where = {}
		self.selector = None
		self.updaters = {}
		self.definer = None
		self.values = []

	def where(self, key, value):
		self._where[key] = value
		return self

	def select(self, *args):
		self.definer = _SELECT
		self.selector = args
		return self

	def insert(self, key, value):
		self.definer = _INSERT
		if type(key) != str:
			for k,v in zip(key, value):
				self.updaters[k] = v
		else:
			self.updaters[key] = value
		return self

	def update(self, key, value):
		self.definer = _UPDATE
		if type(key) != str:
			for k,v in zip(key, value):
				self.updaters[k] = v
		else:
			self.updaters[key] = value
		return self

	def query(self):
		self.format()
		_mysql = MySQLConnection(user=config['username'], password = config['password'],
								 host=config['host'],
								 database=config['dbname'])
		cursor = _mysql.cursor(dictionary=True)
		cursor.execute(self.statement, self.values)
		if self.statement.startswith(_SELECT):
			rows = cursor.fetchall()
		else:
			rows = None
		cursor.close()
		self.clean()
		if rows:
			return rows[0]
		else:
			return None

	def format(self):
		if self.definer == _SELECT:
			statement = statements[_SELECT]
			keys = ''
			for k,v in self._where.iteritems():
				keys += '{key}=%s'.format(key=k)
				self.values.append(v)
			if type(self.selector) != str:
				self.selector = ','.join(self.selector)
			self.statement = statement.format(table=config['userTableName'], selector=self.selector, keys=keys)
			self.values = tuple(self.values)
		elif self.definer == _UPDATE:
			statement = statements[_UPDATE]
			updater = ''
			uvalues = []
			keys = ''
			for k,v in self.updaters.iteritems():
				updater += '{key}=%s '.format(key = k)
				uvalues.append(v)
			for k,v in self._where.iteritems():
				keys += '{key}=%s '.format(key = k)
				self.values.append(v)
			self.statement = statement.format(table=config['userTableName'], updaters=updater, keys=keys)
			self.values = tuple(uvalues + self.values)
		elif self.definer == _INSERT:
			statement = statements[_INSERT]
			inserter = ''
			values = []
			_where = ''
			for k,v in self.updaters.iteritems():
				inserter += '%s,' % k
				values.append(v)
			for k,v in self._where.iteritems():
				_where += '%s=%s ' % (k, v)
			self.statement = statement.format(table=config['userTableName'], keys=inserter, values='%s,'*len(values)[:-1])
			self.values = tuple(values)
			print self.statement
			print self.values

	def clean(self):
		self._where = {}
		self.updaters = {}
		self.selector = None
		self.definer = None
		self.values = []

#mysql = Mysql()
#mysql.where('name', 'root').select('id', 'vip').query()
#mysql.where('name', 'root').update('nick', 'root_').update('small_dick', 'big_dick').query()
#mysql.insert('nick', 'root_').insert('username', 'ballsack').query()

