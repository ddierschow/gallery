#!/usr/local/bin/python

import cgi, copy, getopt, glob, os, os.path, stat, sys, time
if os.getenv('REQUEST_METHOD'):
    import cgitb; cgitb.enable()
import barparse
import CryptCookie
import styles

os.environ['PYTHON_EGG_CACHE'] = '/var/tmp'

#---- global vars -------------------------------------------------------

#from form
cgiform = None
form = {}
pagename = ''
simple = 0

#from file
fmttype = 'main'
other = ()
picdir = ''
shownstyles = {}
pagetitle = ''
tail = {}
title = ''

#from script
docroot = None
artdir = 'gfx'

pagestyles = styles.StyleSet() # hack until we finish converting stuff

#from config
dbuser = "none"
dbpass = "none"
dbname = "none"
artdir = "pics"
cgibin = "../cgi-bin"
htdocs = "../htdocs"

#---- docroot -----------------------------------------------------------

def DocRoot():
    global docroot
    config = dict(map(lambda x: [x[0], dict(map(lambda y: y.split(','), x[1:]))], map(lambda x: x.strip().split('|'), open('.config').readlines())))
    server = '.'.join(os.getenv('SERVER_NAME', 'default.ent').split('.')[-2:])
    globals().update(config[server])

    if os.environ.has_key('DOCUMENT_ROOT'):
	os.chdir(os.environ['DOCUMENT_ROOT'])
    elif docroot:
	os.chdir(docroot)
    else:
	os.chdir(htdocs)
    docroot = os.getcwd()

#---- cookies and authentication ----------------------------------------

def GetCookies():
    cook = CryptCookie.GetCookies()
    if not cook:
	return {'id' : 10,'ip' : '127.0.0.1','pr' : 'vuma'}
	return {}
    return dict(zip(['id','ip','pr'], cook['id'].value.split(';')))


def IsAllowed(priv):
    cook = GetCookies()
    for p in priv:
	if p in cook.get('pr', ''):
	    return True
    return False


def Restrict(priv):
    if not IsAllowed(priv):
	print '<meta http-equiv="refresh" content="0;url=..">'
	sys.exit(0)

#---- html formatting ---------------------------------------------------

def FormatHtml(cookie=None):
    ostr = 'Content-Type: text/html\n'
    if cookie:
	ostr += cookie.output() + '\n'
    else:
	incookie = CryptCookie.GetCookies()
	if not incookie:
	    pass
	elif not 'id' in incookie:
	    pass
	elif not ';' in incookie['id'].value:
	    incookie['id']['expires'] = -1
	    ostr += incookie.output() + '\n'
	    del os.environ['HTTP_COOKIE']
	elif incookie['id'].value.split(';')[1] != os.environ['REMOTE_ADDR']:
	    incookie['id']['expires'] = -1
	    ostr += incookie.output() + '\n'
	    del os.environ['HTTP_COOKIE']
    ostr = ostr + '\n'
    return ostr


def FormatHead(withcolors=True, extra='', stylelist=pagestyles, also={}):
    global pagetitle, title, shownstyles
    shownstyles = stylelist
    ostr = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">\n<html>\n<head><title>%s</title>\n' % pagetitle
    ostr += '<style type="text/css">\n'
    ostr += stylelist.Format(simple)
    ostr += "</style>\n"
    if extra:
	ostr += extra + '\n'
    ostr += '</head>\n<body%s>\n' % Also(also)
    if title:
	ostr += '\n<div class="title">' + title + '</div>'
    return ostr


def FormatTableStart(also={}):
    also['class'] = also.get('class', shownstyles.FindName('table', simple))
    return '<table%s>' % AlsoSpan(also)


def FormatTableEnd():
    return "</table>"


def FormatRowStart(also={}):
    return " <tr%s>" % AlsoSpan(also)


def FormatRowEnd():
    return " </tr>"


def FormatCell(col, content="&nbsp;", hdr=False, also={}, large=False):
    ostr = FormatCellStart(col, hdr, also, large) + '\n'
    ostr +=  "   %s\n" % content
    ostr += FormatCellEnd(col, hdr, large)
    return ostr


