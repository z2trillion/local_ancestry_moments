import numpy as np
from admixture_ms import coalescent

iterations	=	10**6
N						=	1000
T						=	20
r						=	.01
m						=	.3
n						=	1000
c=coalescent(N=N,r=r)

for iteration in xrange(iterations):
	sample=c.simulate_distribution(T=T,n=n,m=m)	
	k1	=	np.mean(sample)
	k2	=	np.var(sample,ddof=1)
	k3	=	np.mean((sample-k1)**3)*n**2/(n-1)/(n-2)

	m2	=	np.mean((sample-k1)**2)
	m4	=	np.mean((sample-k1)**4)
	k4	=	n**2*((n+1)*m4-3*(n-1)*m2**2)/(n-1)/(n-2)/(n-3)

	print k1,k2,k3,k4

