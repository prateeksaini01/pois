from temp import Connection, FaultTolerantConnection, Elgamal
import sys
import random

n = 16
e = 4
k = n - e

block_size = 256
tag_security = 64
tag_size = 2*tag_security

a_pub = (47384888438710931386215784312760678372065505132761136806979269743927639320899L,
	114191898301544883143438548739402893708827885665294514022825393390637319516983L, 
	104929877800320017746301156219610187412911988621147235171353721162239656856174L
) 
# a_priv = (
# 	47384888438710931386215784312760678372065505132761136806979269743927639320899L,
# 	114191898301544883143438548739402893708827885665294514022825393390637319516983L, 
# 	35419066023619120695246287648906566108750826178141484404889079155986724133108L
# )
b_pub = (
	15331369448061383155033776514110524264843948218754853159301419470148750022620L, 
	59823815739333087835575916522949305885907445651407263753424560139576673176123L, 
	32735848692019116713889118418549425785479221436814677827033078041042492306545L
) 
b_priv = (
	15331369448061383155033776514110524264843948218754853159301419470148750022620L, 
	59823815739333087835575916522949305885907445651407263753424560139576673176123L, 
	52755416722796889810406298047257157442501254756601530197639002860386203791287L
)
s = (2129046912237362864, 16016701388143895519L, 14801358758745401490L, 126, 64)
tag_pub = (2129046912237362864, 16016701388143895519L, 11764946258737926440L)
tag_priv = (2129046912237362864, 16016701388143895519L, 4535685677695551754)

recv_con = map( lambda x: Connection(r=int(x)),  sys.argv[1:n+1] )
send_con = map( lambda x: Connection(w=int(x)),  sys.argv[n+1:2*n+1] )

con = FaultTolerantConnection(n, k, send_con, recv_con, block_size, tag_size, s)
elgamal = Elgamal()

data = [random.getrandbits(20) for i in range(8)]
print "DATA: ", data

while True:
	x = [random.getrandbits(block_size - 1) for i in data]
	print ("DATA: " + "sending x = " + repr(x))
	con.send(x, b_priv, tag_priv)

	v = con.recv(a_pub, tag_pub)
	print ("DATA: " + "received v = " + repr(v) )

	m = [ data[i] ^ elgamal.decrypt( b_priv, (v[0], (v[1] - x[i])%b_priv[1]) ) for i in range(len(data))]
	print ("DATA: " + "sending m = " + repr(m))
	con.send(m, b_priv, tag_priv)
