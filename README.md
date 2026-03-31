# Monte Carlo Pi Estimator

Monte Carlo Pi Estimator is a beginner-friendly Streamlit project for estimating the value of pi using random sampling. It is designed for an applied AI university assignment and demonstrates both single-run estimation and repeated-run statistical analysis in a clean, presentation-ready format.

## How It Works

The app generates random points inside the square `[-1, 1] x [-1, 1]` and checks whether each point falls inside the unit circle. Since the circle area to square area ratio is `pi/4`, the estimate is computed as:

`pi ≈ 4 x (inside points / total points)`

As the number of random samples increases, the estimate generally becomes more stable due to the Law of Large Numbers.

## Features

- Monte Carlo simulation for pi estimation
- Visualization with scatter plot and convergence chart
- Experiment comparison across multiple sample sizes
- Multi-run analysis with distribution and summary statistics

## Installation and Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Author

Mert Savaşer - 210911040
