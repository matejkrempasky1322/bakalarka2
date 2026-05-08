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

# Kmitanie mechanickej sústavy

Kmitanie je periodický pohyb telesa okolo rovnovážnej polohy. 
V strojárstve sa stretávame s kmitaním pri vibráciách motorov, 
podvozkov vozidiel, mostov či strojných súčastí. Pochopenie 
tlmeného kmitania je kľúčové pri návrhu tlmičov a pružín.

V tomto notebooku riešime pohybovú rovnicu tlmeného harmonického 
oscilátora numericky pomocou knižnice SciPy a vizualizujeme 
prechod medzi rôznymi režimami tlmenia.

+++

## Teoretický základ

Pohybová rovnica tlmeného harmonického oscilátora:

$$m \cdot \ddot{x} + b \cdot \dot{x} + k \cdot x = 0$$

kde:
- $m$ – hmotnosť telesa [kg]
- $b$ – koeficient tlmenia [N·s/m]
- $k$ – tuhosť pružiny [N/m]
- $x$ – výchylka od rovnovážnej polohy [m]

**Vlastná uhlová frekvencia:**
$$\omega_0 = \sqrt{\frac{k}{m}}$$

**Kritické tlmenie:**
$$b_{krit} = 2 \cdot \sqrt{k \cdot m}$$

Podľa pomeru $b$ a $b_{krit}$ rozlišujeme tri režimy:

| Režim | Podmienka | Popis |
|-------|-----------|-------|
| Podtlmený | $b < b_{krit}$ | Sústava kmitá s klesajúcou amplitúdou |
| Kriticky tlmený | $b = b_{krit}$ | Najrýchlejší návrat bez kmitania |
| Pretlmený | $b > b_{krit}$ | Pomalý návrat bez kmitania |

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from scipy.integrate import solve_ivp
from IPython.display import display, clear_output

%matplotlib inline
plt.style.use('dark_background')
```

## Interaktívna simulácia tlmeného oscilátora

Nastav parametre sústavy a sleduj ako sa mení charakter kmitania. 
Skús postupne zvyšovať tlmenie od podtlmeného režimu cez kritický 
až po pretlmený a sleduj rozdiel v priebehu pohybu.

```{code-cell} ipython3
out = widgets.Output()

