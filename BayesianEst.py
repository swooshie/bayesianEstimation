# -*- coding: utf-8 -*-
"""Assignment1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1r-ihVk1VafUIngKFhHWnE8wkAuhvMJ2-
"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import sys
import numpy as np
import pandas as pd
import statsmodels.api as sm
import sympy as sp
import pymc3
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d import Axes3D
from scipy import stats
from scipy.special import gamma
import random
import decimal
import imageio

from matplotlib import rc
from matplotlib.animation import FuncAnimation
matplotlib.rcParams['animation.embed_limit'] = 2**128
from sympy.interactive import printing
printing.init_printing()

"""# **Setup**"""

np.random.seed(123)

nobs=160
#theta1 = float(decimal.Decimal(random.randrange(0,40))/100)
#theta2 = float(decimal.Decimal(random.randrange(60,100))/100)
#theta = random.choice([theta1,theta2])
theta=0.3
print('The randomly generated MLE:', theta)
Y=np.random.binomial(1,theta, nobs)
print(Y)

# Plotting the data
fig = plt.figure(figsize=(10,6))
gs = gridspec.GridSpec(1,2, width_ratios=[5,1])
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

ax2.hist(-Y, bins=2, rwidth=0.9)
ax1.plot(range(nobs), Y, 'x')


ax1.yaxis.set(ticks=(0,1), ticklabels=('Failure', 'Success'))
ax2.xaxis.set(ticks=(-1,0), ticklabels=('Success', 'Failure'))

ax1.set(title=f'Bernoulli Trial Outcomes $(θ={theta})$', xlabel='Trial', ylim=(-0.2, 1.2))
ax2.set(ylabel='Frequency', ylim=(0,nobs))

fig.tight_layout()

# Likelihood function

t, T, s = sp.symbols('theta, T, s')

# Create the function symbolically

likelihood = (t**s)*(1-t)**(T-s)

# Converting it to Numpy-callable function
_likelihood = sp.lambdify((t,T,s), likelihood, modules='numpy')

# Prior
# For alpha and beta
alpha = 4
beta = 6
prior_mean = alpha/(alpha + beta)
print('Prior mean:', prior_mean)

# Plot the prior 
fig = plt.figure(figsize=(10,4))
ax = fig.add_subplot(111)
X=np.linspace(0,1,1000)
ax.plot(X, stats.beta(alpha, beta).pdf(X), 'g')

# Cleanup
ax.set(title='Prior Distribution:', ylim=(0,12))
ax.legend(['Prior'])

# Posterior
# Finding the hyperparameters of the posterior

alpha_hat = alpha + Y.sum()
beta_hat = beta + nobs - Y.sum()

# Posterior mean
post_mean = alpha_hat/(alpha_hat + beta_hat)
print('Posterior Mean:', post_mean)

# Plot the analytic posterior

fig = plt.figure(figsize=(10,4))
ax= fig.add_subplot(111)
X = np.linspace(0,1,1000)
ax.plot(X, stats.beta(alpha_hat, beta_hat).pdf(X), 'r')

#Plot the prior
ax.plot(X, stats.beta(alpha, beta).pdf(X), 'g')

#Cleanup

ax.set(title='Posterior Distribution(Analytic)', ylim=(0,15))
ax.legend(['Posterior (Analytic)', 'Prior'])

"""# **GIFS Sections**"""

rc('animation', html='jshtml')

fig = plt.figure()
ax= fig.add_subplot(111)
X = np.linspace(0,1,1000)
ax.plot(X, stats.beta(alpha, beta).pdf(X), 'g')
axis = plt.axes(xlim =(0, 1),  
                ylim =(0, 15)) 
line, = axis.plot([], [], lw = 3) 
def init():  
  line.set_data([], []) 
  return line, 
  
def animate(i):
  X = np.linspace(0,1,1000)
  y=Y[:(i+1)%nobs]
  alpha_hat = alpha + y.sum()
  beta_hat = beta + (i+1)%nobs - y.sum()
  line.set_data(X, stats.beta(alpha_hat, beta_hat).pdf(X))

  return line

anim = FuncAnimation(fig, animate, init_func = init, 
                     frames = nobs, interval = 20) 

anim
#anim.save('E:\Aditya\BITS\3-1\CS-F320 Foundation of Data Science\Assignment\anim.mp4')