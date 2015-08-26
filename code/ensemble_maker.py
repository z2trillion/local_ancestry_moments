import numpy as np
import matplotlib.pyplot as plt

from admixture_ms import coalescent

iterations = 5
N = 500
Ts = [5, 50, 500]
r = 1.0
m = .5
n = 50
c=coalescent(N=N, r=r)

fig, axes = plt.subplots(nrows=3, ncols=iterations)
for T, row in zip(Ts, axes):
	for i, axis in enumerate(row):
		sample=c.simulate_distribution(T=T, n=n, m=m)	
		image = np.zeros((n, n))
		for j, individual in enumerate(sample):
			image[:round(n*individual), j] = 1
		axis.imshow(image, interpolation='nearest')
		k1	=	np.mean(sample)
		k2	=	np.var(sample,ddof=1)
		axis.set_xlabel('%.2e' %k2)
		if i == 0:
			axis.set_ylabel('T=%i' %T)
		axis.set_xticks([])
		axis.set_yticks([])
plt.show()