celltype = {False : "td", True : "th"}
def FormatCellStart(col=0, hdr=False, also={}, large=False):
    cellclass = {False : "cell", True : "hcell"}
    nalso = copy.deepcopy(also)
    cname = cellclass[hdr]
    if (".%s_%s" % (cname, col)) in shownstyles:
	cname = "%s_%s" % (cname, col)
    elif '.' + cname not in shownstyles:
	cname = 'table'
    nalso['class'] = nalso.get('class', shownstyles.FindName(cname, simple))
    return '  <%s%s>' % (celltype[hdr], AlsoSpan(nalso))


def FormatCellEnd(col=0, hdr=False, large=False):
    ostr = '  </' + celltype[hdr] + '>\n'
    if large:
	ostr += " </tr>"
    return ostr


def FormatSection(fn, content, also={}):
    global simple
    if simple:
	return ' <th' + Also(also) + '>' + content + '</th>'

    also['class'] = also.get('class', shownstyles.FindName('section', simple))
    ostr = FormatRowStart() + '  <th%s>' % AlsoSpan(also)
    if fn:
	strimg = FmtOptImg(fn, suffix='gif')
	if len(strimg) > 6:
	    ostr += strimg + '<br>'
    ostr += content + '</th>' + FormatRowEnd()
    return ostr


def FormatSubsection(fn, content, col, also={}, large=False, nstyle=None):
    global shownstyles
    cname = "section"
    if ("subsection_%s" % col) in shownstyles:
	cname = "subsection_%s" % col
    elif "subsection" in shownstyles:
	cname = "subsection"
    calso = {'class' : cname}
    if isinstance(nstyle, styles.Style):
	calso['style'] = nstyle.Fields()
    elif nstyle:
	calso['style'] = nstyle
    ostr = FormatRowStart() + '  <th ' + Also(calso) + '>'
    if large:
	ostr += FmtOptImg(fn, suffix='gif') + content + '</th>\n'
    else:
	ostr += FmtOptImg(fn, suffix='gif') + '</th>\n'
	ostr += '  <th' + AlsoSpan(also, calso) + '>%s</th>\n' % content
	ostr += '  <th' + Also(calso) + '>&nbsp;</th>\n'
    ostr += FormatRowEnd()
    return ostr


def FormatTail():
    global body, simple, tail
    ostr = "<p>\n"
    if not simple and tail.get('printable'):
	ostr += '''<a href="%s&simple=1">This list is also available in a more printable form.</a><p>\n''' % (os.environ['REQUEST_URI'])
    if tail.get('vary'):
    	ostr += "Actual model color and decoration probably vary from picture as shown.<p>\n"
    if tail.get('effort'):
    	ostr += "Every effort has been made to make this as accurate as possible.  If you have corrections, please contact us.<p>\n"
    if tail.get('contact'):
	ostr += 'This page is maintained by members of BAMCA.\n'
	ostr += '<a href="../pages/faq.html">See here for information on contacting us.</a><p>\n'
    if tail.get('disclaimer'):
	ostr += '''<hr>
BAMCA is a private club and is not affiliated with Tyco Toys, Inc. or Matchbox
Toys (USA) Ltd.  Matchbox and the Matchbox logo are registered trademarks
of Matchbox International Ltd. and are used with permission.
<hr><p>
'''
    st = tail.get('stat')
    if st:
	ostr += time.strftime('\n<font size=-1><i>Last updated %A, %d %B %Y at %I:%M:%S %p %Z.</i></font>', time.localtime(st[stat.ST_MTIME])) + '\n'
    ostr += "</body>\n</html>"
    return ostr


def FormatMarkup(cmd, args):
    carg = {}
    for arg in reversed(args):
	carg.update(arg)
    return '<' + cmd + Also(args) + '>'


