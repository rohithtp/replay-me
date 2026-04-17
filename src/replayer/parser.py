import yaml

def parse_events(file_path):
    with open(file_path, 'r') as file:
        events = yaml.safe_load(file)
    return events
