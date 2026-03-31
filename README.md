# Monte Carlo Pi Estimator

Monte Carlo Pi Estimator is a Streamlit-based mini analysis tool that estimates the value of pi using random sampling. The project is designed for an applied AI university assignment and includes both single-run simulation and repeated-run variability analysis in a clean, demo-friendly interface.

## Project Overview

This project applies the Monte Carlo method to estimate pi by sampling random points in a square and measuring how many fall inside the unit circle. It is intentionally simple, modular, and suitable for short presentations and academic reports.

## How It Works

The app generates random points inside the square `[-1, 1] x [-1, 1]` and checks whether each point falls inside the unit circle. Since the circle area to square area ratio is `pi/4`, the estimate is computed as:

`pi ≈ 4 x (inside points / total points)`

As the number of samples increases, the estimate usually becomes more stable due to the Law of Large Numbers.

## Features

- Single-run Monte Carlo simulation for pi estimation
- Scatter visualization of sampled points (inside vs outside unit circle)
- Convergence plot of running pi estimate
- Experiment comparison across multiple sample sizes
- Multi-run analysis with histogram and summary statistics
- Compact, presentation-friendly layout with expandable details

## Project Structure

```text
ai-monte-carlo-pi/
├── app.py
├── simulation.py
├── visualizer.py
├── requirements.txt
├── README.md
├── assets/
└── report/
```

## Installation

```bash
pip install -r requirements.txt
```

## Run the App

```bash
streamlit run app.py
```

## Typical Outputs

- Estimated pi, actual pi, and absolute error
- Inside/outside point counts
- Scatter plot and convergence chart
- Multi-run summary metrics (mean, std, min, max, mean absolute error)
- Repeated-run result table and estimate distribution histogram

## Author

Mert Savaşer - 210911040
