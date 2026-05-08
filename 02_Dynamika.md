---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.19.1
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Dynamika pohybu vozidla

### Dynamika sa zaoberá príčinami pohybu, teda silami ktoré pohyb spôsobujú alebo brzdia. V tomto notebooku aplikujeme Newtonove zákony na reálne vozidlo a skúmame vzťah medzi silou, hmotnosťou a zrýchlením.

Pomocou interaktívnych sliderov môžeš meniť parametre vozidla a sledovať 
ako sa okamžite zmenia silové pomery aj výsledné zrýchlenie.

+++

## Teoretický základ

### Na pohybujúce sa vozidlo pôsobia tri hlavné sily:

**Hnacia sila motora:**
$$F_{motor} = \frac{P}{v}$$

**Aerodynamický odpor:**
$$F_{vzduch} = \frac{1}{2} \cdot \rho \cdot C_d \cdot A \cdot v^2$$

**Valivý odpor:**
$$F_{valivý} = \mu \cdot m \cdot g$$

**Výsledné zrýchlenie** podľa Newtonovho druhého zákona:
$$a = \frac{F_{motor} - F_{vzduch} - F_{valivý}}{m}$$

Vozidlo dosiahne maximálnu rýchlosť keď $F_{motor} = F_{vzduch} + F_{valivý}$.

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import ipywidgets as widgets
from IPython.display import display, clear_output

%matplotlib inline
plt.style.use('dark_background')

# Fyzikálne konštanty
RHO = 1.225   # hustota vzduchu [kg/m³]
G   = 9.81    # gravitačné zrýchlenie [m/s²]
A   = 2.2     # čelná plocha vozidla [m²]
```

## Interaktívna analýza síl

Nastav parametre vozidla pomocou sliderov a sleduj ako sa menia 
silové pomery aj výsledné zrýchlenie.

```{code-cell} ipython3
def kresli_diagram(ax, F_m, F_v, F_val, v_val):
    ax.set_xlim(-7, 7)
    ax.set_ylim(-2.5, 3.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor('#1a1a2e')
    ax.set_title(f'Silový diagram pri v = {v_val:.0f} km/h',
                 color='white', fontsize=10, pad=8)

    # Karoséria
    ax.add_patch(patches.FancyBboxPatch(
        (-2.2, 0.1), 4.4, 1.3,
        boxstyle="round,pad=0.2",
        linewidth=2, edgecolor='#777777', facecolor='#2d2d44'))

    # Okná
    for xo in [-1.9, 0.2]:
        ax.add_patch(patches.FancyBboxPatch(
            (xo, 1.0), 1.3, 0.75,
            boxstyle="round,pad=0.06",
            linewidth=1, edgecolor='#444444', facecolor='#1a3a5c'))

    # Kolesá
    for cx in [-1.5, 1.5]:
        ax.add_patch(plt.Circle((cx, -0.12), 0.42, color='#2a2a2a', zorder=3))
        ax.add_patch(plt.Circle((cx, -0.12), 0.25, color='#555555', zorder=4))

    # Škálovanie šípok
    max_F = max(F_m, F_v + F_val, 1)
    sc    = 4.0 / max_F

    # Hnacia sila - modrá šípka doprava
    ax.annotate('', xy=(2.2 + F_m * sc, 0.75), xytext=(2.2, 0.75),
                arrowprops=dict(arrowstyle='->', color='#00BFFF',
                                lw=3, mutation_scale=20))
    ax.text(2.2 + F_m * sc / 2, 1.1,
            f'$F_{{motor}}$\n{F_m:.0f} N',
            color='#00BFFF', fontsize=9, ha='center', fontweight='bold')

    # Aerodyn. odpor - červená šípka doľava
    ax.annotate('', xy=(-2.2 - F_v * sc, 0.75), xytext=(-2.2, 0.75),
                arrowprops=dict(arrowstyle='->', color='#FF4444',
                                lw=3, mutation_scale=20))
    ax.text(-2.2 - F_v * sc / 2, 1.1,
            f'$F_{{vzduch}}$\n{F_v:.0f} N',
            color='#FF4444', fontsize=9, ha='center', fontweight='bold')

    # Valivý odpor - oranžová šípka nadol
    fvs = min(F_val * sc * 2.5, 1.3)
    for cx in [-1.5, 1.5]:
        ax.annotate('', xy=(cx, -0.12 - fvs), xytext=(cx, -0.12),
                    arrowprops=dict(arrowstyle='->', color='#FFA500',
                                    lw=2.2, mutation_scale=16))
    ax.text(0, -0.12 - fvs - 0.4,
            f'$F_{{valivý}}$ = {F_val:.0f} N',
            color='#FFA500', fontsize=9, ha='center', fontweight='bold')

    # Výsledná sila
    F_res = F_m - F_v - F_val
    if abs(F_res) > 20:
        farba = '#00FF88' if F_res > 0 else '#FF4444'
        smer  = '→  ZRÝCHLENIE' if F_res > 0 else '←  SPOMALENIE'
        text  = f'Výsledná sila: {F_res:.0f} N   {smer}'
    else:
        farba = '#FFD700'
        text  = 'Silová rovnováha  │  dosiahnutá $v_{max}$'

    ax.text(0, 3.0, text, color=farba, fontsize=10, ha='center',
            fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#0d0d1a',
                      edgecolor=farba, alpha=0.9))


