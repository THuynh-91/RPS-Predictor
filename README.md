# RPS-Predictor

An adaptive Rock-Paper-Scissors AI that learns to predict and beat opponents using three different strategies.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Models](#models)
- [Environment Setup](#environment-setup)
- [How to Run](#how-to-run)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project implements three AI models that try to predict your next move in Rock-Paper-Scissors. The repository includes:

- Three distinct prediction strategies (Random, Markov Chain, Q-Learning)
- Interactive command-line game interface
- Batch simulation framework for performance evaluation
- Jupyter notebook for statistical analysis
- Manim animations for visualizing game progression and learning curves

## Prerequisites

Before setting up the project, ensure you have:

- **Python 3.8 or higher** installed
- **pip** (Python package installer)
- **(Optional)** LaTeX distribution (e.g., MiKTeX on Windows, MacTeX on macOS) for rendering Manim animations

## Models

1. **Random Predictor**
   - Makes random predictions
   - No learning capability
   - Baseline model (~33% win rate)

2. **Markov Chain Predictor**
   - Detects patterns in your move sequences
   - Builds a transition probability table based on move history
   - Predicts your next move based on recent patterns

3. **Q-Learning Predictor**
   - Uses reinforcement learning to learn optimal counter-strategies
   - Learns from wins, losses, and ties over time
   - Requires training phase before playing (default: 10,000 episodes)

## Environment Setup

### 1. Create a Virtual Environment

**Windows:**
```bash
cd RPS-Predictor
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
cd RPS-Predictor
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## How to Run

### Play the Interactive Game

```bash
cd src
python game.py
```

**Steps:**
1. Select a model (1-3)
2. If you selected Q-Learning, choose training episodes (press Enter for default 10,000)
3. Play using commands:
   - `R` - Rock
   - `P` - Paper
   - `S` - Scissors
   - `STATS` - View current statistics
   - `Q` - Quit

### Run Simulations

To generate simulation data:

```bash
cd src
python generate_csvs.py
```

This creates CSV files in the `results/` directory with 100,000 rounds per model/opponent combination.

### View Analysis

Open the Jupyter notebook for visualizations and statistical analysis:

```bash
jupyter notebook RPS_Simulation_Analysis.ipynb
```

### Generate Manim Animations

The project includes Manim scripts to create visualizations of game progression and statistics.

To render an animation:

```bash
cd src/animations/markov
manim -pql counter_playback.py RPSPlayback
```

**Parameters:**
- `-p` - Preview the video after rendering
- `-q` - Quality (l=low, m=medium, h=high)
- `-l` - Low quality (fastest)

**Available animations:**

Each predictor type has animations for different opponents:

**Markov animations:**
```bash
cd src/animations/markov
manim -pql counter_playback.py RPSPlayback
manim -pql repeater_playback.py RPSPlayback
manim -pql random_playback.py RPSPlayback
manim -pql fizzbuzz_playback.py RPSPlayback
```

**Q-Learning animations:**
```bash
cd src/animations/qlearning
manim -pql [playback_file].py RPSPlayback
```

**Random animations:**
```bash
cd src/animations/random
manim -pql [playback_file].py RPSPlayback
```

The animations visualize:
- Round-by-round gameplay
- Move distributions
- Win/loss/tie statistics
- Cumulative performance trends

## Contributing

Feel free to fork this repository and modify it for your own purposes. This project is provided as-is for educational use.

## License

MIT License 

