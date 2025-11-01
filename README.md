# Multi-Agent Simulation of Sterile Insect Technique in a Multi-Patch System

## Description

This repository contains a comprehensive framework for simulating and optimizing Sterile Insect Technique (SIT) applications in multi-patch mosquito population systems. The project includes:

- **Multi-agent simulation** of SIT for mosquitoes in a multi-patch environment
- **Surrogate modeling** using neural networks to create efficient approximations of the simulation
- **Optimization algorithms** for release strategy optimization through gradient descent
- **Data processing pipelines** for preparing simulation data for machine learning

This research project was conducted during my second year at *École des Mines de Nancy* in the applied mathematics department. For detailed theoretical explanations and methodology, please refer to `docs/report.pdf`.

## Project Structure

```
├── src/sit_simulation/          # Core simulation package
│   ├── core/                   # Core simulation components
│   │   ├── config.py           # Configuration management
│   │   ├── simulation.py       # Main simulation engine
│   │   ├── spatial_manager.py  # Spatial patch management
│   │   └── constants.py        # Simulation constants
│   └── observers/              # Data collection and logging
├── scripts/                    # Utility scripts
│   ├── multiple_simulation.py  # Batch simulation runner
│   └── data_processing.py      # Data preprocessing for ML
├── config/                     # Configuration files
│   ├── simulation_config.yaml  # Simulation parameters
│   ├── insect_config.yaml      # Insect behavior parameters
│   ├── initial_insects.csv     # Initial population data
│   └── release_strategy.csv    # Release strategy templates
├── notebooks/                  # Jupyter notebooks
│   └── final.ipynb         # Surrogate model & optimization
└── docs/                       # Documentation
    └── report.pdf              # Detailed research report
```

## Installation

```bash
# Install the package in development mode
pip install -e .
```

## Usage

### 1. Single Simulation Run

Execute a single SIT simulation with specified configuration:

```bash
python src/sit_simulation/__main__.py \
    --simu_config config/simulation_config.yaml \
    --insect_config config/insect_config.yaml \
    --initial_insects config/initial_insects.csv \
    --release_strategy config/release_strategy.csv \
    --output output/single_simulation
```

### 2. Multiple Simulations (Data Generation)

Generate multiple simulations for training surrogate models:

```bash
python scripts/multiple_simulation.py \
    --base_config config \
    --output multiple_simulations_output \
    --number_of_simulations 1000
```

### 3. Data Processing

Process simulation data for machine learning:

```bash
python scripts/data_processing.py \
    --simu_config config/simulation_config.yaml \
    --input multiple_simulations_output \
    --output processed_data \
    --past_len 20 \
    --future_len 100
```

### 4. Surrogate Modeling and Optimization

Use the Jupyter notebook for advanced analysis:

```bash
jupyter notebook notebooks/final.ipynb
```
