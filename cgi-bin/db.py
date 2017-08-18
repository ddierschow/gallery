#!/usr/local/bin/python

import datetime, MySQLdb, os


class db:
    def __init__(self, cgibin='../cgi-bin'):
	dbd = eval(open(cgibin + '/.dbconnect').read())
	self.db = MySQLdb.connect(user=dbd['user'], passwd=dbd['passwd'], db=dbd['db'])
	self.cgibin = cgibin

    # user functions

    def login(self, name, passwd):
	if not self.db:
	    return None, None
	cu = self.db.cursor()
	self.log('''select id, privs from user where name = '%s' and passwd = PASSWORD('%s')''' % (name, passwd))
	cu.execute('''select id, privs from user where name = '%s' and passwd = PASSWORD('%s')''' % (name, passwd))
	ret = cu.fetchone()
	if ret:
	    return ret[0], ret[1]
	return None, None

    def changepassword(self, id, passwd):
	if not self.db:
	    return None
	cu = self.db.cursor()
	self.log("""update user set passwd=PASSWORD('%s') where id = '%s'""" % (passwd, id))
	cu.execute("""update user set passwd=PASSWORD('%s') where id = '%s'""" % (passwd, id))
	self.db.commit()
	ret = cu.fetchone()
	if ret:
	    return ret[0]
	return None

    def changeemail(self, id, email):
	if not self.db:
	    return None
	cu = self.db.cursor()
	self.log("""update user set email='%s' where id = '%s'""" % (email, id))
	cu.execute("""update user set email='%s' where id = '%s'""" % (email, id))
	self.db.commit()
	ret = cu.fetchone()
	if ret:
	    return ret[0]
	return None

    def createuser(self, name, passwd, email):
	if not self.db:
	    return None
	cu = self.db.cursor()
	try:
	    self.log('''insert user (name, passwd, privs, email, state) values ('%s', PASSWORD('%s'), '', '%s', 0)''' %(name, passwd, email))
	    cu.execute('''insert user (name, passwd, privs, email, state) values ('%s', PASSWORD('%s'), '', '%s', 0)''' %(name, passwd, email))
	except:
	    return None
	return self.login(name, passwd)

    # generic functions

    def select(self, table, cols=None, where=None, order=None):
	if not self.db:
	    return []
	cu = self.db.cursor()
	if not cols:
	    self.log('desc %s' % table)
	    cu.execute('desc %s' % table)
	    cols = map(lambda x: x[0], cu.fetchall())
	query = '''select %s from %s''' % (','.join(cols), table)
	if where:
	    query += ''' where %s''' % where
	if order:
	    query += ''' order by %s''' % order
	try:
	    #print "<!--",query,"-->"
	    self.log(query)
	    cu.execute(query)
	except:
	    return []
	res = cu.fetchall()
	return map(lambda x: dict(zip(cols, x)), res)

    def update(self, table, values, where=None):
	if not self.db:
	    return []
	cu = self.db.cursor()

	setlist = ','.join(map(lambda x: x + "=" + self.db.literal(str(values[x])), values))

	query = '''update %s set %s''' % (table, setlist)
	if where:
	    query += ''' where %s;''' % where
	#print "<!--",query,"-->"
	try:
	    self.log(query)
	    cu.execute(query)
	except:
	    pass
	return cu.fetchall()

    def updateflag(self, table, values, where=None):
	if not self.db:
	    return []
	cu = self.db.cursor()

	setlist = ','.join(map(lambda x: x + "=" + str(values[x]), values))

	query = '''update %s set %s''' % (table, setlist)
	if where:
	    query += ''' where %s;''' % where
	#print "<!--",query,"-->"
	try:
	    self.log(query)
	    cu.execute(query)
	except:
	    pass
	return cu.fetchall()

    def insert(self, table, inits):
	if not self.db:
	    return []
	cu = self.db.cursor()

	cols = []
	vals = []
	for key in inits:
	    cols.append(key)
	    vals.append(self.db.literal(inits[key]))

	try:
	    query = '''insert into %s (%s) values (%s)''' % (table, ','.join(cols), ','.join(vals))
	    #print "<!--",query,"-->"
	    self.log(query)
	    cu.execute(query)
	except:
	    pass
	return cu.fetchall()

    def remove(self, table, where=None):
	if not self.db:
	    return []
	cu = self.db.cursor()

	query = '''delete from %s''' % table
	if where:
	    query += ''' where %s''' % where
	try:
	    #print "<!--",query,"-->"
	    self.log(query)
	    cu.execute(query)
	except:
	    pass
	return cu.fetchall()

    def log(self, action):
	#print action
	file('logs/database.log', 'a').write('%s %s\n' % (str(datetime.datetime.today()), action))


if __name__ == '__main__':
    pass
