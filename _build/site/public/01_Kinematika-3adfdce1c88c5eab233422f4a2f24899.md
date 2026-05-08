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

# Kinematika pohybu vozidla

Tento notebook sa venuje základným pojmom kinematiky: pohybu s konštantnou 
rýchlosťou, rovnomerne zrýchlenému pohybu a brzdeniu vozidla.

Pomocou interaktívnych sliderov môžeš meniť hodnoty fyzikálnych veličín 
a sledovať, ako sa okamžite zmenia grafy závislostí polohy, rýchlosti 
a zrýchlenia od času.

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
tags: [hide-input]
---
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display
%matplotlib inline

# Tmavý štýl pre všetky grafy
plt.style.use('dark_background')
```

## Rovnomerne zrýchlený pohyb

Pohyb vozidla opisujú tri základné rovnice kinematiky:

- Poloha: $s(t) = s_0 + v_0 \cdot t + \frac{1}{2} \cdot a \cdot t^2$
- Rýchlosť: $v(t) = v_0 + a \cdot t$
- Zrýchlenie: $a(t) = a = \text{konst.}$

kde $v_0$ je počiatočná rýchlosť a $a$ je zrýchlenie.

```{code-cell} ipython3
def zobraz_kinematiku(v0_kmh, a, t_max, jednotky):
    v0 = v0_kmh / 3.6
    t = np.linspace(0, t_max, 500)
    
    s = v0 * t + 0.5 * a * t**2
    v = v0 + a * t
    v_kmh = v * 3.6
    acc = np.full_like(t, a)
    
    mask = v >= 0
    t = t[mask]
    s = s[mask]
    v_kmh = v_kmh[mask]
    acc = acc[mask]
    
    # Prepočet jednotiek polohy
    if jednotky == 'km':
        s_plot = s / 1000
        s_label = 'Poloha s (km)'
    else:
        s_plot = s
        s_label = 'Poloha s (m)'
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    fig.suptitle(f'Kinematika pohybu  |  v₀ = {v0_kmh} km/h  |  a = {a} m/s²', 
                 fontsize=13, color='white')
    
    ax1.plot(t, s_plot, color='#00BFFF', linewidth=2)
    ax1.set_ylabel(s_label, color='white')
    ax1.set_title('Závislosť polohy od času', color='#aaaaaa', fontsize=10)
    ax1.grid(True, alpha=0.2)
    ax1.fill_between(t, s_plot, alpha=0.15, color='#00BFFF')
    
    ax2.plot(t, v_kmh, color='#FFA500', linewidth=2)
    ax2.set_ylabel('Rýchlosť v (km/h)', color='white')
    ax2.set_title('Závislosť rýchlosti od času', color='#aaaaaa', fontsize=10)
    ax2.grid(True, alpha=0.2)
    ax2.fill_between(t, v_kmh, alpha=0.15, color='#FFA500')
    
    ax3.plot(t, acc, color='#90EE90', linewidth=2)
    ax3.set_ylabel('Zrýchlenie a (m/s²)', color='white')
    ax3.set_xlabel('Čas t (s)', color='white')
    ax3.set_title('Závislosť zrýchlenia od času', color='#aaaaaa', fontsize=10)
    ax3.grid(True, alpha=0.2)
    ax3.fill_between(t, acc, alpha=0.15, color='#90EE90')
    
    plt.tight_layout()
    plt.show()

widgets.interact(
    zobraz_kinematiku,
    v0_kmh=widgets.FloatSlider(
        value=50, min=0, max=130, step=5,
        description='v₀ (km/h):',
        style={'description_width': '100px'},
        layout=widgets.Layout(width='500px')
    ),
    a=widgets.FloatSlider(
        value=-3, min=-10, max=5, step=0.5,
        description='a (m/s²):',
        style={'description_width': '100px'},
        layout=widgets.Layout(width='500px')
    ),
    t_max=widgets.FloatSlider(
        value=10, min=2, max=30, step=1,
        description='Čas (s):',
        style={'description_width': '100px'},
        layout=widgets.Layout(width='500px')
    ),
    jednotky=widgets.RadioButtons(
        options=['m', 'km'],
        value='m',
        description='Jednotky:',
        style={'description_width': '100px'}
    )
)
```

## Brzdná dráha

Brzdná dráha závisí od počiatočnej rýchlosti kvadraticky. To znamená, 
že pri dvojnásobnej rýchlosti je brzdná dráha **štvornásobná**.

$$s_{brzdenie} = \frac{v_0^2}{2 \cdot |a|}$$

```{code-cell} ipython3
def zobraz_brzdnu_drahu(a_brzd, jednotky):
    v_kmh = np.linspace(0, 130, 200)
    v_ms = v_kmh / 3.6
    
    s_brzd = v_ms**2 / (2 * abs(a_brzd))
    
    if jednotky == 'km':
        s_plot = s_brzd / 1000
        s_label = 'Brzdná dráha (km)'
    else:
        s_plot = s_brzd
        s_label = 'Brzdná dráha (m)'
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(v_kmh, s_plot, color='#FF6B6B', linewidth=2.5)
    ax.fill_between(v_kmh, s_plot, alpha=0.15, color='#FF6B6B')
    
    for v_ref in [50, 90, 130]:
        s_ref = (v_ref / 3.6)**2 / (2 * abs(a_brzd))
        s_ref_plot = s_ref / 1000 if jednotky == 'km' else s_ref
        jednotka_text = 'km' if jednotky == 'km' else 'm'
        ax.plot(v_ref, s_ref_plot, 'o', color='white', markersize=7)
        ax.annotate(f'{v_ref} km/h\n→ {s_ref_plot:.2f} {jednotka_text}',
                    xy=(v_ref, s_ref_plot),
                    xytext=(v_ref + 3, s_ref_plot + 0.002 if jednotky == 'km' else s_ref_plot + 3),
                    fontsize=9, color='white')
    
    ax.set_xlabel('Počiatočná rýchlosť (km/h)', color='white')
    ax.set_ylabel(s_label, color='white')
    ax.set_title(f'Brzdná dráha v závislosti od rýchlosti  |  spomalenie = {a_brzd} m/s²',
                 color='white')
    ax.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.show()

