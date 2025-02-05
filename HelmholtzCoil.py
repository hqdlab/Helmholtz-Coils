# -*- coding: utf-8 -*-
"""
@version: 1.0.0
@date: 2025-02-05
@author: johannes@majer.ch, HQDLab, USTC

This modules calculates magnetic fields of current loops, Helmholtz coils and anti-Helmholtz coils.

Please read the document 'Helmholtz Coils Theory.pdf' dated February 5, 2025 for reference.

FieldXXX
    functions starting with FieldXXX calculate the field without the factor mu0*I/(2*R)

MagneticFieldXXX
    functions starting MagneticFieldXXX calculate magnetic fields in units of Tesla.
    mu0*I/(2*R)*FieldXXX

"""


import numpy as np
import scipy


# vacuum permeability
#   unit: Henry / Meter = Newton / Ampere^2 = Tesla * Meter / Ampere
mu0 = 4*np.pi*1e-7



# ---------------------
# Current Loop
# ---------------------

def FieldLoopBz(z, rho, R=1):
    ksq = 4*R*rho/((R+rho)**2+z**2)
    K = scipy.special.ellipk(ksq)
    E = scipy.special.ellipe(ksq)
    return R/(np.pi*(np.sqrt((R+rho)**2+z**2)))*(K + E*(R**2-rho**2-z**2)/((R-rho)**2+z**2))


def MagneticFieldLoopBz(z, rho, R, I):
    # refere to equation (3)
    return mu0*I/(2*R)*FieldLoopBz(z, rho, R)


def FieldLoopBrho(z, rho, R=1):
    if rho == 0:
        return 0
    ksq = 4*R*rho/((R+rho)**2+z**2)
    K = scipy.special.ellipk(ksq)
    E = scipy.special.ellipe(ksq)
    return (R*z)/(np.pi*rho*(np.sqrt((R+rho)**2+z**2)))*(-K + E*(R**2+rho**2+z**2)/((R-rho)**2+z**2))


def MagneticFieldLoopBrho(z, rho, R, I):
    # refere to equation (4)
    return mu0*I/(2*R)*FieldLoopBrho(z, rho, R)


def FieldLoopOnAxis(z, R=1):
    return R**3/(R**2+z**2)**(3/2)


def MagneticFieldLoopOnAxis(z, R, I):
    # refere to equation (1)
    return mu0*I/(2*R)*FieldLoopOnAxis(z,R)


def FieldLoopDiscrete(z, rho, N=360):
    # this function approximates the loop with N straight wires
    # it returns the field as vector (f_rho, f_phi, f_z)
    bf = np.array([0, 0, 0])
    if z == 0 and abs(rho)== 1:
        return bf
    for i in range(N):
        theta0 = i*2*np.pi/N
        theta1 = theta0+2*np.pi/N
        dl = np.array([np.cos(theta1) - np.cos(theta0), np.sin(theta1) - np.sin(theta0), 0])
        s = np.array([rho-np.cos(theta0), -np.sin(theta0), z])
        ns = np.linalg.norm(s)
        dbf = np.cross(dl, s)/ns**3
        bf = bf + dbf
    bf = bf / (2*np.pi)
    return bf



# ---------------------
# Helmholtz Coil
# ---------------------

def FieldHelmholtzOnAxis(z, R=1):
    return R**3/(R**2+(z+R/2)**2)**(3/2) + R**3/(R**2+(z-R/2)**2)**(3/2)


def MagneticFieldHelmholtzOnAxis(z, R, I):
    # refere to equation (5)
    return mu0*I/(2*R)*FieldHelmholtzOnAxis(z,R)



def FieldHelmholtzBz(z, rho, R=1):
    return FieldLoopBz(z+R/2, rho, R) + FieldLoopBz(z-R/2, rho, R)


def MagneticFieldHelmholtzBz(z, rho, R, I):
    return mu0*I/(2*R)*FieldHelmholtzBz(z, rho, R)



def FieldHelmholtzBrho(z, rho, R=1):
    return FieldLoopBro(z+R/2, rho, R) + FieldLoopBrho(z-R/2, rho, R)


def MagneticFieldHelmholtzBrho(z, rho, R, I):
    return mu0*I/(2*R)*FieldHelmholtzBrho(z, rho, R)



# ---------------------
# Anti Helmholtz Coil
# ---------------------

def FieldAntiHelmholtzOnAxis(z, R=1):
    return R**3/(R**2+(z+R/2)**2)**(3/2) - R**3/(R**2+(z-R/2)**2)**(3/2)


def MagneticFieldAntiHelmholtzOnAxis(z, R, I):
    # refere to equation (7)
    return mu0*I/(2*R)*FieldAntiHelmholtzOnAxis(z,R)



def FieldAntiHelmholtzBz(z, rho, R=1):
    return FieldLoopBz(z+R/2, rho, R) - FieldLoopBz(z-R/2, rho, R)


def MagneticFieldAntiHelmholtzBz(z, rho, R, I):
    return mu0*I/(2*R)*FieldAntiHelmholtzBz(z, rho, R)



def FieldAntiHelmholtzBrho(z, rho, R=1):
    return FieldLoopBro(z+R/2, rho, R) - FieldLoopBrho(z-R/2, rho, R)


def MagneticFieldAntiHelmholtzBrho(z, rho, R, I):
    return mu0*I/(2*R)*FieldAntiHelmholtzBrho(z, rho, R)
