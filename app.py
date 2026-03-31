"""Streamlit app entry point for Monte Carlo Pi Estimator."""

from __future__ import annotations

import math

import streamlit as st

from simulation import estimate_pi, run_multiple_experiments
from visualizer import (
    build_convergence_figure,
    build_multi_run_histogram_figure,
    build_scatter_figure,
)

DEFAULT_POINTS = 10_000
MIN_UI_POINTS = 100
MAX_UI_POINTS = 200_000
MIN_UI_RUNS = 5
MAX_UI_RUNS = 50
COMPARISON_SIZES = (100, 1_000, 5_000, 10_000)


def _render_header() -> None:
    """Render page title and short description."""
    st.title("Monte Carlo Pi Estimator")
    st.write(
        "Estimate pi by randomly sampling points in a square and checking how many "
        "fall inside the unit circle. This demo highlights simulation-based "
        "approximation and convergence behavior."
    )


def _render_sidebar_controls() -> tuple[int, int, bool]:
    """Render sidebar controls and return user selections."""
    st.sidebar.header("Simulation Controls")
    num_points = st.sidebar.slider(
        label="Number of points",
        min_value=MIN_UI_POINTS,
        max_value=MAX_UI_POINTS,
        value=DEFAULT_POINTS,
        step=100,
        help="Higher values usually improve accuracy but take more time.",
    )
    num_runs = st.sidebar.slider(
        label="Number of repeated runs",
        min_value=MIN_UI_RUNS,
        max_value=MAX_UI_RUNS,
        value=20,
        step=1,
        help="Used in Multi-Run Analysis to show variability across repeated experiments.",
    )
    run_clicked = st.sidebar.button("Run Simulation", type="primary")
    return num_points, num_runs, run_clicked


def _render_explanation() -> None:
    """Render conceptual explanation for the demo."""
    st.markdown("### Why Monte Carlo Works")
    st.write(
        "In this setup, points are sampled uniformly in the square `[-1, 1] x [-1, 1]`, "
        "which has area `4`. The unit circle has area `pi`, so the fraction of sampled "
        "points inside the circle approximates `pi/4`. Multiplying that fraction by `4` "
        "gives an estimate of pi."
    )
    st.write(
        "By the Law of Large Numbers, as the number of random samples increases, "
        "the empirical ratio tends to the true probability, so the pi estimate "
        "typically becomes more stable and accurate."
    )


def _build_experiment_comparison_rows(sample_sizes: tuple[int, ...]) -> list[dict[str, str]]:
    """Run multiple sample sizes and return table-ready comparison rows."""
    rows: list[dict[str, str]] = []
    for sample_size in sample_sizes:
        estimated_pi, _, _, _, _ = estimate_pi(sample_size)
        absolute_error = abs(math.pi - estimated_pi)
        rows.append(
            {
                "Number of Points": f"{sample_size:,}",
                "Estimated Pi": f"{estimated_pi:.6f}",
                "Absolute Error": f"{absolute_error:.6f}",
            }
        )
    return rows


def _render_analysis_summary(estimated_pi: float, absolute_error: float, num_points: int) -> None:
    """Render a concise, automatically generated interpretation."""
    closeness_statement = (
        "reasonably close to the true value"
        if absolute_error <= 0.02
        else "a useful but still coarse approximation of the true value"
    )
    st.markdown("### Analysis Summary")
    st.write(
        f"With **{num_points:,}** random points, the estimator produced "
        f"**pi ≈ {estimated_pi:.6f}** with an absolute error of **{absolute_error:.6f}**. "
        f"This estimate appears **{closeness_statement}**. In Monte Carlo methods, "
        "increasing the number of random samples generally reduces fluctuation and "
        "improves estimate stability."
    )


