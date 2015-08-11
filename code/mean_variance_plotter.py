import numpy as np
import matplotlib.pyplot as plt

resamples = np.loadtxt('ASW_YRI_CEU_pruned_resample_B.txt')

means = np.mean(resamples, axis=0)
variances = np.var(resamples, axis=0, ddof=1)
e3 = ((resamples - means)**3).sum(axis=0)

x = means * (1-means)
print np.polyfit(x, variances, 1)
#plt.ylim([0,.0005])

plt.scatter(x, variances)
plt.show()