def zobraz_kmitanie(m, k, b, x0, v0):
    # Kritické tlmenie
    b_krit = 2 * np.sqrt(k * m)
    omega0 = np.sqrt(k / m)
    pomer  = b / b_krit

    # Určenie režimu tlmenia
    if pomer < 0.99:
        rezim = 'PODTLMENÝ'
        farba_rezim = '#00FF88'
    elif pomer <= 1.01:
        rezim = 'KRITICKY TLMENÝ'
        farba_rezim = '#FFD700'
    else:
        rezim = 'PRETLMENÝ'
        farba_rezim = '#FF6B6B'

    # Numerické riešenie pohybovej rovnice cez SciPy
    def pohybova_rovnica(t, y):
        x, v = y
        dxdt = v
        dvdt = (-b * v - k * x) / m
        return [dxdt, dvdt]

    # Časový rozsah simulácie
    T_kyvov = 2 * np.pi / omega0
    t_max   = max(15 * T_kyvov, 5)
    t_span  = (0, t_max)
    t_eval  = np.linspace(0, t_max, 2000)

    # Riešenie
    sol = solve_ivp(
        pohybova_rovnica,
        t_span,
        [x0, v0],
        t_eval=t_eval,
        method='RK45',
        rtol=1e-8
    )

    t = sol.t
    x = sol.y[0]
    v = sol.y[1]

    # Obálka exponenciálneho útlmu (len pre podtlmený režim)
    if pomer < 1:
        alpha  = b / (2 * m)
        obalka = x0 * np.exp(-alpha * t)

    with out:
        clear_output(wait=True)

        fig = plt.figure(figsize=(13, 10))
        fig.patch.set_facecolor('#0d0d1a')

        ax1 = fig.add_axes([0.07, 0.55, 0.55, 0.38])
        ax2 = fig.add_axes([0.68, 0.55, 0.28, 0.38])
        ax3 = fig.add_axes([0.07, 0.08, 0.55, 0.35])
        ax4 = fig.add_axes([0.68, 0.08, 0.28, 0.35])

        # ── Graf výchylky ────────────────────────────────────────
        ax1.set_facecolor('#0d0d1a')
        ax1.plot(t, x, color='#00BFFF', linewidth=2.2,
                 label='Výchylka x(t)')
        ax1.axhline(y=0, color='white', linewidth=1,
                    linestyle='--', alpha=0.3)

        if pomer < 1:
            ax1.plot(t,  obalka, color='#FFD700', linewidth=1.5,
                     linestyle='--', alpha=0.7, label='Obálka útlmu')
            ax1.plot(t, -obalka, color='#FFD700', linewidth=1.5,
                     linestyle='--', alpha=0.7)

        ax1.fill_between(t, x, 0, where=(x >= 0),
                         alpha=0.08, color='#00BFFF')
        ax1.fill_between(t, x, 0, where=(x < 0),
                         alpha=0.08, color='#FF6B6B')
        ax1.set_xlabel('Čas t (s)', color='#cccccc', fontsize=10)
        ax1.set_ylabel('Výchylka x (m)', color='#cccccc', fontsize=10)
        ax1.set_title('Závislosť výchylky od času', color='white',
                      fontsize=11, pad=8)
        ax1.legend(fontsize=9, facecolor='#1a1a2e', edgecolor='#555555')
        ax1.grid(True, alpha=0.12)
        ax1.tick_params(colors='#aaaaaa')

        # ── Fázový diagram x-v ───────────────────────────────────
        ax2.set_facecolor('#0d0d1a')
        body = ax2.scatter(x, v, c=t, cmap='plasma',
                           s=1.5, alpha=0.8)
        ax2.axhline(y=0, color='white', lw=0.8, alpha=0.3)
        ax2.axvline(x=0, color='white', lw=0.8, alpha=0.3)
        ax2.set_xlabel('Výchylka x (m)', color='#cccccc', fontsize=9)
        ax2.set_ylabel('Rýchlosť v (m/s)', color='#cccccc', fontsize=9)
        ax2.set_title('Fázový diagram', color='white', fontsize=11, pad=8)
        ax2.grid(True, alpha=0.12)
        ax2.tick_params(colors='#aaaaaa', labelsize=8)
        plt.colorbar(body, ax=ax2, label='Čas (s)')

        # ── Graf rýchlosti ───────────────────────────────────────
        ax3.set_facecolor('#0d0d1a')
        ax3.plot(t, v, color='#FFA500', linewidth=2.0,
                 label='Rýchlosť v(t)')
        ax3.axhline(y=0, color='white', linewidth=1,
                    linestyle='--', alpha=0.3)
        ax3.fill_between(t, v, 0, where=(v >= 0),
                         alpha=0.08, color='#FFA500')
        ax3.fill_between(t, v, 0, where=(v < 0),
                         alpha=0.08, color='#FF6B6B')
        ax3.set_xlabel('Čas t (s)', color='#cccccc', fontsize=10)
        ax3.set_ylabel('Rýchlosť v (m/s)', color='#cccccc', fontsize=10)
        ax3.set_title('Závislosť rýchlosti od času', color='white',
                      fontsize=11, pad=8)
        ax3.legend(fontsize=9, facecolor='#1a1a2e', edgecolor='#555555')
        ax3.grid(True, alpha=0.12)
        ax3.tick_params(colors='#aaaaaa')

        # ── Porovnanie troch režimov ─────────────────────────────
        ax4.set_facecolor('#0d0d1a')
        t_por = np.linspace(0, t_max, 2000)

        for b_por, farba, nazov in [
            (b_krit * 0.3, '#00FF88', 'Podtlmený'),
            (b_krit * 1.0, '#FFD700', 'Kritický'),
            (b_krit * 3.0, '#FF6B6B', 'Pretlmený')
        ]:
            sol_por = solve_ivp(
                lambda t, y: [y[1], (-b_por * y[1] - k * y[0]) / m],
                (0, t_max), [x0, v0],
                t_eval=t_por, method='RK45'
            )
            ax4.plot(sol_por.t, sol_por.y[0],
                     color=farba, linewidth=1.8,
                     linestyle='-' if nazov == 'Kritický' else '--',
                     label=nazov, alpha=0.85)

        ax4.axhline(y=0, color='white', lw=0.8, alpha=0.3)
        ax4.set_xlabel('Čas t (s)', color='#cccccc', fontsize=9)
        ax4.set_ylabel('Výchylka x (m)', color='#cccccc', fontsize=9)
        ax4.set_title('Porovnanie režimov', color='white',
                      fontsize=11, pad=8)
        ax4.legend(fontsize=8.5, facecolor='#1a1a2e', edgecolor='#555555')
        ax4.grid(True, alpha=0.12)
        ax4.tick_params(colors='#aaaaaa', labelsize=8)

        fig.suptitle(
            f'Tlmený harmonický oscilátor  │  m = {m} kg  │  '
            f'k = {k} N/m  │  b = {b:.1f} N·s/m  │  Režim: {rezim}',
            fontsize=12, color=farba_rezim, y=0.98
        )
        plt.show()

        print(f'{"═"*52}')
        print(f'  Hmotnosť:              {m} kg')
        print(f'  Tuhosť pružiny:        {k} N/m')
        print(f'  Koeficient tlmenia:    {b:.1f} N·s/m')
        print(f'{"─"*52}')
        print(f'  Vlastná frekvencia:    {omega0:.3f} rad/s  '
              f'({omega0/(2*np.pi):.3f} Hz)')
        print(f'  Kritické tlmenie:      {b_krit:.2f} N·s/m')
        print(f'  Pomer b/b_krit:        {pomer:.3f}')
        print(f'{"─"*52}')
        print(f'  Režim tlmenia:         {rezim}')
        print(f'{"═"*52}')