def _render_multi_run_analysis(num_points: int, num_runs: int) -> bool:
    """Render repeated-run metrics, compact preview, and expandable details."""
    try:
        multi_run_result = run_multiple_experiments(num_points=num_points, num_runs=num_runs)
    except (TypeError, ValueError) as exc:
        st.error(f"Multi-run analysis could not run: {exc}")
        return False

    runs = multi_run_result["runs"]
    summary = multi_run_result["summary"]
    estimate_values = [row["estimated_pi"] for row in runs]

    st.markdown("## Multi-Run Analysis")
    st.write(
        "This section repeats the simulation several times using the same number of points "
        "to show how random sampling affects the result."
    )

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Mean Estimated Pi", f"{summary['mean_estimated_pi']:.6f}")
    col2.metric("Std. Deviation", f"{summary['std_dev_estimated_pi']:.6f}")
    col3.metric("Mean Absolute Error", f"{summary['mean_absolute_error']:.6f}")
    col4.metric("Minimum Estimate", f"{summary['min_estimated_pi']:.6f}")
    col5.metric("Maximum Estimate", f"{summary['max_estimated_pi']:.6f}")

    st.markdown("### Distribution of Repeated Runs")
    histogram_fig = build_multi_run_histogram_figure(estimate_values)
    st.pyplot(histogram_fig, use_container_width=True)

    st.markdown("### Run-by-Run Summary")
    table_rows = [
        {
            "Run Number": row["run_number"],
            "Estimated Pi": f"{row['estimated_pi']:.6f}",
            "Absolute Error": f"{row['absolute_error']:.6f}",
        }
        for row in runs
    ]
    best_run = min(runs, key=lambda row: row["absolute_error"])
    worst_run = max(runs, key=lambda row: row["absolute_error"])
    st.write(
        f"Best run: **#{best_run['run_number']}** (pi = {best_run['estimated_pi']:.6f}, "
        f"error = {best_run['absolute_error']:.6f}) | "
        f"Worst run: **#{worst_run['run_number']}** (pi = {worst_run['estimated_pi']:.6f}, "
        f"error = {worst_run['absolute_error']:.6f})"
    )
    st.caption("Preview of first 5 runs:")
    st.dataframe(table_rows[:5], use_container_width=True, hide_index=True)
    with st.expander("Show Detailed Run-by-Run Results"):
        st.dataframe(table_rows, use_container_width=True, hide_index=True)
    st.caption(
        "Repeated runs highlight the stochastic nature of Monte Carlo methods: even with "
        "the same number of points, different random samples can produce slightly different "
        "estimates. As sampling becomes more reliable, the distribution tends to concentrate "
        "closer to the true value of pi."
    )
    return True


def _run_and_render_results(num_points: int, num_runs: int) -> bool:
    """Execute simulation and render results with compact default layout."""
    try:
        estimated_pi, inside_count, outside_count, points, convergence_history = estimate_pi(num_points)
    except (TypeError, ValueError) as exc:
        st.error(f"Simulation could not run: {exc}")
        return False

    absolute_error = abs(math.pi - estimated_pi)
    inside_ratio = inside_count / num_points
    outside_ratio = outside_count / num_points

    st.markdown("## Simulation Results")
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    col1.metric("Estimated Pi", f"{estimated_pi:.6f}")
    col2.metric("Actual Pi", f"{math.pi:.6f}")
    col3.metric("Absolute Error", f"{absolute_error:.6f}")
    col4.metric("Inside Circle", f"{inside_count:,} ({inside_ratio:.2%})")
    col5.metric("Outside Circle", f"{outside_count:,} ({outside_ratio:.2%})")
    col6.metric("Total Points", f"{num_points:,}")

    st.caption(
        "Rule used: pi ≈ 4 × (inside points / total points). "
        "Larger samples generally reduce random fluctuation."
    )

    st.markdown("### Experiment Comparison")
    st.write("Comparison details are hidden by default to keep the demo focused.")
    comparison_rows = _build_experiment_comparison_rows(COMPARISON_SIZES)
    with st.expander("Show Experiment Comparison Details"):
        st.dataframe(comparison_rows, use_container_width=True, hide_index=True)
    st.caption(
        "Across repeated runs, larger sample sizes generally produce more stable and "
        "accurate estimates of pi."
    )

    st.markdown("### Visual Analysis")
    scatter_fig = build_scatter_figure(points)
    convergence_fig = build_convergence_figure(convergence_history)
    st.pyplot(scatter_fig, use_container_width=True)
    st.pyplot(convergence_fig, use_container_width=True)
    _render_analysis_summary(estimated_pi, absolute_error, num_points)
    st.markdown("---")
    return _render_multi_run_analysis(num_points=num_points, num_runs=num_runs)


def main() -> None:
    """Run the Streamlit application."""
    st.set_page_config(page_title="Monte Carlo Pi Estimator", layout="wide")

    _render_header()
    num_points, num_runs, run_clicked = _render_sidebar_controls()

    if run_clicked:
        with st.spinner("Running simulation..."):
            success = _run_and_render_results(num_points, num_runs)
        if success:
            st.success("Simulation completed.")
    else:
        st.info("Choose the number of points in the sidebar, then click **Run Simulation**.")

    st.markdown("---")
    _render_explanation()


if __name__ == "__main__":
    main()
