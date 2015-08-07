import sys
import wright_fisher_admixer as wf
	
k1 = 0.2264
T_start = int(sys.argv[1])
T_stop	=	int(sys.argv[2])

rate = 1-(1-k1)**(1/float(T_stop-T_start+1))
print rate

parameters	=	{}
for T in range(T_start,T_stop):
	parameters[T]	=	([rate],[0])
parameters[T_stop] = ([rate,1-rate],[0,1])

nSamples = 49
sim	=	wf.Simulation(N=1000)
for i in range(1000):
	d	= sim.drawDistribution(nSamples,30,parameters)
	print nSamples*'%f '%tuple(d[:,0])
	#print	np.var(d[:,0],ddof=1),np.var(d[:,1],ddof=1),np.var(d[:,2],ddof=1)

