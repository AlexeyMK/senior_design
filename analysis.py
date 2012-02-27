#!/usr/local/bin/pythonw

""" note: use (at least on alexey's osx) /usr/local/bin/pythonw
sample code
"""
from scipy import linspace, polyval, polyfit, sqrt, stats, randn
from pylab import plot, title, show , legend


def mean_squared_error(tuples):
  """Uses lin-reg for something like [(2,1), (4,2) (0, 5), ...]"""
  polynomial_degree = 1 
  xs = [tup[0] for tup in tuples]
  ys = [tup[1] for tup in tuples]
  mx, b = polyfit(xs, ys, polynomial_degree)

  # mean square error (smaller is better)
  expected_ys = [mx * x + b for x in xs]
  errors_squared = [(expect - actual)**2 for expect, actual in zip(expected_ys, ys)]
  err = sqrt(sum(errors_squared) / len(tuples))

  return err

def plot_linreg(tuples):
  """lin-reg for something like [(2,1), (4,2) (0, 5), ...]"""
  polynomial_degree = 1 
  xs = [tup[0] for tup in tuples]
  ys = [tup[1] for tup in tuples]
  mx, b = polyfit(xs, ys, polynomial_degree)
  expected_ys = [mx * x + b for x in xs]

  #matplotlib ploting
  title('Linear Regression')
  plot(xs,ys,'g.')
  plot(xs,expected_ys,'r.-')
  legend(['actual', 'regression'])
  show()

#Linear regression using stats.linregress
#(a_s,b_s,r,tt,stderr)=stats.linregress(t,xn)
#print('Linear regression using stats.linregress')
#print('parameters: a=%.2f b=%.2f \nregression: a=%.2f b=%.2f, std error= %.3f' % (a,b,a_s,b_s,stderr))
