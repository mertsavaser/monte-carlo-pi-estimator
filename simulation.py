"""Monte Carlo simulation helpers for estimating pi."""

from __future__ import annotations

import random
import statistics
from typing import TypedDict

MIN_POINTS = 1
MAX_POINTS = 1_000_000
MIN_RUNS = 1
MAX_RUNS = 1_000


class PointRecord(TypedDict):
    """Structured point data for plotting and analysis."""

    x: float
    y: float
    inside_circle: bool


class ExperimentRunResult(TypedDict):
    """Result for one Monte Carlo run."""

    run_number: int
    estimated_pi: float
    absolute_error: float


class MultiRunSummary(TypedDict):
    """Summary statistics across repeated Monte Carlo runs."""

    mean_estimated_pi: float
    min_estimated_pi: float
    max_estimated_pi: float
    std_dev_estimated_pi: float
    mean_absolute_error: float


class MultiRunResult(TypedDict):
    """Container for repeated Monte Carlo experiment output."""

    runs: list[ExperimentRunResult]
    summary: MultiRunSummary


def _generate_point() -> tuple[float, float]:
    """Generate a random point in the square [-1, 1] x [-1, 1]."""
    return random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)


def _is_inside_unit_circle(x: float, y: float) -> bool:
    """Return True when the point lies inside/on the unit circle."""
    return (x * x) + (y * y) <= 1.0


def estimate_pi(
    num_points: int,
) -> tuple[float, int, int, list[PointRecord], list[float]]:
    """
    Estimate pi using a Monte Carlo simulation.

    The algorithm samples random points uniformly from the square
    with corners (-1, -1) and (1, 1). The ratio of points that land
    inside the unit circle approximates pi/4.

    Args:
        num_points: Number of random points to sample.
            Must be in [1, 1_000_000].

    Returns:
        A tuple containing:
        1) estimated_pi: Final pi estimate.
        2) inside_count: Number of points inside/on the unit circle.
        3) outside_count: Number of points outside the unit circle.
        4) points: Structured point records for plotting.
        5) convergence_history: Running pi estimate after each new point.

    Raises:
        TypeError: If num_points is not an integer.
        ValueError: If num_points is outside the supported range.
    """
    if not isinstance(num_points, int):
        raise TypeError("num_points must be an integer.")
    if not (MIN_POINTS <= num_points <= MAX_POINTS):
        raise ValueError(f"num_points must be between {MIN_POINTS} and {MAX_POINTS}.")

    inside_count = 0
    points: list[PointRecord] = []
    convergence_history: list[float] = []

    for idx in range(1, num_points + 1):
        x, y = _generate_point()
        inside = _is_inside_unit_circle(x, y)

        if inside:
            inside_count += 1

        points.append({"x": x, "y": y, "inside_circle": inside})
        convergence_history.append(4.0 * (inside_count / idx))

    outside_count = num_points - inside_count
    estimated_pi = convergence_history[-1]

    return estimated_pi, inside_count, outside_count, points, convergence_history


def run_multiple_experiments(num_points: int, num_runs: int) -> MultiRunResult:
    """
    Run repeated Monte Carlo pi estimation experiments.

    Args:
        num_points: Number of points used in each run.
        num_runs: Number of repeated runs to execute.

    Returns:
        Structured output containing per-run results and summary statistics.

    Raises:
        TypeError: If num_runs is not an integer.
        ValueError: If num_runs is outside the supported range.
    """
    if not isinstance(num_runs, int):
        raise TypeError("num_runs must be an integer.")
    if not (MIN_RUNS <= num_runs <= MAX_RUNS):
        raise ValueError(f"num_runs must be between {MIN_RUNS} and {MAX_RUNS}.")

    run_rows: list[ExperimentRunResult] = []
    estimates: list[float] = []
    absolute_errors: list[float] = []

    for run_index in range(1, num_runs + 1):
        estimated_pi, _, _, _, _ = estimate_pi(num_points)
        absolute_error = abs(estimated_pi - 3.141592653589793)
        run_rows.append(
            {
                "run_number": run_index,
                "estimated_pi": estimated_pi,
                "absolute_error": absolute_error,
            }
        )
        estimates.append(estimated_pi)
        absolute_errors.append(absolute_error)

    summary: MultiRunSummary = {
        "mean_estimated_pi": statistics.mean(estimates),
        "min_estimated_pi": min(estimates),
        "max_estimated_pi": max(estimates),
        "std_dev_estimated_pi": statistics.pstdev(estimates),
        "mean_absolute_error": statistics.mean(absolute_errors),
    }
    return {"runs": run_rows, "summary": summary}
