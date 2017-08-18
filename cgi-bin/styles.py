#!/usr/local/bin/python

import copy

basicstyles = ['body', 'body.simple', 'a:link', 'a:visited', 'a:active', 'a:hover', '.title', '.button', '.textbutton', 'img']
defstyles = {
    'body'        : {'c' : '#000000', 'bgc' : '#FFFFFF'},
    'body.simple' : {'c' : '#000000', 'bgc' : '#FFFFFF'},
    'a:link'      : {'c' : '#000066', 'bgc' : 'transparent', 'td' : 'none'},
    'a:visited'   : {'c' : '#660000', 'bgc' : 'transparent', 'td' : 'none'},
    'a:active'    : {'c' : '#006600', 'bgc' : 'transparent', 'td' : 'none'},
    'a:hover'     : {'c' : '#000066', 'bgc' : 'transparent', 'td' : 'underline'},
    '.button' : {
	'bw' : '0px',
	'va' : 'middle',
	'p' : '1px',
	'c' : '#FFFFFF'},
    '.textbutton' : {
	'bw' : '0px',
	'va' : 'middle',
	'p' : '1px',
	'bgc' : '#006600',
	'c' : '#FFFFFF',
	'ff' : '"Trebuchet MS", "Arial", "sans-serif"'},
    '.title' : {
	'c' : '#000000',
	'fz' : 'xx-large',
	'fw' : 'bold',
	'ta' : 'center'},
    '.table' : {
	'bgc' : '#FFFFFF',
	'bc' : '#000000',
	'bw' : '1px',
	'p' : '2px',
	'bsp' : '1px',
	'w' : '100%',
	'bs' : 'solid',
	'bcps' : 'separate'},
    '.section' : {
	'bgc' : '#FFFFFF',
	'bc' : '#000000',
	'ta' : 'center',
	'va' : 'middle',
	'bw' : 'thin',
	'fz' : 'x-large',
	'c' : '#000000',
	'bs' : 'solid',
	'p' : '4px'},
    '.subsection' : {
	'ta' : 'center',
	'va' : 'middle',
	'fz' : 'large',
	'bs' : 'solid',
	'bw' : 'thin',
	'bc' : '#000000'},
    '.hcell' : {
	#'bgc' : '#FFFFFF',
	'va' : 'top',
	'fz' : 'medium',
	'ta' : 'center',
	'bs' : 'ridge',
	'bw' : 'thin',
	'bc' : '#000000',
	'fw' : 'bold',
	#'c' : '#000000',
	'p' : '4px'}, 
    '.cell' : {
	#'bgc' : '#FFFFFF',
	'va' : 'top',
	'fz' : 'medium',
	'ta' : 'left',
	'bs' : 'ridge',
	'bw' : 'thin',
	'bc' : '#000000',
	#'c' : '#000000',
	'p' : '4px'}, 
}

style_d = {
	'bb'    : 'border-bottom',
	'bbc'   : 'border-bottom-color',
	'bbw'   : 'border-bottom-width',
	'bcps'  : 'border-collapse',
	'bc'    : 'border-color',
	'bga'   : 'background-attachment',
	'bgc'   : 'background-color',
	'bgi'   : 'background-image',
	'bgp'   : 'background-position',
	'bgr'   : 'background-repeat',
	'bl'    : 'border-left',
	'blc'   : 'border-left-color',
	'blw'   : 'border-left-width',
	'br'    : 'border-right',
	'brc'   : 'border-right-color',
	'brw'   : 'border-right-width',
	'bs'    : 'border-style',
	'bsp'   : 'border-spacing',
	'bt'    : 'border-top',
	'btc'   : 'border-top-color',
	'btw'   : 'border-top-width',
	'bw'    : 'border-width',
	'c'     : 'color',
	'clr'   : 'clear',
	'cs'    : 'caption-side',
	'ec'    : 'empty-cells',
	'f'     : 'float',
	'ff'    : 'font-family',
	'fs'    : 'font-style',
	'fsa'   : 'font-size-adjust',
	'fstr'  : 'font-stretch',
	'fv'    : 'font-variant',
	'fw'    : 'font-weight',
	'fz'    : 'font-size',
	'h'     : 'height',
	'lh'    : 'line-height',
	'ls'    : 'letter-spacing',
	'lsi'   : 'list-style-image',
	'lsp'   : 'list-style-position',
	'lst'   : 'list-style-type',
	'm'     : 'margin',
	'mb'    : 'margin-bottom',
	'ml'    : 'margin-left',
	'mo'    : 'marker-offset',
	'mr'    : 'margin-right',
	'mt'    : 'margin-top',
	'oc'    : 'outline-color',
	'os'    : 'outline-style',
	'ow'    : 'outline-width',
	'p'     : 'padding',
	'pb'    : 'padding-bottom',
	'pl'    : 'padding-left',
	'pr'    : 'padding-right',
	'pt'    : 'padding-top',
	'ta'    : 'text-align',
	'td'    : 'text-decoration',
	'ti'    : 'text-indent',
	'tl'    : 'table-layout',
	'ts'    : 'text-shadow',
	'tt'    : 'text-transform',
	'va'    : 'vertical-align',
	'w'     : 'width',
	'whs'   : 'white-space',
	'ws'    : 'word-spacing',
}