out = widgets.Output()

def zobraz(m, P_kW, Cd, mu):
    P     = P_kW * 1000
    v     = np.linspace(0.5, 90, 800)
    v_kmh = v * 3.6

    F_motor  = P / v
    F_vzduch = 0.5 * RHO * Cd * A * v**2
    F_valivý = mu * m * G * np.ones_like(v)
    F_odpor  = F_vzduch + F_valivý
    F_celk   = F_motor - F_odpor
    a        = np.clip(F_celk / m, -25, 25)

    idx_vmax = np.argmin(np.abs(F_celk))
    v_max    = v_kmh[idx_vmax]

    # Hodnoty pre silový diagram pri polovici v_max
    v_diag   = max(v_max / 2, 10) / 3.6
    F_m_diag = P / v_diag
    F_v_diag = 0.5 * RHO * Cd * A * v_diag**2
    F_val_d  = mu * m * G

    with out:
        clear_output(wait=True)

        fig = plt.figure(figsize=(13, 10))
        fig.patch.set_facecolor('#0d0d1a')

        ax_d = fig.add_axes([0.05, 0.55, 0.90, 0.38])
        ax1  = fig.add_axes([0.07, 0.08, 0.42, 0.38])
        ax2  = fig.add_axes([0.57, 0.08, 0.42, 0.38])

        ax_d.set_facecolor('#1a1a2e')
        kresli_diagram(ax_d, F_m_diag, F_v_diag, F_val_d, v_max / 2)

        # Graf síl
        ax1.set_facecolor('#0d0d1a')
        ax1.plot(v_kmh, F_motor,  color='#00BFFF', lw=2.2, label='Hnacia sila')
        ax1.plot(v_kmh, F_vzduch, color='#FF4444', lw=2.2, label='Aerodyn. odpor')
        ax1.plot(v_kmh, F_valivý, color='#FFA500', lw=2.0,
                 linestyle='--', label='Valivý odpor')
        ax1.plot(v_kmh, F_odpor,  color='#FF0000', lw=2.0,
                 linestyle=':', label='Celkový odpor')
        ax1.axvline(x=v_max, color='#FFD700', lw=1.8, linestyle='--',
                    alpha=0.8, label=f'v_max ≈ {v_max:.0f} km/h')
        ax1.fill_between(v_kmh, F_motor, F_odpor,
                         where=(F_motor >= F_odpor),
                         alpha=0.10, color='#00BFFF', label='Zóna zrýchlenia')
        ax1.fill_between(v_kmh, F_motor, F_odpor,
                         where=(F_motor < F_odpor),
                         alpha=0.10, color='#FF4444', label='Zóna spomalenia')
        ax1.set_xlabel('Rýchlosť (km/h)', color='#cccccc')
        ax1.set_ylabel('Sila (N)', color='#cccccc')
        ax1.set_title('Silová analýza', color='white', fontsize=11)
        ax1.legend(fontsize=8, loc='upper right',
                   facecolor='#1a1a2e', edgecolor='#555555')
        ax1.grid(True, alpha=0.12)
        ax1.set_ylim(bottom=0)
        ax1.set_xlim(left=0)
        ax1.tick_params(colors='#aaaaaa')

        # Graf zrýchlenia
        ax2.set_facecolor('#0d0d1a')
        ax2.plot(v_kmh, a, color='#00FF88', lw=2.5)
        ax2.axhline(y=0, color='white', lw=1, linestyle='--', alpha=0.4)
        ax2.axvline(x=v_max, color='#FFD700', lw=1.8, linestyle='--',
                    alpha=0.8, label=f'v_max ≈ {v_max:.0f} km/h')
        ax2.fill_between(v_kmh, a, 0, where=(a >= 0),
                         alpha=0.15, color='#00FF88', label='Zrýchlenie')
        ax2.fill_between(v_kmh, a, 0, where=(a < 0),
                         alpha=0.15, color='#FF4444', label='Spomalenie')
        ax2.set_xlabel('Rýchlosť (km/h)', color='#cccccc')
        ax2.set_ylabel('Zrýchlenie (m/s²)', color='#cccccc')
        ax2.set_title('Zrýchlenie vozidla', color='white', fontsize=11)
        ax2.legend(fontsize=8, facecolor='#1a1a2e', edgecolor='#555555')
        ax2.grid(True, alpha=0.12)
        ax2.set_xlim(left=0)
        ax2.tick_params(colors='#aaaaaa')

        fig.suptitle(
            f'Dynamika vozidla  │  m = {m} kg  │  P = {P_kW} kW ({P_kW*1.36:.0f} PS)'
            f'  │  Cd = {Cd}  │  v_max ≈ {v_max:.0f} km/h',
            fontsize=12, color='white', y=0.97
        )
        plt.show()

        print(f'{"═"*48}')
        print(f'  Hmotnosť:            {m} kg')
        print(f'  Výkon motora:        {P_kW} kW  ({P_kW*1.36:.0f} PS)')
        print(f'  Koef. odporu Cd:     {Cd}')
        print(f'  Valivý odpor μ:      {mu}')
        print(f'{"─"*48}')
        print(f'  Maximálna rýchlosť:  ≈ {v_max:.0f} km/h')
        print(f'{"═"*48}')


