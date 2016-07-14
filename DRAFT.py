from scipy import stats
import matplotlib.pyplot as plt

x = np.linspace(-5, 5, num=150)
y = x + np.random.normal(size=x.size)
y[11:15] += 10  # add outliers
y[-5:] -= 7

res = stats.theilslopes(y, x, 0.90)
lsq_res = stats.linregress(x, y)

print 'dawdawdawd'
print res
print lsq_res