def FormatLink(url, txt, nstyle=None, also={}):
    ostr = ''
    if nstyle:
	ostr += '<span' + Also(nstyle) + '>'
    if not url:
	ostr += txt
    elif not txt:
	ostr += '<a href="%s"%s>%s</a>' % (url, Also(also), url)
    else:
	ostr += '<a href="%s"%s>%s</a>' % (url, Also(also), txt)
    if nstyle:
	ostr += '</span>'
    return ostr


def DictMerge(d1, d2):
    d = copy.deepcopy(d1)
    d.update(d2)
    return d


def AlsoSpan(also={}, style={}):
    ostr = ''
    for tag in ['rowspan', 'colspan', 'class', 'style']:
	if also.get(tag, style.get(tag)):
	    ostr = ostr + ' %s="%s"' % (tag, also.get(tag, style.get(tag)))
    return ostr


def Also(also={}, style={}):
    nalso = DictMerge(style, also)
    ostr = ''
    for tag in nalso:
	if nalso.get(tag):
	    ostr = ostr + ' %s="%s"' % (tag, nalso[tag])
    return ostr


def Escape(txt):
    badlist = [
	('%', '%25'),
	('!', '%21'),
	('*', '%2A'),
	("'", '%27'),
	('(', '%28'),
	(')', '%29'),
	(';', '%3B'),
	(':', '%3A'),
	('@', '%40'),
	('&', '%26'),
	('=', '%3D'),
	('+', '%2B'),
	('$', '%24'),
	(',', '%2C'),
	('/', '%2F'),
	('?', '%3F'),
	('#', '%23'),
	('[', '%5B'),
	(']', '%5D'),
	(' ', '%20'),
    ]
    for b in badlist:
	txt = txt.replace(b[0], b[1])
    return txt


def Literal(istr):
    if not istr:
	return ''
    htmlescapes = {
	'&' : '&amp;',
	'"' : '&quot;',
	'<' : '&lt;',
	'>' : '&gt;',
    }
    ostr = ''
    for c in istr:
	ostr += htmlescapes.get(c, c)
    return ostr

#---- forms -------------------------------------------------------------

def ReadForm(fields={}):
    DocRoot()
    global cgiform, form, pagename, simple
    form = copy.deepcopy(fields)
    if os.environ.has_key('DOCUMENT_ROOT'):
	cgiform = cgi.FieldStorage()
	for field in cgiform.keys():
	    if type(cgiform[field]) == list:
		form.setdefault(field, [])
		for elem in cgiform[field]:
		    form[field].append(elem.value)
	    elif type(fields.get(field)) == list:
		form[field] = [cgiform[field].value]
	    else:
		form[field] = cgiform[field].value

    else:
	switches = options = ""
	switch = {}
	opts = files = []
	coptions = switches
	if options:
	    coptions += ':'.join(list(options)) + ':'

	try: # get command line
	    opts, files = getopt.getopt(sys.argv[1:], coptions)
	except getopt.GetoptError:
	    return

	for opt in switches:
	    switch[opt] = False
	for opt in options:
	    switch[opt] = []

	for opt in opts:
	    if opt[0][1] in options:
		switch[opt[0][1]] = switch.get(opt[0][1], []) + [opt[1]]
	    else:
		switch[opt[0][1]] = not switch.get(opt[0][1], False)

	for fl in files:
	    if '=' in fl:
		spl = fl.split('=')
		form[spl[0]] = spl[1]

    simple = int(form.get("simple", 0))
    pagename = form.get('page', '')
    barparse.ignoreoverride = int(form.get("noignore", 0))
    return form

#---- files -------------------------------------------------------------

