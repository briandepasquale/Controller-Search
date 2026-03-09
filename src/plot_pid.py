"""
PID feedback control loop block diagram.
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
            ha='center', va='center', fontsize=11, fontweight='bold',
            color='white', zorder=4)
    if sublabel:
        ax.text(x + w/2, y + h/2 - 0.22, sublabel,
                ha='center', va='center', fontsize=8.5,
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


def plot(save_path='pid_diagram.png'):
    """Draw and save the PID feedback control loop block diagram."""
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)
    ax.axis('off')

    ax.text(0.3, 2.5, 'Setpoint\nr(t)', ha='center', va='center', fontsize=10)

    _circle(ax, 1.5, 2.5)
    ax.text(1.28, 2.72, '+', fontsize=10, color='black')
    ax.text(1.28, 2.25, '−', fontsize=12, color='black')

    _box(ax, 2.6, 1.6, 2.0, 1.8, 'PID Controller', color='#2D6A9F')
    ax.text(3.6, 3.1,  'Kp · e',     ha='center', va='center', fontsize=8.5, color='#222')
    ax.text(3.6, 2.5,  'Ki · ∫e dt', ha='center', va='center', fontsize=8.5, color='#222')
    ax.text(3.6, 1.9,  'Kd · de/dt', ha='center', va='center', fontsize=8.5, color='#222')
    for yline in [2.2, 2.8]:
        ax.plot([2.65, 4.55], [yline, yline], color='#aac', lw=0.8, zorder=3)
    _circle(ax, 5.0, 2.5, r=0.25, label='Σ')

    _box(ax, 6.0, 1.9, 2.0, 1.2, 'Plant', sublabel='ẏ = −ay + bu', color='#2A7D4F')

    ax.text(11.5, 2.5, 'Output\ny(t)', ha='center', va='center', fontsize=10)

    _box(ax, 4.5, 0.4, 2.0, 0.8, 'Sensor', color='#8B4513')

    _arrow(ax, 0.6,  2.5, 1.22, 2.5)
    _arrow(ax, 1.78, 2.5, 2.6,  2.5)
    _arrow(ax, 4.6,  2.5, 4.75, 2.5)
    _arrow(ax, 5.25, 2.5, 6.0,  2.5)
    _arrow(ax, 8.0,  2.5, 11.2, 2.5)

    ax.plot([9.0, 9.0], [2.5, 0.8], color='black', lw=1.8, zorder=2)
    ax.plot([9.0, 6.5], [0.8, 0.8], color='black', lw=1.8, zorder=2)
    _arrow(ax, 6.5, 0.8, 4.5, 0.8)
    _arrow(ax, 4.5, 0.8, 1.5, 0.8)
    ax.plot([1.5, 1.5], [0.8, 2.22], color='black', lw=1.8, zorder=2)

    ax.text(2.1,  2.65, 'e(t)', fontsize=9, color='#333')
    ax.text(5.35, 2.65, 'u(t)', fontsize=9, color='#333')
    ax.text(9.2,  1.65, 'y(t)', fontsize=9, color='#333')

    ax.set_title('PID Feedback Control Loop', fontsize=14, fontweight='bold', pad=10)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"Saved {save_path}")
    return fig


if __name__ == "__main__":
    plot()
