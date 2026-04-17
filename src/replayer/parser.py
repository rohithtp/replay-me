import yaml

def parse_events(file_path):
    try:
        with open(file_path, 'r') as file:
            events = yaml.safe_load(file)
        if not isinstance(events, list):
            raise ValueError("Events should be a list")
        return events
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return []
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return []
