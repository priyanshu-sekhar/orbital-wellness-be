# FastAPI Application

This is a FastAPI application exposing Orbital Wellness API endpoints. It currently exposes the following endpoints:
- `GET /usage`: Returns the usage data for the current billing period

## Project Structure

The project is structured as follows:

- `src/main.py`: This is the main entry point of the application. It defines the FastAPI application and the API endpoints.
- `src/helpers.py`: This file contains helper functions used throughout the application.
- `src/models.py`: This file contains the data models used in the application.
- `.venv/lib/python3.10/site-packages/httpx/_transports/default.py`: This file is part of the httpx library, which is used for making HTTP requests.
- `tests`: This directory contains the test cases for the application.

## Setup Instructions

### Python Requirements
- Python 3.10 or higher

### Pip and Poetry
- Ensure you have `pip` installed. If not, you can install it by following the instructions [here](https://pip.pypa.io/en/stable/installation/).
- Install `poetry` for Python package management by running `pip install poetry`.

### Running the Project
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required Python packages by running `poetry install`.
4. Run the web crawler by executing `python src/main.py`.

## Testing
You can test the application's endpoints using the requests defined in `test_main.py`. 