class Style:
    def __init__(self, name='', vals={}):
	self.name = name
	self.style = copy.deepcopy(defstyles.get(name, {}))
	self.style.update(vals)

    def Parse(self, llist):
	self.name = llist[1]
	for ent in llist[2:]:
	    p,v = tuple(ent.split(',') + [''])[0:2]
	    self.style[p] = v

    def __repr__(self):
	return repr(self.name) + ' : ' + repr(self.style)

    def __str__(self):
	return self.name + ' : ' + str(self.style)

    def Interpret(self, p):
	if p == 'bgi':
	    return 'url(' + self.style[p] + ')'
	return self.style[p]

    def Fields(self):
	return ' '.join(map(lambda p: style_d.get(p, p) + ': ' + self.Interpret(p) +';', self.style.keys()))

    def Format(self):
	name = self.name
	return name + ' {' + self.Fields() + '}'

    def setdefault(self, key, arg):
	self.style.setdefault(key, arg)

    def keys(self):
	return self.style.keys()

    def update(self, dic):
	self.style.update(dic)

    def __len__(self):
	return len(self.style)

    def __getitem__(self, key):
	return self.style[key]

    def __setitem__(self, key, val):
	self.style[key] = val

    def __iter__(self):
	return self.style.iterkeys()

    def __delitem__(self, key):
	del self.style[key]

    def __contains__(self, key):
	return key in self.style


class StyleSet:
    def __init__(self, styles=[]):
	self.styleset = {}
	if type(styles) != list:
	    styles = [styles]

	for cname in basicstyles + styles:
	    if ',' in cname:
		cnames = cname.split(',')
		for modif in cnames[1:]:
		    self.setdefault(cnames[0] + '_' + modif, Style(cnames[0]))
		    self.styleset[cnames[0] + '_' + modif].name = cnames[0] + '_' + modif
	    else:
		self.setdefault(cname, Style(cname))

    def __repr__(self):
	return '{ ' + ', '.join(map(lambda x: repr(self.styleset[x]), self.styleset)) + ' }'

    def __str__(self):
	return ', '.join(map(lambda x: str(self.styleset[x]), self.styleset))

    def setdefault(self, key, arg):
	if not key in self.styleset:
	    self.styleset[key] = Style(key)
	    self.styleset[key].update(arg)
	    self.styleset[key].name = key

    def get(self, name, default=None):
	return self.styleset.get(name, default)

    def Format(self, simple=False):
	ostr = ''
	if self.styleset:
	    stylekeys = filter(lambda x: not x.endswith('.simple'), self.styleset.keys())
	    for cname in stylekeys:
		if simple and cname + ".simple" in self.styleset:
		    ostr += self.styleset[cname].Format() + '\n'
		else:
		    ostr += self.styleset[cname].Format() + '\n'
	return ostr

    def keys(self):
	return self.styleset.keys()

    def update(self, dic):
	for key in dic:
	    if key in self.styleset:
		self.styleset[key].update(dic[key])
	    else:
		self.styleset[key] = dic[key]
		self.styleset[key].name = key

    def __len__(self):
	return len(self.styleset)

    def __getitem__(self, key):
	if not key in self.styleset:
	    self.styleset[key] = Style(key)
	return self.styleset[key]

    def __setitem__(self, key, val):
	self.styleset[key] = val
	self.styleset[key].name = key

    def __iter__(self):
	return self.styleset.iterkeys()

    def __delitem__(self, key):
	del self.styleset[key]

    def __contains__(self, key):
	return key in self.styleset

    def Parse(self, llist):
	if llist[0] == 'page':
	    bstyles = { 'b' : 'body', 'l' : 'a:link', 'v' : 'a:visited', 'a' : 'a:active', 'h' : 'a:hover' }
	    for ent in llist.llist[1:]:
		simp = ''
		sset, nstyle = tuple(ent.split(':', 1))
		for stt in sset:
		    if stt == 's':
			simp = '.simple'
		    elif stt in bstyles:
			for sty in nstyle.split(';'):
			    sty = sty.split(',', 1)
			    self.styleset[bstyles[stt] + simp][sty[0]] = sty[1]
	else:
	    cname = llist[1]
	    sd = Style(cname)
	    sd.Parse(llist)
	    if ',' in cname:
		cnames = cname.split(',')
		for modif in cnames[1:]:
		    self.styleset.setdefault(cnames[0] + '_' + modif + '.simple', Style(cnames[0]))
		    self.styleset.setdefault(cnames[0] + '_' + modif, Style(cnames[0]))
		    self.styleset[cnames[0] + '_' + modif].name = cnames[0] + '_' + modif
		    self.styleset[cnames[0] + '_' + modif].update(sd)
	    else:
		self.styleset.setdefault(cname + '.simple', Style(cname))
		self.styleset.setdefault(cname, Style(cname))
		self.styleset[cname].update(sd)

    def FindName(self, cname, simple=False):
	if simple and '.' + cname + '.simple' in self.styleset:
	    return cname + '.simple'
	elif '.' + cname in self.styleset:
	    return cname
	elif '.' + cname[:cname.find('_')] in self.styleset:
	    return cname[:cname.find('_')]
	return Style()


if __name__ == '__main__':
	print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
