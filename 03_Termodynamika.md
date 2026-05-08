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

# Termodynamika spaľovacieho motora

Spaľovací motor je tepelný stroj, ktorý premieňa tepelnú energiu paliva 
na mechanickú prácu. Účinnosť tohto procesu je obmedzená základnými 
zákonmi termodynamiky. V tomto notebooku skúmame Carnotov cyklus ako 
ideálny model tepelného stroja a vizualizujeme ho prostredníctvom 
animovaného p-V diagramu.

+++

## Teoretický základ

**Carnotov cyklus** pozostáva zo štyroch dejov:

1. **Izotermická expanzia** pri teplote $T_H$ – plyn prijíma teplo $Q_H$
2. **Adiabatická expanzia** – plyn sa ochladzuje z $T_H$ na $T_C$
3. **Izotermická kompresia** pri teplote $T_C$ – plyn odovzdáva teplo $Q_C$
4. **Adiabatická kompresia** – plyn sa ohrieva z $T_C$ na $T_H$

**Tepelná účinnosť** Carnotovho cyklu:
$$\eta = 1 - \frac{T_C}{T_H}$$

kde $T_H$ je teplota teplého zásobníka a $T_C$ je teplota studeného zásobníka, 
obe v Kelvinoch. Táto účinnosť predstavuje teoretický maximálny limit, 
ktorý nemôže prekonať žiadny reálny tepelný stroj pracujúci medzi 
týmito dvoma teplotami.

**Prepočet teplôt:**
$$T[K] = T[°C] + 273{,}15$$

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import ipywidgets as widgets
from IPython.display import display, HTML, clear_output

%matplotlib inline
plt.style.use('dark_background')
```

## Interaktívny p-V diagram a výpočet účinnosti

Nastav teploty zásobníkov a sleduj ako sa mení tvar Carnotovho cyklu 
v p-V diagrame aj hodnota tepelnej účinnosti.

```{code-cell} ipython3
def carnotov_cyklus(T_H, T_C, n=1, R=8.314, V1=1.0, V2=3.0, gamma=1.4):
    V_1 = V1
    p_1 = n * R * T_H / V_1
    V_2 = V2
    p_2 = n * R * T_H / V_2
    V_3 = V_2 * (T_H / T_C) ** (1 / (gamma - 1))
    p_3 = n * R * T_C / V_3
    V_4 = V_1 * (T_H / T_C) ** (1 / (gamma - 1))
    p_4 = n * R * T_C / V_4

    V_12 = np.linspace(V_1, V_2, 200)
    p_12 = n * R * T_H / V_12
    V_23 = np.linspace(V_2, V_3, 200)
    p_23 = p_2 * (V_2 / V_23) ** gamma
    V_34 = np.linspace(V_3, V_4, 200)
    p_34 = n * R * T_C / V_34
    V_41 = np.linspace(V_4, V_1, 200)
    p_41 = p_4 * (V_4 / V_41) ** gamma

    body = {'V': [V_1, V_2, V_3, V_4], 'p': [p_1, p_2, p_3, p_4]}
    vetvy = [
        (V_12, p_12, '#00BFFF', '1→2  Izotermická expanzia ($T_H$)'),
        (V_23, p_23, '#00FF88', '2→3  Adiabatická expanzia'),
        (V_34, p_34, '#FF6B6B', '3→4  Izotermická kompresia ($T_C$)'),
        (V_41, p_41, '#FFA500', '4→1  Adiabatická kompresia'),
    ]
    return body, vetvy


out = widgets.Output()

