import socket
import sys

class mysocket:
	def __init__(self, sock=None):
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.sock = sock

	def connect(self, host, port):
		try:
			for res in socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM):
				af, socktype, proto, canonname, sa = res
				print res
				print sa
				try:
					self.sock = socket.socket(af, socktype, proto)
				except socket.error, msg:
					self.sock = None
					continue
				try:
					self.sock.connect(sa)
				except socket.error, msg:
					self.sock.close()
					self.sock = None
					continue
				break
			if self.sock is None:
				print 'Closing Program...Could not open socket'
				sys.exit(1)
		except socket.gaierror, msg:
			print 'Closing Program...Could not resolve host name'
			print msg
			sys.exit(1)
	def mysend(self, msg):
		totalsent = 0
		while totalsent < len(msg):
			sent = self.sock.send(msg[totalsent:])
			if sent == 0:
				raise RuntimeError("socket connection broken")
			totalsent = totalsent + sent

	def myreceive(self):
		msg = ''
		while 1:
			chunk = self.sock.recv(512)
			print len(chunk)
			if chunk == '':
				break
		print msg
		return msg
	def mydisconnet(self):
		self.sock.close();
		
		
		
"""
import pyodbc
cnxn = pyodbc.connect('DSN=Test')
cnxn.commit()
cursor = cnxn.cursor()
print cursor.tables()
cursor.execute("insert into TbCardex (BOOKREF) values (?)", "1")
cursor.execute("insert into TbCardex (BOOKREF) values (?)", "2")
cursor.execute("insert into TbCardex (BOOKREF) values (?)", "3")
cursor.execute("select * from TbCardex")
for row in cursor:
	for item in row:
		print item
"""
