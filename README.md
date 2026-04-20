# Replayer

Replayer is a CLI tool designed to replay career events and generate a resume. This project follows modern Python standards and uses event sourcing patterns.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Installation

### With uv (recommended)

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/yourusername/replayer.git
   cd replayer
   ```

2. **Create a virtual environment and install**:
   ```sh
   uv venv
   uv pip install -e .
   ```

3. **Run the CLI**:
   ```sh
   uv run replay --help
   ```

### With pip

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/yourusername/replayer.git
   cd replayer
   ```

2. **Set Up a Virtual Environment**:
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the Package**:
   ```sh
   pip install -e .
   ```

4. **Run the CLI**:
   ```sh
   replay --help
   ```

> **If `pip install -e .` fails**, recreate the venv from scratch:
> ```sh
> rm -rf venv
> python3 -m venv venv
> source venv/bin/activate
> pip install -e .
> ```

## Usage

### Replay events (generate resume output)

```sh
replay events.yaml
```

### Add a new event

```sh
# Add a work event
replay add-event events.yaml event=work company=Acme title=Engineer \
  start_date=2020-01-01 end_date=2022-12-31

# Add an education event
replay add-event events.yaml event=education institution=MIT degree="BS CS" \
  start_date=2010-09-01 end_date=2014-06-01
```

### Update an existing event

```sh
# Update the title of event at index 0
replay update-event events.yaml 0 title="Senior Engineer"
```

### Sample events.yaml

```yaml
- event: work
  company: Sample Company
  title: Software Engineer
  start_date: '2023-01-01'
  end_date: '2023-12-31'

- event: education
  institution: MIT
  degree: BS Computer Science
  start_date: '2010-09-01'
  end_date: '2014-06-01'
```

## Testing

### Run all tests

```sh
uv run python -m unittest discover tests -v
```

### Run a single test file

```sh
uv run python -m unittest tests.test_parser -v
uv run python -m unittest tests.test_engine -v
uv run python -m unittest tests.test_creator -v
uv run python -m unittest tests.test_sample_flow -v
```

### Run a single test case

```sh
uv run python -m unittest tests.test_creator.TestAddEvent.test_add_work_event_to_empty_file -v
```

### Without uv (virtualenv activated)

```sh
python -m unittest discover tests -v
```

### Test coverage

| File | What is tested |
|------|---------------|
| `tests/test_parser.py` | Valid YAML, multiple events, file not found, non-list YAML, empty file |
| `tests/test_engine.py` | Work event, education event, multi-event output, unknown type skipped, empty list |
| `tests/test_creator.py` | Add work/education, multiple adds, new file creation, missing fields, unknown type, update, out-of-range index |
| `tests/test_sample_flow.py` | CLI replay, add-event, update-event, --help, error paths, bad args |

## Contributing

We welcome contributions! Please read our [Contributing Guide](CONTRIBUTING.md) to learn how you can help.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