widgets.interact(
    zobraz_brzdnu_drahu,
    a_brzd=widgets.FloatSlider(
        value=6, min=2, max=12, step=0.5,
        description='Spomalenie (m/s²):',
        style={'description_width': '150px'},
        layout=widgets.Layout(width='500px')
    ),
    jednotky=widgets.RadioButtons(
        options=['m', 'km'],
        value='m',
        description='Jednotky:',
        style={'description_width': '100px'}
    )
)
```

## Zastavovacia vzdialenosť

Celková zastavovacia vzdialenosť sa skladá z dvoch častí:

1. **Reakčná vzdialenosť** – vzdialenosť prejdená počas reakčného času vodiča (typicky 1 sekunda)
2. **Brzdná dráha** – vzdialenosť prejdená počas samotného brzdenia

$$s_{celková} = s_{reakcia} + s_{brzdenie} = v_0 \cdot t_{reakcia} + \frac{v_0^2}{2 \cdot |a|}$$

Zadaj svoju rýchlosť a zisti, za akú vzdialenosť sa vozidlo zastaví.

```{code-cell} ipython3
def vypocet_zastavovacia(v0_kmh, t_reakcia, a_brzd, jednotky):
    v0_ms = v0_kmh / 3.6
    
    # Výpočet vzdialeností
    s_reakcia = v0_ms * t_reakcia
    s_brzdenie = v0_ms**2 / (2 * abs(a_brzd))
    s_celkova = s_reakcia + s_brzdenie
    
    # Prepočet jednotiek
    if jednotky == 'km':
        s_r = s_reakcia / 1000
        s_b = s_brzdenie / 1000
        s_c = s_celkova / 1000
        j = 'km'
    else:
        s_r = s_reakcia
        s_b = s_brzdenie
        s_c = s_celkova
        j = 'm'
    
    # Vizualizácia ako horizontálny pruh
    fig, ax = plt.subplots(figsize=(10, 3))
    
    ax.barh(['Vzdialenosť'], [s_r], color='#FFA500', 
            label=f'Reakčná vzdialenosť: {s_r:.2f} {j}', height=0.4)
    ax.barh(['Vzdialenosť'], [s_b], left=[s_r], color='#FF6B6B',
            label=f'Brzdná dráha: {s_b:.2f} {j}', height=0.4)
    
    ax.set_xlabel(f'Vzdialenosť ({j})', color='white')
    ax.set_title(f'Zastavovacia vzdialenosť pri {v0_kmh} km/h  |  Celková: {s_c:.2f} {j}',
                 color='white', fontsize=12)
    ax.legend(loc='lower right', fontsize=9)
    ax.grid(True, alpha=0.2, axis='x')
    
    plt.tight_layout()
    plt.show()
    
    # Textový výstup
    print(f'─' * 45)
    print(f'  Rýchlosť:               {v0_kmh} km/h')
    print(f'  Reakčný čas:            {t_reakcia} s')
    print(f'  Brzdné spomalenie:      {a_brzd} m/s²')
    print(f'─' * 45)
    print(f'  Reakčná vzdialenosť:    {s_r:.2f} {j}')
    print(f'  Brzdná dráha:           {s_b:.2f} {j}')
    print(f'  ══════════════════════════════════════')
    print(f'  CELKOVÁ vzdialenosť:    {s_c:.2f} {j}')
    print(f'─' * 45)

widgets.interact(
    vypocet_zastavovacia,
    v0_kmh=widgets.FloatSlider(
        value=90, min=10, max=200, step=5,
        description='Rýchlosť (km/h):',
        style={'description_width': '150px'},
        layout=widgets.Layout(width='500px')
    ),
    t_reakcia=widgets.FloatSlider(
        value=1.0, min=0.5, max=3.0, step=0.1,
        description='Reakčný čas (s):',
        style={'description_width': '150px'},
        layout=widgets.Layout(width='500px')
    ),
    a_brzd=widgets.FloatSlider(
        value=6, min=2, max=12, step=0.5,
        description='Spomalenie (m/s²):',
        style={'description_width': '150px'},
        layout=widgets.Layout(width='500px')
    ),
    jednotky=widgets.RadioButtons(
        options=['m', 'km'],
        value='m',
        description='Jednotky:',
        style={'description_width': '100px'}
    )
)
```

```{code-cell} ipython3

```