widgets.interact(
    zobraz,
    m=widgets.IntSlider(
        value=1400, min=800, max=3500, step=50,
        description='Hmotnosť (kg):',
        style={'description_width': '150px'},
        layout=widgets.Layout(width='500px')),
    P_kW=widgets.IntSlider(
        value=100, min=30, max=400, step=10,
        description='Výkon (kW):',
        style={'description_width': '150px'},
        layout=widgets.Layout(width='500px')),
    Cd=widgets.FloatSlider(
        value=0.30, min=0.15, max=0.60, step=0.01,
        description='Koef. odporu Cd:',
        style={'description_width': '150px'},
        layout=widgets.Layout(width='500px')),
    mu=widgets.FloatSlider(
        value=0.015, min=0.005, max=0.05, step=0.005,
        description='Valivý odpor μ:',
        style={'description_width': '150px'},
        layout=widgets.Layout(width='500px'))
)

display(out)
```

## Záver

Tento notebook ukázal ako Newtonove zákony opisujú pohyb reálneho vozidla.

- Hnacia sila klesá s rastúcou rýchlosťou, aerodynamický odpor naopak rastie kvadraticky
- Maximálna rýchlosť nastane keď sa hnacia sila a celkový odpor vyrovnajú
- Ťažšie vozidlo dosahuje nižšie zrýchlenie pri rovnakom výkone motora
- Aerodynamický odpor pri vysokých rýchlostiach dominuje nad ostatnými odpormi
