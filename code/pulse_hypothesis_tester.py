import os
import numpy as np

results = {}
resultsK3={}

for fileName in os.listdir('simulations'):
	if fileName[0] == 'T':
		T = int(fileName[2:-4])
		data = np.loadtxt('simulations/'+fileName)
	
		variances = np.sort(np.var(data,axis=1,ddof=1))
		results[T] = variances[[12,-13]]

		n  = len(data[0])
		s1 = np.sum(data,axis=1)
		s2 = np.sum(data**2,axis=1)
		s3 = np.sum(data**3,axis=1)
		k3 = np.sort(2*s1**3-3*n*s1*s2+n**2*s3)/(n*(n-1)*(n-2))
		resultsK3[T] = k3[[12,-13]]


observedVariance = 0.008636
observedK3       = 0.000284

for T in np.sort(results.keys()):
	print T, 
	print results[T][0] < observedVariance < results[T][1],
	print resultsK3[T][0] < observedK3 < resultsK3[T][1]
