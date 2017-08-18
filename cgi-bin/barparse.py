#!/usr/local/bin/python

import os, re

#non_bar_re = re.compile (r'\s*([^|]*?)\s*(?:\||$)')
#def BarList(str):
#    return non_bar_re.findall(str)


class ArgList:
    def __init__(self, line):
	self.llist = []
	line = line.strip( )
	if len( line ) and line[0] != '#':
	    self.llist = map(lambda x: x.strip(), line.split('|'))
	self.curarg = 0

    def Clean(self):
	self.llist = map(lambda x: x.strip(), self.llist)

    def Args(self):
	return len(self.llist)

    def GetArg(self, defval=None, start=-1):
	ret = defval
	if start >= 0:
	    self.curarg = start
	if self.curarg < self.Args():
	    nval = self.llist[self.curarg].strip()
	    if nval:
		ret = nval
	    self.curarg += 1
	return ret

    def GetArgs( self, defvals, start=-1):
	ret = ()
	if start >= 0:
	    self.curarg = start
	for val in defvals:
	    ret = ret + ( self.GetArg( val ), )
	return ret

    def __len__(self):
	return len(self.llist)

    def Rewind(self):
	self.curarg = 0

    def __getitem__(self, s):
	return self.llist.__getitem__(s)

    def __str__(self):
	return str(self.llist)


class BarFile:
    def __init__(self, fname):
	self.filename = fname
	try:
	    self.handle = file(fname)
	except IOError:
	    print FormatHead()
	    print "<!--",fname,"is on crack. -->"
	    print """I'm sorry, that page was not found.  Please use your "BACK" button or try something else."""
	    print FormatTail()
	    sys.exit(1)
	self.srcstat = os.fstat(self.handle.fileno())
	self.ignoreoverride = False
	self.dats = {}
	self.Parse()

    def __getitem__(self, arg):
	return self.__dict__[arg]

    def get(self, arg, val=None):
	return self.__dict__.get(arg, val)

    def Read(self):
	return self.ReadFile(self.handle)

    def ReadLine(self, line):
	llist = ArgList(line)
	llist.Clean()
	return llist

    def ReadFile(self, dbh):
	db = dbh.readlines()
	dblist = []
	ignoreflag = False
	for line in db:
	    if line[0] == '#':
		continue
	    llist = self.ReadLine(line)
	    if not llist:
		continue
	    cmd = llist.GetArg()
	    if cmd == 'ignore':
		ignoreflag = not self.ignoreoverride and int(llist.GetArg())
	    elif cmd == 'if':
		ignoreflag = not eval(llist.GetArg())
	    elif cmd == 'endif':
		ignoreflag = False
	    elif ignoreflag:
		continue
	    elif cmd == 'include':
		dblist.extend( self.ReadInclude( llist.GetArg() ) )
	    else:
		llist.Rewind()
		dblist.append( llist )
	return dblist

    def ReadInclude(self, datname):
	try:
	    dbf = file(datname)
	except IOError:
	    return []
	return self.ReadFile(dbf)
	fst = os.fstat(dbf.fileno())
	db = dbf.readlines()
	dblist = []
	for line in db:
	    if line[0] == '#':
		continue
	    llist = self.ReadLine(line)
	    if not llist:
		continue
	    cmd = llist.GetArg()
	    if cmd == 'include':
		dblist.extend( self.ReadInclude( llist.GetArg() ) )
	    else:
		llist.Rewind()
		dblist.append( llist )
	return dblist

    def Peek(self, datname):
	line = self.handle.readline()
	llist = self.ReadLine(line)
	return llist

    def Parse(self):
	self.dblist = []
	rawlist = self.Read()
	for e in rawlist:
	    ent = self.ParseCommand(e)
	    if ent:
		self.dblist.append(ent)
	self.ParseEnd()
	return self.dblist

    def ParseCommand(self, llist):
	cmd = llist.GetArg()
	ent = self.ParseField(self.__class__, str(cmd), llist)
	if ent == None:
	    ent = self.ParseByData(llist)
	if ent == None:
	    ent = self.ParseElse(llist)
	return ent

    def ParseData(self, llist, cmdname="cmd"):
	if llist[0] in self.dats:
	    return dict(zip([cmdname] + self.dats[llist[0]][0], llist.llist))
	return None

    def ParseByData(self, llist):
	return self.ParseData(llist)

    def ParseElse(self, llist):
	return None

    def ParseField(self, pclass, cmd, llist):
	if "Parse_"+cmd in pclass.__dict__:
	    ret = pclass.__dict__['Parse_' + cmd](self, llist)
	    if ret != None:
		return ret
	    return False
	if pclass.__bases__:
	    return pclass.__bases__[0].ParseField(self, pclass.__bases__[0], cmd, llist)
	return None

    def Parse_data(self, llist):
	key = llist.GetArg()
	fld = llist.GetArg()
	typ = llist.GetArg('')
	self.dats[key] = (fld.split(','), typ)

    def ParseEnd(self):
	pass


class RawBarFile(BarFile):
    def __init__(self, fname):
	BarFile.__init__(self, fname)

    def ReadLine(self, line):
	llist = ArgList(line)
	return llist


class SimpleFile(BarFile):
    def __init__(self, fname):
	self.dblist = []
	BarFile.__init__(self, fname)

    def __iter__(self):
	return self.dblist.__iter__()

    def ParseElse(self, llist):
	self.dblist.append(llist)


if __name__ == '__main__':
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
