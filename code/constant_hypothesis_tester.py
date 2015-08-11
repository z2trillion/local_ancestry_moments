import os
import numpy as np
import matplotlib.pyplot as plt

statistics = ['k2','k3','k4']
criticalValues = {s:{} for s in statistics}

for fileName in os.listdir('simulations'):
	if fileName[0] == 's':
		T_start = int(fileName[6])
		T_stop  = int(fileName[13:-4])
		
		#try:
		data = np.loadtxt('simulations/'+fileName,skiprows=1)
		#except ValueError,StopIteration:
		#continue
		
		n  = len(data[0])
		m1 = np.mean(data,axis=1)
		m2 = np.mean((data-m1[:,None])**2,axis=1)
		m3 = np.mean((data-m1[:,None])**3,axis=1)
		m4 = np.mean((data-m1[:,None])**4,axis=1)

		k2 = n*np.sort(m2)/(n-1)
		k3 = n**2*np.sort(m3)/((n-1)*(n-2))
		k4 = n**2*np.sort((n+1)*m4-3*(n-1)*m2**2)/((n-1)*(n-2)*(n-3))
		
		criticalValues['k2'][(T_start,T_stop)] = k2[[8,-8]]
		criticalValues['k3'][(T_start,T_stop)] = k3[[8,-8]]
		criticalValues['k4'][(T_start,T_stop)] = k4[[8,-8]]

observed = {}
observed['k2'] = 0.008636
observed['k3'] = 0.000284
observed['k4'] = -3.17950532473*10**-5


image = np.zeros((17,17))

for Ts in sorted(criticalValues['k2'].keys()):
	rejected = False
	for s in statistics:
		if not criticalValues[s][Ts][0] < observed[s] < criticalValues[s][Ts][1]:
			rejected = True
	if not rejected:
		try:
			image[Ts] = 1
		except IndexError:
			pass
	
#image = image.transpose()

plt.imshow(image,interpolation='nearest')
plt.show()



