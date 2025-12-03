# Analytics service for FOMS

A Flask API service that serves predictions from pre-trained scikit-learn models.

## Requirements

- Python 3.8+
- pip

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Circuitea/foms-analytics.git
   cd foms-analytics
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Or using `pyproject.toml`:
   ```bash
   pip install .
   ```

## Development

1. Install development dependencies:
   ```bash
   pip install -e .
   ```

2. Run the Flask development server:
   ```bash
   flask run
   ```
   Or:
   ```bash
   python run.py
   ```

3. Run tests:
   ```bash
   pytest
   ```

## Project Structure

```
foms-analytics/
├── app/
│   ├── __init__.py
│   ├── api.py
│   ├── model.py
│   └── utils.py
├── models/
│   └── *.pkl
├── tests/
├── requirements.txt
├── pyproject.toml
├── run.py
└── README.md
```

## API Usage

Send a POST request to the prediction endpoint with the required input data.

## License

MIT