def zobraz_cyklus(T_H_C, T_C_C):
    T_H = T_H_C + 273.15
    T_C = T_C_C + 273.15

    if T_C >= T_H:
        with out:
            clear_output(wait=True)
            print("Teplota studeného zásobníka musí byť nižšia ako teplého!")
        return

    eta = 1 - T_C / T_H
    body, vetvy = carnotov_cyklus(T_H, T_C)

    with out:
        clear_output(wait=True)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
        fig.patch.set_facecolor('#0d0d1a')

        ax1.set_facecolor('#0d0d1a')
        for V, p, farba, label in vetvy:
            ax1.plot(V, p, color=farba, linewidth=2.5, label=label)

        for i, (V, p, farba, _) in enumerate(vetvy):
            mid = len(V) // 2
            ax1.annotate('',
                xy=(V[mid+2], p[mid+2]), xytext=(V[mid-2], p[mid-2]),
                arrowprops=dict(arrowstyle='->', color=farba,
                                lw=2, mutation_scale=15))

        for i, (vb, pb) in enumerate(zip(body['V'], body['p'])):
            ax1.plot(vb, pb, 'o', color='white', markersize=8, zorder=5)
            ax1.text(vb + 0.05, pb + 0.02,
                     f'  {i+1}', color='white', fontsize=11, fontweight='bold')

        V_uzavr = np.concatenate([vetvy[0][0], vetvy[1][0],
                                   vetvy[2][0], vetvy[3][0]])
        p_uzavr = np.concatenate([vetvy[0][1], vetvy[1][1],
                                   vetvy[2][1], vetvy[3][1]])
        ax1.fill(V_uzavr, p_uzavr, alpha=0.12, color='#FFD700')

        ax1.set_xlabel('Objem V (×10⁻³ m³)', color='#cccccc', fontsize=11)
        ax1.set_ylabel('Tlak p (kPa)', color='#cccccc', fontsize=11)
        ax1.set_title('Carnotov cyklus – p-V diagram', color='white',
                      fontsize=12, pad=10)
        ax1.legend(fontsize=8.5, facecolor='#1a1a2e',
                   edgecolor='#555555', framealpha=0.9)
        ax1.grid(True, alpha=0.12)
        ax1.tick_params(colors='#aaaaaa')
        ax1.text(0.02, 0.97, f'$T_H$ = {T_H_C} °C  ({T_H:.0f} K)',
                 transform=ax1.transAxes, color='#00BFFF', fontsize=9, va='top')
        ax1.text(0.02, 0.91, f'$T_C$ = {T_C_C} °C  ({T_C:.0f} K)',
                 transform=ax1.transAxes, color='#FF6B6B', fontsize=9, va='top')

        ax2.set_facecolor('#0d0d1a')
        T_H_range = np.linspace(T_C + 10, T_C + 1500, 300)
        eta_range = 1 - T_C / T_H_range

        ax2.plot(T_H_range - 273.15, eta_range * 100,
                 color='#00BFFF', linewidth=2.5, label='Carnotova účinnosť')
        ax2.axvline(x=T_H_C, color='#FFD700', linewidth=2,
                    linestyle='--', alpha=0.9,
                    label=f'Aktuálne $T_H$ = {T_H_C} °C')
        ax2.plot(T_H_C, eta * 100, 'o', color='#FFD700',
                 markersize=10, zorder=5)
        ax2.annotate(f'η = {eta*100:.1f} %',
                     xy=(T_H_C, eta * 100),
                     xytext=(T_H_C + 50, eta * 100 - 5),
                     color='#FFD700', fontsize=11, fontweight='bold',
                     arrowprops=dict(arrowstyle='->', color='#FFD700', lw=1.5))
        ax2.fill_between(T_H_range - 273.15, eta_range * 100,
                         alpha=0.10, color='#00BFFF')
        ax2.set_xlabel('Teplota teplého zásobníka $T_H$ (°C)',
                       color='#cccccc', fontsize=11)
        ax2.set_ylabel('Účinnosť η (%)', color='#cccccc', fontsize=11)
        ax2.set_title('Závislosť účinnosti od teploty',
                      color='white', fontsize=12, pad=10)
        ax2.legend(fontsize=9, facecolor='#1a1a2e',
                   edgecolor='#555555', framealpha=0.9)
        ax2.grid(True, alpha=0.12)
        ax2.tick_params(colors='#aaaaaa')
        ax2.set_ylim(0, 100)

        fig.suptitle(
            f'Carnotov cyklus  │  $T_H$ = {T_H_C} °C  │  '
            f'$T_C$ = {T_C_C} °C  │  η = {eta*100:.1f} %',
            fontsize=12, color='white', y=1.01
        )
        plt.tight_layout()
        plt.show()

        print(f'{"═"*48}')
        print(f'  Teplota teplého zásobníka:    {T_H_C} °C  ({T_H:.1f} K)')
        print(f'  Teplota studeného zásobníka:  {T_C_C} °C  ({T_C:.1f} K)')
        print(f'{"─"*48}')
        print(f'  Carnotova účinnosť:           {eta*100:.2f} %')
        print(f'  Teplo prijaté Q_H:            {1 - T_C/T_H:.3f} (norm.)')
        print(f'  Teplo odovzdané Q_C:          {T_C/T_H:.3f} (norm.)')
        print(f'{"═"*48}')
        print(f'  Žiadny reálny motor nemôže dosiahnuť')
        print(f'  účinnosť vyššiu ako {eta*100:.1f} % pri týchto teplotách.')
        print(f'{"═"*48}')


widgets.interact(
    zobraz_cyklus,
    T_H_C=widgets.IntSlider(
        value=400, min=100, max=1500, step=10,
        description='T_H (°C):',
        style={'description_width': '120px'},
        layout=widgets.Layout(width='500px')),
    T_C_C=widgets.IntSlider(
        value=50, min=0, max=300, step=5,
        description='T_C (°C):',
        style={'description_width': '120px'},
        layout=widgets.Layout(width='500px'))
)

display(out)
```

## Porovnanie s reálnym spaľovacím motorom

Typický spaľovací motor pracuje pri teplotách:
- Teplota spaľovania: $T_H \approx 1800\text{–}2200$ °C
- Teplota výfuku: $T_C \approx 100\text{–}150$ °C

Nastav tieto hodnoty v slideri a pozri aká je teoretická maximálna 
účinnosť. Reálne motory dosahujú len $30\text{–}40$ % z tejto hodnoty 
kvôli treniu, tepelným stratám a nedokonalému spaľovaniu.

+++

## Záver

Tento notebook demonštroval Carnotov cyklus ako teoretický základ 
termodynamiky tepelných strojov.

- Tepelná účinnosť závisí výlučne od teplôt zásobníkov, nie od 
  pracovnej látky ani od konštrukcie stroja
- Vyšší teplotný rozdiel $T_H - T_C$ vedie k vyššej účinnosti
- Žiadny reálny motor nemôže prekročiť Carnotovu účinnosť
- Spaľovacie motory majú teoretickú maximálnu účinnosť okolo 
  60–70 %, reálne dosahujú 30–40 % kvôli nevratným dejom

```{code-cell} ipython3

```