class ArgFile (barparse.BarFile):
    def __init__(self, fname):
	self.picdir = ''
	self.fmttype = 'main'
	self.pagetitle = self.title = ''
	self.other = ()
	self.tail = {}
	self.styles = styles.StyleSet()
	#self.styles['.title'] = self.styles['.title.simple'] = styles.Style('.title')
	barparse.BarFile.__init__(self, fname)

    def Read(self):
	self.tail['stat'] = self.srcstat
	try:
	    return barparse.BarFile.Read(self)
	except IOError:
	    print FormatHead()
	    print "<!--",form,"-->"
	    print "<!--",datname,"is on crack. -->"
	    print """I'm sorry, that page was not found.  Please use your "BACK" button or try something else."""
	    print FormatTail()
	    sys.exit(1)

    def Parse_formatter(self, llist):
	self.picdir = llist.GetArg()
	self.fmttype = llist.GetArg()
	self.pagetitle = llist.GetArg()
	self.other = llist.llist[llist.curarg:]

    def Parse_style(self, llist):
	self.styles.Parse(llist)

    def Parse_page(self, llist):
	self.styles.Parse(llist)

    def Parse_title(self, llist):
	self.title = llist.GetArg('')

    def Parse_tail(self, llist):
	arg = llist.GetArg()
	while arg:
	    self.tail[arg] = 1
	    arg = llist.GetArg()


class SimpleFile(ArgFile):
    def __init__(self, fname):
	self.dblist = []
	ArgFile.__init__(self, fname)

    def __iter__(self):
	return self.dblist.__iter__()

    def ParseElse(self, llist):
	llist.Rewind()
	self.dblist.append(llist)

    def __len__(self):
	return len(self.dblist)


def Apply(dbfile):
    global fmttype, other, pagestyles, pagetitle, picdir, tail, title
    picdir = dbfile.picdir
    fmttype = dbfile.fmttype
    pagetitle = dbfile.pagetitle
    other = dbfile.other
    pagestyles.update(dbfile.styles)
    title = dbfile.title
    tail.update(dbfile.tail)


def ReadDir(patt, tdir=None):
    global picdir
    if not tdir:
	tdir = picdir
    odir = os.getcwd()
    os.chdir(tdir)
    flist = glob.glob(patt.strip())
    os.chdir(odir)
    return flist


def RootExt(fn):
    root, ext = os.path.splitext(fn)
    if ext:
	ext = ext[1:]
    return root,ext


def CleanName(f, morebad=''):
    badlist = [',', '#']

    n = f.strip()
    for b in badlist + list(morebad):
	n = n.replace(b[0], '_')
#    c = n.count('.')
#    if c > 0:
#	n = n.replace('.', '_', c - 1)
    return n


def IsAnyGood(flist, ext='', pdir=None, v=True):
    global picdir
    if not pdir:
	pdir = picdir
    for f in flist:
	if IsGood(pdir + '/' + f + '.' + ext, v):
	    return True
    return False


def IsGood(fname, v=True):
    fname = os.path.normpath(fname)
    if not fname:
	if v:
	    print "<!-- B",fname,"-->"
	return False
    if not os.path.exists(fname):
	if v:
	    print "<!-- N",fname,"-->"
	return False
    st = os.stat(fname)
    if (st[stat.ST_MODE] & 0x004) == 0:
	if v:
	    print "<!-- S",fname,"-->"
	return False
    if v:
	print "<!-- +",fname,"-->"
    return True


def Render(fname):
    if IsGood(fname):
	print file(fname).read()

#---- graphics ----------------------------------------------------------

def FmtButton(fname, also={}):
    global artdir
    if IsGood(os.environ['DOCUMENT_ROOT'] + '/' + artdir + '/but_' + fname.replace(' ', '_') + '.gif'):
	return '<img src="../%s/but_%s.gif"%s>' % (artdir, fname.replace(' ', '_'), Also({'class':'button','alt':fname}, also))
    return '<span class="textbutton">&nbsp;%s&nbsp;</span>' % fname.upper().replace(' ', '_')


def FmtArt(fname, desc='', hspace=0, also={}):
    global artdir
    return '<img src="../%s/%s"%s>' % (artdir, fname, Also({'hspace':hspace, 'alt':desc}, also))


def ImgSrc(pth, alt=None, also={}):
    if IsGood(pth):
	return '<img src="../' + pth + '"' + Also({'alt':alt}, also) + '>'
    return ''


