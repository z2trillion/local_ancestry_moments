import sys
import itertools
import multiprocessing as mp
import wright_fisher_admixer as wf
	
k1 = 0.2264
nSamples = 49

def simulate(T):
	T_start, T_stop = T
	rate = 1-(1-k1)**(1/float(T_stop-T_start+1))

	parameters	=	{}
	for t in range(T_start,T_stop):
		parameters[t]	=	([rate],[0])
	parameters[T_stop] = ([rate,1-rate],[0,1])

	sim	=	wf.Simulation(N=1000)

	output = open('start=%i_stop=%i.txt' %T, 'w')
	for i in xrange(10000):
		d	= sim.drawDistribution(nSamples,30,parameters)
		output.write(nSamples*'%f '%tuple(d[:,0]) + '\n')
	#print	np.var(d[:,0],ddof=1),np.var(d[:,1],ddof=1),np.var(d[:,2],ddof=1)

times = itertools.product(range(8),range(18))
times = [(t_start, t_stop) for t_start, t_stop in times if t_start <= t_stop]

pool = mp.Pool(processes=10)

pool.map(simulate, times)
