import matplotlib.pyplot as plt
import numpy as np

def nacrtaj_kvadrat():
    fig, ax = plt.subplots()
    kvadrat = plt.Rectangle((0, 0), 1, 1, edgecolor='blue', facecolor='lightblue')
    ax.add_patch(kvadrat)
    ax.set_xlim(-0.2, 1.2)
    ax.set_ylim(-0.2, 1.2)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig

def nacrtaj_pravougaonik():
    fig, ax = plt.subplots()
    pravougaonik = plt.Rectangle((0, 0), 2, 1, edgecolor='green', facecolor='lightgreen')
    ax.add_patch(pravougaonik)
    ax.set_xlim(-0.2, 2.2)
    ax.set_ylim(-0.2, 1.2)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig

def nacrtaj_krug():
    fig, ax = plt.subplots()
    krug = plt.Circle((0.5, 0.5), 0.5, edgecolor='red', facecolor='mistyrose')
    ax.add_patch(krug)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig
