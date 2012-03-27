#!/usr/local/bin/pythonw
""" note: use (at least on alexey's osx) /usr/local/bin/pythonw
Based on http://www.scipy.org/Cookbook/LinearRegression
"""
from scipy import linspace, polyval, polyfit, sqrt, stats
from pylab import plot, title, show, legend, xlabel, ylabel, savefig


def mean_squared_error(tuples):
  """Uses lin-reg for something like [(2,1), (4,2) (0, 5), ...]"""
  polynomial_degree = 1 
  xs = [int(tup[0]) for tup in tuples]
  ys = [int(tup[1]) for tup in tuples]
  mx, b = polyfit(xs, ys, polynomial_degree)

  # mean square error (smaller is better)
  expected_ys = [mx * x + b for x in xs]
  errors_squared = [(expect - actual)**2 for expect, actual in zip(expected_ys, ys)]
  err = sqrt(sum(errors_squared) / len(tuples))

  return err


def plot_linreg(tuples, save_fname=None, do_show=False):
  """lin-reg for something like [(2,1), (4,2) (0, 5), ...]"""
  polynomial_degree = 1 
  xs = [tup[0] for tup in tuples]
  ys = [tup[1] for tup in tuples]
  mx, b = polyfit(xs, ys, polynomial_degree)
  expected_ys = [mx * x + b for x in xs]

  #matplotlib ploting
  title('Linear Regression')
  plot(xs,ys,'g.', label="actual")
  plot(xs,expected_ys,'r.-', label="expected")
  legend(['data','trendline from data'])
  # TODO (maybe) plot 'actual' expected line (IE, 0 --> 1, 10 --> 5?)
  xlabel('Amount offered (c)')
  ylabel('Rating given (1-5 stars)')
  if save_fname:
     savefig(save_fname, format="png") 
  if do_show:
    show()

