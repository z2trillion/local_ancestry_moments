import numpy as np
from bisect import bisect
class Simulation:
	def __init__(self,N):
		self.N	=	N
	def drawDistribution(self,nSamples,R,admixtureParameters):	
		population	=	Population(N=self.N)
		population.makePedigree(nSamples,admixtureParameters)
		population.inheritLocalAncestries(R)
		distribution	=	np.zeros((nSamples,3))
		for source in [0,1,2]:
			for i,person in enumerate(population.generations[0].people.values()):
				try:
					distribution[i,source]	=	person.getAncestryFractions()[source]
				except KeyError:
					distribution[i,source]	=	0
		return distribution
class Population:
	def __init__(self,N):
		self.N						=	N
	def makePedigree(self,nSamples,admixtureParameters):
		currentGeneration	=	None
		self.generations	=	[None for T in range(max(admixtureParameters)+1)]
		for T in range(len(self.generations)):
			try:
				ms,sources	=	admixtureParameters[T]
				currentGeneration	=	Generation(self,currentGeneration,nSamples,ms=ms,sources=sources)
			except KeyError:
				currentGeneration	=	Generation(self,currentGeneration,nSamples)
			self.generations[T]	=	currentGeneration
	def inheritLocalAncestries(self,R):
		for generation in self.generations[::-1]:
			generation.inheritLocalAncestries(R)
class Generation:
	def __init__(self,population,nextGeneration=None,nSamples=None,ms=None,sources=None):
		if nextGeneration is None:
			self.people	=	dict((i,Person(ms=ms,sources=sources)) for i in range(nSamples))
		else:
			leftParentIDs		=	[np.random.randint(population.N) for chromosome in nextGeneration]
			rightParentIDs	=	[np.random.randint(population.N) for chromosome in nextGeneration]
			parentIDs				=	set(leftParentIDs)|set(rightParentIDs)
			
			self.people	=	dict((ID,Person(ms=ms,sources=sources)) for ID in parentIDs)
			nextGeneration.assignParents(self,leftParentIDs,rightParentIDs)
	def __iter__(self):
		return self
	def next(self):
		try: 
			self.counter	+= 1
		except AttributeError:
			self.counter	=	0
		try:
			if not self.people.values()[self.counter].isMigrant:
				return self.people.values()[self.counter]
			else:
				return self.next() 
		except IndexError:
			self.counter	=	-1
			raise StopIteration
	def assignParents(self,previousGeneration,leftParentIDs,rightParentIDs):
		for i,chromosome in enumerate(self):
			chromosome.assignLeftParent(previousGeneration.people[leftParentIDs[i]])
			chromosome.assignRightParent(previousGeneration.people[rightParentIDs[i]])
	def inheritLocalAncestries(self,R):
		for chromosome in self.people.values():
			chromosome.inheritLocalAncestry(R)
class Person:
	def __init__(self,ms=None,sources=None):
		self.isMigrant	 =	False
		if ms is not None:
			u	=	np.random.uniform()
			p	=	0
			for i in range(len(ms)):
				p+=ms[i]
				if u<p:
					self.isMigrant	=	True
					self.source			=	sources[i]
					break 
	def assignLeftParent(self,leftParent):
		self.leftParent		=	leftParent
	def assignRightParent(self,rightParent):
		self.rightParent	=	rightParent
	def inheritLocalAncestry(self,R):
		if self.isMigrant:
			self.leftChromosome		=	Chromosome([R],[self.source])
			self.rightChromosome	=	Chromosome([R],[self.source])
		else:
			self.leftChromosome		=	self.leftParent.makeGamete(R)
			self.rightChromosome	=	self.rightParent.makeGamete(R)
	def makeGamete(self,R):
		nCrossoverPoints	=	np.random.poisson(R)	 
		#crossoverPoints	=np.array([1])
		crossoverPoints		=	R*np.sort(np.random.uniform(size=nCrossoverPoints))
		crossoverPoints		=	np.append(crossoverPoints,R+1)
		#print crossoverPoints
		if np.random.uniform()<.5:
			copying			=	self.leftChromosome
			notCopying	=	self.rightChromosome
		else:
			copying			=	self.rightChromosome
			notCopying	=	self.leftChromosome

		transitionPoints	=	copying.getTransitionPoints(0,crossoverPoints[0])
		ancestries				=	copying.getAncestries(0,crossoverPoints[0])
		for i,crossoverPoint in enumerate(crossoverPoints[:-1]):
			copying,notCopying	=	notCopying,copying

			newTransitionPoints	=	copying.getTransitionPoints(crossoverPoint,crossoverPoints[i+1])
			newAncestries				=	copying.getAncestries(crossoverPoint,crossoverPoints[i+1])
				
			newTransitionPoints	=	np.append(crossoverPoint,newTransitionPoints)
			newAncestries				=	np.append(notCopying.getAncestry(crossoverPoint),newAncestries)

			transitionPoints	=	np.append(transitionPoints,newTransitionPoints)
			ancestries				=	np.append(ancestries,newAncestries)
			
		transitionPoints	= np.append(transitionPoints[np.diff(ancestries)!=0],R)
		ancestries				= np.append(ancestries[np.diff(ancestries)!=0],ancestries[-1])
		assert len(ancestries)==len(transitionPoints)
		return Chromosome(transitionPoints,ancestries)
	def getAncestryFractions(self):
		leftFractions		=	self.leftChromosome.getAncestryFractions()
		rightFractions	=	self.rightChromosome.getAncestryFractions()
		
		fractions	=	{}
		for label in set(leftFractions.keys())|set(rightFractions.keys()):
			try:
				leftFraction	=	leftFractions[label]
			except KeyError:
				leftFraction	=	0
			try:
				rightFraction	=	rightFractions[label]
			except KeyError:
				rightFraction	=	0
			fractions[label]	=	(leftFraction+rightFraction)/2
		return fractions
class Chromosome:
	def __init__(self,transitionPoints,ancestries):
		self.transitionPoints	=	np.array(transitionPoints)
		self.ancestries				=	np.array(ancestries)
	def getAncestries(self,left,right):
		indices	=	(left<self.transitionPoints)*(self.transitionPoints<right)
		return self.ancestries[indices]
	def getTransitionPoints(self,left,right):
		indices	=	(left<self.transitionPoints)*(self.transitionPoints<right)
		return self.transitionPoints[indices]
	def getAncestry(self,x):
		try:
			return self.ancestries[bisect(self.transitionPoints,x)]	
		except IndexError:
			print x,self.transitionPoints,self.ancestries
		 	raise IndexError
	def getAncestryFractions(self):
		segmentLengths	=	np.diff(np.append([0],self.transitionPoints))
		fractions	=	{}
		for label in set(self.ancestries):
			fractions[label]	=	sum(segmentLengths[self.ancestries==label])/self.transitionPoints[-1]
		return fractions
if __name__=='__main__':
	parameters	=	{}
	#parameters[4]		=	((0.5,0.5),(0,1))
	parameters[2]		=	([0.16],[0])
	parameters[20]	=	([0.071,0.929],[1,2])

	sim	=	Simulation(N=1000)
	total=0
	for i in range(1000):
		#p	=	Population(N=1000)
		#p.makePedigree(8,parameters)
		#print i
		d	= sim.drawDistribution(8,30,parameters)
		#print 8*'%f '%tuple(d[:,1])
		print	np.var(d[:,0],ddof=1),np.var(d[:,1],ddof=1),np.var(d[:,2],ddof=1)