def FindImg(fnames, made=True, suffix="jpg", pdir=None):
    global picdir
    if type(fnames) == str:
	fnames = [fnames]
    if not pdir:
	pdir = picdir
    #print "<!--",pdir,fnames,"-->"
    if suffix:
	suffix = '.' + suffix
    for fname in fnames:
	fname = CleanName(fname)
	if fname:
	    suf = suffix
	    if '.' in fname:
		suf = fname[fname.rfind('.'):]
		fname = fname[:fname.rfind('.') - 1]

	    pth = (pdir + '/' + fname + suf)
	    if IsGood(pth, v=False):
		return pth

	    pth = (pdir + '/' + fname.lower() + suf)
	    if IsGood(pth, v=False):
		return pth
    return NoPic(made)


def FmtImg(fnames, alt=None, suffix="jpg", pdir=None, also={}, made=True):
    global picdir
    if type(fnames) == str:
	fnames = [fnames]
    if not pdir:
	pdir = picdir
    #print "<!--",pdir,fnames,"-->"
    if suffix:
	suffix = '.' + suffix
    for fname in fnames:
	#fname = CleanName(fname)
	if fname:
	    suf = suffix
	    if '.' in fname:
		suf = fname[fname.rfind('.'):]
		fname = fname[:fname.rfind('.')]

	    img = ImgSrc(pdir + '/' + fname + suf, alt, also)
	    if img:
		return img
	    img = ImgSrc(pdir + '/' + (fname + suf).lower(), alt, also)
	    if img:
		return img
    return NoPic(made)


def NoPic(made=True):
    nopic = {False : 'nopic.gif', True : 'notmade.gif'}
    return FmtArt(nopic[not made])


def FmtWCImg(fn, alt=None, wc='', prefix='', suffix='jpg', pdir=None):
    global picdir
    if not pdir:
	pdir = picdir
    imgs = []

    orig = (prefix + fn + '.' + suffix)
    patt = (prefix + fn + wc + '.' + suffix)
    for fname in [orig] + ReadDir(patt, pdir):
	img = ImgSrc(pdir + '/' + fname, alt)
	if img:
	    imgs.append(img)
    return imgs


def FmtOptImg(fnames, alt=None, prefix='', suffix='jpg', pdir=None):
    global picdir
    if type(fnames) == str:
	fnames = [fnames]
    if not pdir:
	pdir = picdir
    if suffix:
	suffix = '.' + suffix
    for fname in fnames:
	if not '.' in fname:
	    fname = fname + suffix
	img = ImgSrc(pdir + '/' + prefix + fname, alt)
	if img:
	    return img
	img = ImgSrc(pdir + '/' + (prefix + fname).lower(), alt)
	if img:
	    return img
    return '&nbsp;'#NoPic()


def FmtHRefImg(fnames, txt, pdir=None, also={}):
    global picdir
    if type(fnames) == str:
	fnames = [fnames]
    if not pdir:
	pdir = picdir
    for fname in filter(None, fnames):
	#fname = CleanName(fname)
	if IsGood(pdir + '/' + fname + '.jpg'):
	    return '<a href="../%s.jpg"%s>%s</a>' % (pdir + '/' + fname, Also(also), txt)
	if IsGood(pdir + '/' + fname.lower() + '.jpg'):
	    return '<a href="../%s.jpg"%s>%s</a>' % (pdir + '/' + fname, Also(also), txt)
    return txt#NoPic()

#---- miscellaneous -----------------------------------------------------

def Plural(thing):
    if len(thing) != 1:
	return 's'
    return ''


def GetSearch(key):
    global form
    obj = form.get(key, "").split()
    nob = []
    col = ''
    for w in obj:
	if col:
	    col = col + ' ' + w
	    if col[-1] == '"':
		nob.append(col[1:-1])
		col = ''
	elif w[0] == '"' and w[-1] != '"':
	    col = w
	else:
	    nob.append(w)
    if col:
	nob.append(col[1:])
    return nob

def DumpDict(t, d, keys={}):
    print "<p><h3>",t,"</h3><p>"
    print '<dl>'
    if not keys:
	keys = d.keys()
    keys.sort()
    for k in keys:
	print '<dt>', k, '<dd>', d[k]
    print '</dl>'

#---- -------------------------------------------------------------------

if __name__ == '__main__':
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
