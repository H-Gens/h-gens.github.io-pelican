# -*- coding: utf-8 -*-
"""
Created on Sat Mar 07 13:46:52 2015

@author: Alfonzo Jack

draws a Cox - Ci + Cdep series equivalent circuit
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['lines.linewidth'] = 2

plt.figure(2, figsize=(2, 2.5))
plt.clf()

wire = 2.0
width = 1.0
sep = 0.5

# ----------------
# pre-set the axis limits
# ----------------
# plt.axis([-width / 2, width / 2 + 0.3, 0, 3 * wire + 2 * sep])
# plt.axis([-1, 1.3, 0, 3 * wire + 2 * sep])
plt.axis('off')


# ----------------
# draw
# ----------------
# Ci
offset = -width
# wire
plt.plot([0 + offset, 0 + offset], [0.5 * wire, wire], 'k')
# capacitor
plt.plot([-width / 2 + offset, width / 2 + offset], [wire, wire], 'k')
plt.plot([-width / 2 + offset, width / 2 + offset], [wire + sep, wire + sep], 'k')
# wire
plt.plot([0 + offset, 0 + offset], [wire + sep, 1.5 * wire + sep], 'k')

# Cb
offset = width
# wire
plt.plot([0 + offset, 0 + offset], [0.5 * wire, wire], 'k')
# capacitor
plt.plot([-width / 2 + offset, width / 2 + offset], [wire, wire], 'k')
plt.plot([-width / 2 + offset, width / 2 + offset], [wire + sep, wire + sep], 'k')
# wire
plt.plot([0 + offset, 0 + offset], [wire + sep, 1.5 * wire + sep], 'k')

# branching wire
plt.plot(
    [-width, width], 
    [1.5 * wire + sep, 1.5 * wire + sep], 
    'k'
)
plt.plot(
    [-width, width], 
    [0.5 * wire, 0.5 * wire], 
    'k'
)
plt.plot([0, 0], [0, 0.5 * wire], 'k')

# Cox
plt.plot([0, 0], [1.5 * wire + sep, 2 * wire + sep], 'k')
plt.plot([-width / 2, width / 2], [2 * wire + sep, 2 * wire + sep], 'k')
plt.plot([-width / 2, width / 2], [2 * wire + 2 * sep, 2 * wire + 2 * sep], 'k')
# wire
plt.plot([0, 0], [2 * wire + 2 * sep, 3 * wire + 2 * sep], 'k')


# ----------------
# annotate
# ----------------
plt.text(width / 2 + width * 0.2, 2 * wire + sep, r'$C_{ox}$', fontsize=16)
plt.text(-width * 3 / 2 - 0.2, wire + sep + 0.5, r'$C_i$', fontsize=16)
plt.text(width * 3/ 2 - 0.3, wire + sep + 0.5, r'$C_b$', fontsize=16)
