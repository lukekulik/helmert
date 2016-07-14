# Imports #
from random import random
import statsmodels.api as smapi
from statsmodels.formula.api import ols
import statsmodels.graphics as smgraphics
# Make data #
x = range(30)
y = [y*(10+random())+200 for y in x]
# Add outlier #
x.insert(6,15)
y.insert(6,220)
# Make fit #
regression = ols("data ~ x", data=dict(data=y, x=x)).fit()
# Find outliers #
test = regression.outlier_test()
outliers = ((x[i],y[i]) for i,t in enumerate(test.icol(2)) if t < 0.5)
print 'Outliers: ', list(outliers)
# Figure #
figure = smgraphics.regressionplots.plot_fit(regression, 1)
# Add line #
smgraphics.regressionplots.abline_plot(model_results=regression, ax=figure.axes[0])

