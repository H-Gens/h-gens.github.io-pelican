# -*- coding: utf-8 -*-
"""
Created on Sat Mar 07 12:22:30 2015

@author: Alfonzo Jack

draws a band diagram including Evac for SPE derivation
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import matplotlib as mpl
mpl.rcParams['lines.linewidth'] = 2
# -----------------------
# user-defined settings
# -----------------------
T = 300 # lattice temperature, Kelvin
tox = 20e-9 * 100 # 50 nm oxide converted to cm
Nd = 1e16 # donor doping concentration, # / cm^3
Na = 1e17 # acceptor doping concentration, # / cm^3
CBO = 1.0 # SiO2/Si conduction band offset, eV
VBO = 1.0 # SiO2/Si valence band offset, eV

# -----------------------
# physical constants
# -----------------------
e0 = 8.854e-14 # permittivity of free space, F / cm
q = 1.602e-19 # elementary charge, Coulombs
k = 8.617e-5 # Boltzmann constant, eV / K

# -----------------------
# material parameters 
# -----------------------
es = 11.7 # relative permittivity, silicon
eox = 3.9 # relative permittivity, SiO2
chi_s = 4.17 # electron affinity, silicon, eV
phi_m = 5.01 # work function, nickel, eV
# bandgap, silicon, eV
Eg = 1.17 - 4.73e-4 * T ** 2 / (T + 636.0)
# effective valence band DOS, silicon, # / cm^3
Nv = 3.5e15 * T ** 1.5
# effective conduction band DOS, silicon, # / cm^3
Nc = 6.2e15 * T ** 1.5

def solve_bisection(func, target, xmin, xmax):
    """
    Returns the independent value x satisfying func(x)=value.
    - uses the bisection search method
      https://en.wikipedia.org/wiki/Bisection_method

    Arguments:
        func - callable function of a single independent variable
        target - the value func(x) should equal
        [xmin, xmax] - the range over which x can exist
    """
    tol = 1e-10 # when |a - b| <= tol, quit searching
    max_iters = 1e2 # maximum number of iterations
    a = xmin
    b = xmax
    cnt = 1
    # before entering while(), calculate Fa
    Fa = target - func(a)
    c = a

    # bisection search loop
    while np.abs(a - b) > tol and cnt < max_iters:
        cnt += 1
        # make 'c' be the midpoint between 'a' and 'b'
        c = (a + b) / 2.0
        # calculate at the new 'c'
        Fc = target - func(c)

        if Fc == 0:
            # 'c' was the sought-after solution, so quit
            break
        elif np.sign(Fa) == np.sign(Fc):
            # the signs were the same, so modify 'a'
            a = c
            Fa = Fc
        else:
            # the signs were different, so modify 'b'
            b = c

    if cnt == max_iters:
        print('WARNING: max iterations reached')

    return c

# -----------------------
# dependent calculations
# -----------------------
# intrinsic carrier concentration, silicon, # / cm^3
ni = np.sqrt(Nc * Nv) * np.exp(-Eg / (2 * k * T))
# Energy levels are relative to one-another in charge expressions.
# - Therefore, it is OK to set Ev to a reference value of 0 eV.
# Usually, energy levels are given in Joules and one converts to eV.
# - I have just written each in eV to save time.
Ev = 0 # valence band energy level
Ec = Eg # conduction band energy level
Ei = k * T * np.log(ni / Nc) + Ec # intrinsic energy level
phit = k * T # thermal voltage, eV
# get the Fermi level in the bulk where there is no band-bending
n = lambda Ef: Nc * np.exp((-Ec + Ef) / phit)
p = lambda Ef: Nv * np.exp((Ev - Ef) / phit)
func = lambda Ef: p(Ef) - n(Ef) + Nd - Na
Ef = solve_bisection(func, 0, Ev, Ec)
# compute semiconductor work function (energy from vacuum to Ef)
phi_s = chi_s + Ec - Ef
# flatband voltage and its constituent(s)
# - no defect-related charges considered
phi_ms = phi_m - phi_s # metal-semiconductor workfunction, eV
Vfb = phi_ms # flatband voltage, V
# oxide capacitance per unit area, F / cm^2
Coxp = eox * e0 / tox
# if both Nd and Na are zero, then make one slightly higher
# calculate effective compensated doping densities
# - assume complete ionization
if Na > Nd:
    Na = Na - Nd
    Nd = 0
    device_type = 'nMOS'
else:
    Nd = Nd - Na
    Na = 0
    device_type = 'pMOS'
# -----------------------
# define the SPE
# -----------------------
# compute equilibrium carrier concentrations
n_o = Nc * np.exp((-Ec + Ef) / phit)
p_o = Nv * np.exp((Ev - Ef) / phit)
# define the charge function so it can be used in the SPE
f = lambda psis: psis * (Na - Nd) \
  + phit * p_o * (np.exp(-psis / phit) - 1) \
  + phit * n_o * (np.exp(psis / phit) - 1)
Qs = lambda psis: -np.sign(psis) * np.sqrt(2 * q * e0 * es * f(psis))
SPE = lambda psis: Vfb + psis - Qs(psis) / Coxp


# -----------------------
# y-computation functions
# -----------------------
# define the electric field
E = lambda psi: np.sign(psi) * np.sqrt(2 * q / (es * e0) * f(psi))
# this is the integrand needed to compute y
integrand_y = lambda psi: 1 / E(psi)

def compute_y_vs_psi(psis):
    """
    This function creates a 'psi' variable ranging from psis to ~zero.
    It then computes the y-values corresponding to every value in psi.

    psis is the surface potential and must be a scalar constant.
    """
    # handle the flatband case
    if psis == 0:
        y = np.linspace(0, 150, 101) * 1e-7
        psi = 0 * y
        return y, psi
    # (1) let semiconductor potential range from psis to near-zero
    psi = np.linspace(psis, psis * 1e-3, 101)
    # (2) call compute_y() at every value in psi
    # collect the returned y-values in an array
    y = np.array([])
    for value in psi:
        y_current, error = quad(integrand_y, value, psis)
        y = np.hstack((y, y_current))
    return y, psi


# -----------------------
# choose a potential to plot
# -----------------------
#psis = Ev - Ef        # accumulation
#psis = 0              # flatband
psis = Ei - Ef        # weak inversion
#psis = 2 * (Ei - Ef)  # strong inversion
#psis = Ec - Ef        # (very) strong inversion

# compute the corresponding Vgb value
Vgb = SPE(psis)

# create figure, label axes, turn grid on
plt.figure(1, figsize=(6, 5))
plt.clf()
plt.xlabel('y (nm)', fontsize=14)
plt.ylabel('potential relative to Ev (eV)', fontsize=14)
plt.grid(True)

# get psiox from the potential balance equation (see SPE derivation)
psiox = Vgb - psis - phi_ms
# print Vgb, psiox

# construct the psi vs y curve
y, psi = compute_y_vs_psi(psis)
# y and tox are in cm, so change to be in nm
y = y / 100 * 1e9
toxnm = tox / 100 * 1e9

# plot the conduction/intrinsic/valence bands
plt.plot(y, Ev - psi, 'b')
plt.plot(y, Ei - psi, 'b--')
plt.plot(y, Ec - psi, 'b')

# plot the fermi level
plt.plot(y, 0 * y + Ef, 'k')

# plot the SiO2 bands
plt.plot([0, 0], [Ev - psis - VBO, Ec - psis + CBO], 'r')
plt.plot(
    [-toxnm, -toxnm], 
    [Ev - psis - VBO - psiox, Ec - psis + CBO - psiox], 
    'r'
)
plt.plot([-toxnm, 0], [Ev - psis - VBO - psiox, Ev - psis - VBO], 'r')
plt.plot([-toxnm, 0], [Ec - psis + CBO - psiox, Ec - psis + CBO], 'r')

# plot the gate's Fermi level (???)
plt.plot(
    [-toxnm - 15, -toxnm], 
    [Ef - phi_ms - psis - psiox, Ef - phi_ms - psis - psiox],
    'k'
)

# ---------------------------------------------
# draw the vacuum level
# ---------------------------------------------
# plot the silicon vacuum level
plt.plot(y, Ec - psi + chi_s, 'k', linewidth=1)

# plot the SiO2 vacuum level
plt.plot(
    [-toxnm, 0], 
    [Ec - psis - psiox + chi_s, Ec - psis + chi_s], 
    'k', linewidth=1
)

# plot the gate's vacuum level
plt.plot(
    [-toxnm - 15, -toxnm], 
    [Ef - phi_ms - psis - psiox + phi_m, Ef - phi_ms - psis - psiox + phi_m],
    'k', linewidth=1
)




# ---------------------------------------------
# create some example plots that lack axes
# ---------------------------------------------
plt.grid(False)
plt.axis('off')

# surface potential
# plt.annotate(
#     '',                            # give the arrow no text
#     xy=(0, Ec + chi_s - psis),             # arrow start point
#     xycoords='data',               # 
#     xytext=(0, Ec + chi_s - psis - 0.5),                # arrow end point
#     textcoords='data',             #
#     arrowprops={
#         'arrowstyle': '->',
#         'connectionstyle': 'arc3'
#     }
# )
# plt.annotate(
#     '',
#     xy=(0, Ec + chi_s),
#     xycoords='data',
#     xytext=(0, Ec + chi_s + 0.5),
#     textcoords='data',
#     arrowprops={
#         'arrowstyle': '->',
#         'connectionstyle': 'arc3'
#     }
# )
plt.annotate(
    '',
    xy=(0, Ec + chi_s),
    xycoords='data',
    xytext=(0, Ec + chi_s - psis),
    textcoords='data',
    arrowprops={
        'arrowstyle': '->',
        'connectionstyle': 'arc3'
    }
)
plt.text(-12, Ec + chi_s - psis / 2, r'$\psi_s$', fontsize=15)

# oxide potential
plt.annotate(
    '', 
    xy=(-toxnm, Ec - psis + chi_s),
    xycoords='data',
    xytext=(-toxnm, Ec - psis + chi_s - psiox),
    textcoords='data',
    arrowprops={
        'arrowstyle': '->',
        'connectionstyle': 'arc3'
    }
)
plt.text(
    -toxnm - 17, 0.5 * (Ec - psis + chi_s + Ec - psis + chi_s - psiox), 
    r'$\psi_{ox}$', fontsize=15
)

# gate-bulk bias
plt.annotate(
    '', 
    xy=(-toxnm - 15, Ef),
    xycoords='data',
    xytext=(-toxnm - 15, Ef - Vgb),
    textcoords='data',
    arrowprops={
        'arrowstyle': '<-',
        'connectionstyle': 'arc3'
    }
)
plt.text(
    -toxnm - 30, 0.5 * (Ef + Ef - Vgb), 
    r'$V_{gb}$', fontsize=15
)

# metal workfunction
plt.annotate(
    '', 
    xy=(-toxnm - 8, Ef - Vgb + phi_m),
    xycoords='data',
    xytext=(-toxnm - 8, Ef - Vgb),
    textcoords='data',
    arrowprops={
        'arrowstyle': '->',
        'connectionstyle': 'arc3'
    }
)
plt.text(
    -toxnm - 20, 0.5 * (Ef + Ef - Vgb + phi_m), 
    r'$\phi_m$', fontsize=15
)

# semiconductor workfunction
plt.annotate(
    '', 
    xy=(max(y) * 0.7, Ef + phi_s),
    xycoords='data',
    xytext=(max(y) * 0.7, Ef),
    textcoords='data',
    arrowprops={
        'arrowstyle': '<-',
        'connectionstyle': 'arc3'
    }
)
plt.text(
    max(y) * 0.7 - 15, 0.5 * (Ef + Ef + phi_s), 
    r'$\phi_s$', fontsize=15
)

# dotted lines
plt.plot([0, max(y)], [Ec + chi_s, Ec + chi_s], 'k--', linewidth=0.5)
plt.plot(
    [-toxnm, 0], 
    [Ec - psis + chi_s, Ec - psis + chi_s], 
    'k--', linewidth=0.5
)
plt.plot([-toxnm - 15, max(y)], [Ef, Ef], 'k--', linewidth=0.5)

# nickel
plt.text(-toxnm - 25, Ev - psis - VBO - 1, 'nickel', fontsize=12)
#sio2
plt.text(-toxnm + 5, Ev - psis - VBO - 1, 'SiO2', fontsize=12)
#si
plt.text(max(y) / 3, Ev - psis - VBO - 1, 'silicon', fontsize=12)
# Ec
plt.text(max(y) * 0.8 , Ec + chi_s + 0.2, r'$E_{VAC}$', fontsize=15)


plt.tight_layout()
