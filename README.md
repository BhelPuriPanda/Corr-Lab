# CorrLab Parser

A lightweight Python utility for parsing CorrTest ASCII (.cor) electrochemical corrosion files into structured datasets.

## Features

- Parses raw `.cor` files
- Extracts experiment metadata
- Converts data into a Pandas DataFrame
- Exports processed data to CSV
- Plots Current Density vs Time
- Calculates integrated current using the trapezoidal rule

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python parser.py sample.cor
```

## Output

```
output.csv
current_vs_time.png
```

## Tech Stack

- Python
- Pandas
- NumPy
- Matplotlib