widgets.interact(
    zobraz_kmitanie,
    m=widgets.FloatSlider(
        value=1.0, min=0.1, max=5.0, step=0.1,
        description='Hmotnosť m (kg):',
        style={'description_width': '160px'},
        layout=widgets.Layout(width='500px')),
    k=widgets.FloatSlider(
        value=10.0, min=1.0, max=100.0, step=1.0,
        description='Tuhosť k (N/m):',
        style={'description_width': '160px'},
        layout=widgets.Layout(width='500px')),
    b=widgets.FloatSlider(
        value=1.0, min=0.0, max=30.0, step=0.5,
        description='Tlmenie b (N·s/m):',
        style={'description_width': '160px'},
        layout=widgets.Layout(width='500px')),
    x0=widgets.FloatSlider(
        value=1.0, min=0.1, max=3.0, step=0.1,
        description='Počiat. výchylka (m):',
        style={'description_width': '160px'},
        layout=widgets.Layout(width='500px')),
    v0=widgets.FloatSlider(
        value=0.0, min=-5.0, max=5.0, step=0.1,
        description='Počiat. rýchlosť (m/s):',
        style={'description_width': '160px'},
        layout=widgets.Layout(width='500px'))
)

display(out)
```

## Záver

Tento notebook demonštroval numerické riešenie pohybovej rovnice 
tlmeného harmonického oscilátora pomocou knižnice SciPy.

- Podtlmený režim ($b < b_{krit}$): sústava kmitá s exponenciálne 
  klesajúcou amplitúdou, typický pre nedostatočne tlmený podvozok
- Kriticky tlmený režim ($b = b_{krit}$): najrýchlejší návrat 
  do rovnovážnej polohy bez prekmitovania, ideálny pre tlmiče
- Pretlmený režim ($b > b_{krit}$): pomalý návrat bez kmitania, 
  nevhodný pre podvozkové aplikácie kvôli pomalej odozve

Fázový diagram ukazuje ako sústava stráca energiu a spirálovito 
sa blíži k rovnovážnemu bodu.

```{code-cell} ipython3

```
