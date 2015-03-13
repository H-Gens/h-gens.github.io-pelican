# -*- coding: utf-8 -*-
"""
Created on Sat Mar 07 13:23:09 2015

@author: Alfonzo Jack

draws a Cox - Cs series equivalent circuit
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['lines.linewidth'] = 2

plt.figure(1, figsize=(1.75, 2.5))
plt.clf()

wire = 2.0
width = 1.0
sep = 0.5

# ----------------
# pre-set the axis limits
# ----------------
plt.axis([-width / 2, width / 2 + 0.3, 0, 3 * wire + 2 * sep])
plt.axis([-1, 1.3, 0, 3 * wire + 2 * sep])
plt.axis('off')


# ----------------
# draw
# ----------------
# wire
plt.plot([0, 0], [0, wire], 'k')
# Cs
plt.plot([-width / 2, width / 2], [wire, wire], 'k')
plt.plot([-width / 2, width / 2], [wire + sep, wire + sep], 'k')
# wire
plt.plot([0, 0], [wire + sep, 2 * wire + sep], 'k')

# Cox
plt.plot([-width / 2, width / 2], [2 * wire + sep, 2 * wire + sep], 'k')
plt.plot([-width / 2, width / 2], [2 * wire + 2 * sep, 2 * wire + 2 * sep], 'k')
# wire
plt.plot([0, 0], [2 * wire + 2 * sep, 3 * wire + 2 * sep], 'k')


# ----------------
# annotate
# ----------------
plt.text(width / 2 + width * 0.2, 2 * wire + sep, r'$C_{ox}$', fontsize=16)
plt.text(width / 2 + width * 0.2, wire, r'$C_s$', fontsize=16)
