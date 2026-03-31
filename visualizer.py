"""Visualization utilities for Monte Carlo simulation output."""

from __future__ import annotations

import random

from matplotlib.figure import Figure
from matplotlib.patches import Circle, Rectangle
import matplotlib.pyplot as plt

MAX_PLOT_POINTS = 10_000
PLOT_SAMPLE_SIZE = 5_000


def build_scatter_figure(points: list[dict[str, float | bool]]) -> Figure:
    """
    Build a scatter plot of generated Monte Carlo points.

    Points are visually separated by whether they are inside or outside
    the unit circle. The unit circle boundary and sampling square boundary
    are both drawn for geometric clarity.

    Args:
        points: List of point records, each containing:
            - x (float)
            - y (float)
            - inside_circle (bool)

    Returns:
        A matplotlib Figure object with the scatter visualization.
    """
    if not points:
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.set_title("Monte Carlo Point Sampling")
        ax.text(0.5, 0.5, "No points to display.", ha="center", va="center", transform=ax.transAxes)
        ax.set_axis_off()
        plt.tight_layout()
        return fig

    plot_points = (
        random.sample(points, PLOT_SAMPLE_SIZE)
        if len(points) > MAX_PLOT_POINTS
        else points
    )

    inside_x: list[float] = []
    inside_y: list[float] = []
    outside_x: list[float] = []
    outside_y: list[float] = []

    for point in plot_points:
        x = float(point["x"])
        y = float(point["y"])
        is_inside = bool(point["inside_circle"])

        if is_inside:
            inside_x.append(x)
            inside_y.append(y)
        else:
            outside_x.append(x)
            outside_y.append(y)

    fig, ax = plt.subplots(figsize=(6, 6))

    if inside_x:
        ax.scatter(
            inside_x,
            inside_y,
            s=4,
            c="#2ca02c",
            alpha=0.5,
            label="Inside Unit Circle",
            edgecolors="none",
        )
    if outside_x:
        ax.scatter(
            outside_x,
            outside_y,
            s=4,
            c="#d62728",
            alpha=0.5,
            label="Outside Unit Circle",
            edgecolors="none",
        )

    circle = Circle(
        (0, 0),
        1.0,
        fill=False,
        linewidth=1.0,
        linestyle="-",
        color="#1f77b4",
        label="Unit Circle Boundary",
    )
    square = Rectangle(
        (-1, -1),
        2,
        2,
        fill=False,
        linewidth=1.0,
        linestyle="--",
        color="#111111",
        label="Sampling Square",
    )
    ax.add_patch(circle)
    ax.add_patch(square)

    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x-coordinate")
    ax.set_ylabel("y-coordinate")
    ax.set_title("Monte Carlo Sampling in the Unit Square")
    ax.grid(True, linestyle=":", linewidth=0.8, alpha=0.35)
    ax.legend(loc="upper right", frameon=True, fontsize=9)

    plt.tight_layout()
    return fig


def build_convergence_figure(convergence_history: list[float]) -> Figure:
    """
    Build a convergence plot for running pi estimates.

    Args:
        convergence_history: Running pi estimate values after each sample.

    Returns:
        A matplotlib Figure object showing estimate convergence over time.
    """
    if not convergence_history:
        fig, ax = plt.subplots(figsize=(7, 3))
        ax.set_title("Pi Estimate Convergence")
        ax.text(0.5, 0.5, "No convergence data to display.", ha="center", va="center", transform=ax.transAxes)
        ax.set_axis_off()
        plt.tight_layout()
        return fig

    sample_steps = list(range(1, len(convergence_history) + 1))

    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(
        sample_steps,
        convergence_history,
        color="#1f77b4",
        linewidth=1.4,
        alpha=0.85,
        label="Running Pi Estimate",
    )
    ax.axhline(
        y=3.141592653589793,
        color="#ff7f0e",
        linestyle="--",
        linewidth=1.2,
        label="Reference: True Pi",
    )

    ax.set_xlabel("Number of Random Samples")
    ax.set_ylabel("Estimated Pi")
    ax.set_title("Convergence of Monte Carlo Pi Estimate")
    ax.grid(True, linestyle=":", linewidth=0.8, alpha=0.35)
    ax.legend(loc="best", frameon=True, fontsize=9)
    ax.margins(x=0.01)

    plt.tight_layout()
    return fig


def build_multi_run_histogram_figure(estimated_pi_values: list[float]) -> Figure:
    """
    Build a histogram of pi estimates from repeated experiments.

    Args:
        estimated_pi_values: Pi estimates collected from multiple runs.

    Returns:
        A matplotlib Figure object for Streamlit rendering.
    """
    if not estimated_pi_values:
        fig, ax = plt.subplots(figsize=(8.2, 4.8))
        ax.set_title("Distribution of Pi Estimates Across Runs")
        ax.text(0.5, 0.5, "No multi-run data to display.", ha="center", va="center", transform=ax.transAxes)
        ax.set_axis_off()
        fig.tight_layout()
        return fig

    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    bin_count = min(20, max(6, len(estimated_pi_values) // 2))
    ax.hist(
        estimated_pi_values,
        bins=bin_count,
        color="#4c78a8",
        alpha=0.8,
        edgecolor="#1f1f1f",
        linewidth=0.6,
    )
    ax.axvline(
        x=3.141592653589793,
        color="#ff7f0e",
        linestyle="--",
        linewidth=1.8,
        label="Reference: True Pi",
    )

    ax.set_title("Distribution of Pi Estimates Across Runs")
    ax.set_xlabel("Estimated Pi")
    ax.set_ylabel("Frequency")
    ax.grid(True, axis="y", linestyle=":", linewidth=0.8, alpha=0.35)
    ax.legend(loc="best", frameon=True, fontsize=9)
    fig.tight_layout(pad=1.0)
    return fig
