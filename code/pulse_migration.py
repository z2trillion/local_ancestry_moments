import sys
import wright_fisher_admixer as wf
	
k1 = 0.2264
T  = int(sys.argv[1])
parameters	=	{}
parameters[T]	=	([k1,1-k1],[0,1])


nSamples = 49
sim	=	wf.Simulation(N=1000)
for i in range(1000):
	d	= sim.drawDistribution(nSamples,30,parameters)
	print nSamples*'%f '%tuple(d[:,0])
	#print	np.var(d[:,0],ddof=1),np.var(d[:,1],ddof=1),np.var(d[:,2],ddof=1)

