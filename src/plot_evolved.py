"""
Block diagram for the evolved controller (best result from 100-iteration run).
Highlights: adaptive Kp, integral anti-windup clamp, integral perturbation.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def _box(ax, x, y, w, h, label, sublabel=None, color='#4C72B0'):
    rect = mpatches.FancyBboxPatch((x, y), w, h,
                                    boxstyle="round,pad=0.08",
                                    linewidth=1.5, edgecolor='black',
                                    facecolor=color, alpha=0.85, zorder=3)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2 + (0.12 if sublabel else 0), label,
            ha='center', va='center', fontsize=10, fontweight='bold',
            color='white', zorder=4)
    if sublabel:
        ax.text(x + w/2, y + h/2 - 0.22, sublabel,
                ha='center', va='center', fontsize=8,
                color='#dde', zorder=4)


def _arrow(ax, x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='black',
                                lw=1.8, connectionstyle='arc3,rad=0'),
                zorder=2)


def _circle(ax, x, y, r=0.28, label='+'):
    c = plt.Circle((x, y), r, color='white', ec='black', lw=1.8, zorder=3)
    ax.add_patch(c)
    ax.text(x, y, label, ha='center', va='center', fontsize=13, zorder=4)


def plot(save_path='evolved_diagram.png'):
    """Draw and save the evolved controller block diagram."""
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 6)
    ax.axis('off')

    # Setpoint
    ax.text(0.35, 3.0, 'Setpoint\nr(t)', ha='center', va='center', fontsize=10)

    # Summing junction
    _circle(ax, 1.5, 3.0)
    ax.text(1.28, 3.22, '+', fontsize=10, color='black')
    ax.text(1.28, 2.75, '−', fontsize=12, color='black')

    # Evolved controller box — wider to show internals
    _box(ax, 2.6, 1.2, 3.8, 3.6, 'Evolved Controller', color='#6A3D9A')

    # Internal labels inside controller box
    ax.text(4.5, 4.4, 'Kp(t)·e  [adaptive]',  ha='center', va='center', fontsize=8, color='#f0e0ff')
    ax.text(4.5, 3.8, 'Ki·∫e dt  [+ 0.0013·e perturbation]', ha='center', va='center', fontsize=8, color='#f0e0ff')
    ax.text(4.5, 3.2, 'integral clamp ±96',    ha='center', va='center', fontsize=8, color='#f0e0ff', style='italic')
    ax.text(4.5, 2.6, 'Kd·de/dt',              ha='center', va='center', fontsize=8, color='#f0e0ff')
    ax.text(4.5, 2.0, 'Kp adapts: if |ḋ|>0.12,\nKp += 0.015·ḋ', ha='center', va='center', fontsize=7.5, color='#ffddaa')
    for yline in [2.3, 3.5]:
        ax.plot([2.65, 6.35], [yline, yline], color='#998', lw=0.7, zorder=3, linestyle='--')

    # Summing junction inside controller (Σ of P+I+D)
    _circle(ax, 7.0, 3.0, r=0.25, label='Σ')

    # Saturation block
    _box(ax, 7.8, 2.4, 1.4, 1.2, 'Sat', sublabel='[−10, 10]', color='#B8860B')

    # Plant
    _box(ax, 10.0, 2.4, 2.0, 1.2, 'Plant', sublabel='ẏ = −ay + bu', color='#2A7D4F')

    # Output
    ax.text(13.5, 3.0, 'Output\ny(t)', ha='center', va='center', fontsize=10)

    # Sensor / feedback
    _box(ax, 4.5, 0.3, 2.0, 0.8, 'Sensor', color='#8B4513')

    # Arrows — forward path
    _arrow(ax, 0.7,  3.0, 1.22, 3.0)   # setpoint → sum junction
    _arrow(ax, 1.78, 3.0, 2.6,  3.0)   # sum junction → controller
    _arrow(ax, 6.4,  3.0, 6.75, 3.0)   # controller → Σ
    _arrow(ax, 7.25, 3.0, 7.8,  3.0)   # Σ → saturation
    _arrow(ax, 9.2,  3.0, 10.0, 3.0)   # sat → plant
    _arrow(ax, 12.0, 3.0, 13.2, 3.0)   # plant → output

    # Feedback path
    ax.plot([12.5, 12.5], [3.0, 1.1], color='black', lw=1.8, zorder=2)
    ax.plot([12.5, 6.5],  [1.1, 1.1], color='black', lw=1.8, zorder=2)
    _arrow(ax, 6.5, 1.1, 4.5, 1.1)
    _arrow(ax, 4.5, 1.1, 1.5, 1.1)
    ax.plot([1.5, 1.5], [1.1, 2.72], color='black', lw=1.8, zorder=2)

    # Labels
    ax.text(2.1,  3.18, 'e(t)', fontsize=9, color='#333')
    ax.text(7.35, 3.18, 'u\'(t)', fontsize=9, color='#333')
    ax.text(9.3,  3.18, 'u(t)', fontsize=9, color='#333')
    ax.text(12.6, 2.1,  'y(t)', fontsize=9, color='#333')

    ax.set_title('Evolved Controller — 100-Iteration OpenEvolve Run  (score 0.9421 → 0.9666)',
                 fontsize=13, fontweight='bold', pad=12)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"Saved {save_path}")
    return fig


if __name__ == "__main__":
    plot()
