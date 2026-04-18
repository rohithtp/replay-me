# Replayer

Replayer is a CLI tool designed to replay career events and generate a resume. This project follows modern Python standards and uses event sourcing patterns.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/yourusername/replayer.git
   cd replayer
   ```

2. **Set Up a Virtual Environment** (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt; pip install build; 
   ```

4. **Build the Package** (if needed):
   ```sh
   python -m build
   ```

5. **Install the Package**:
   ```sh
   pip install .
   pip install -e .
   ```

## Usage

1. **Run the CLI Tool**:
   ```sh
   replay --help
   ```

2. **Example Command**:
   ```sh
   replay events.yaml
   ```

3. **Sample Event**:
   ```yaml
   - event: work
     start_date: 2023-01-01
     end_date: 2023-12-31
     company: Sample Company
     title: Software Engineer
   ```

## Testing

1. **Run Tests**:
   ```sh
   python -m unittest discover tests
   ```

2. **Sample Test**:
   The `tests/test_sample_flow.py` file contains a sample test that verifies the flow and reports correctness.

3. **Example Test Output**:
   ```sh
   ...
   ----------------------------------------------------------------------
   Ran 1 test in 0.001s

   OK
   ```

## Contributing

We welcome contributions! Please read our [Contributing Guide](CONTRIBUTING.md) to learn how you can help.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
