#!/usr/local/bin/python

import os, sys
import Cookie
import Crypto.Cipher.DES


class CryptCookie(Cookie.BaseCookie):
    def __init__(self, inp=None):
	self.crypkey = 'LesNey47'
	self.cipher = Crypto.Cipher.DES.new(self.crypkey, Crypto.Cipher.DES.MODE_ECB)
	Cookie.BaseCookie.__init__(self, inp)

    def value_decode(self, val):
	decval = Cookie._unquote(val)
	decval = self.cipher.decrypt(decval).strip()
        return decval, val

    def value_encode(self, val):
	strval = str(val)
	strval += ' ' * (8 - len(strval) % 8)
	strval = self.cipher.encrypt(strval)
        return val, Cookie._quote(strval)


def ClearCookie(cdict):
    cookie = Cookie.BaseCookie()
    for key in cdict.keys():
	cookie[key] = cdict[key]
	cookie[key]['expires'] = -1
	cookie[key]['domain'] = CookieDomain()
	cookie[key]['path'] = '/'
    return cookie


def CookieDomain():
    return '.'.join(os.environ['SERVER_NAME'].split('.')[-2:])


def MakeCookie(cdict, expires=6000):
    if not cdict:
	return Cookie.Cookie()
    cookie = CryptCookie()
    for key in cdict.keys():
	cookie[key] = cdict[key]
	cookie[key]['expires'] = expires
	cookie[key]['domain'] = CookieDomain()
	cookie[key]['path'] = '/'
    return cookie


def GetCookies():
    if os.environ.get('HTTP_COOKIE'):
	cookie = CryptCookie()
	try:
	    cookie.load(os.environ['HTTP_COOKIE'])
	except:
	    pass
	return cookie


if __name__ == '__main__':
    pass
