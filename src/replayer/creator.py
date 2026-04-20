import yaml
from datetime import date

REQUIRED_FIELDS = {
    'work': ['company', 'title', 'start_date', 'end_date'],
    'education': ['institution', 'degree', 'start_date', 'end_date'],
}


def _load(file_path):
    try:
        with open(file_path, 'r') as f:
            events = yaml.safe_load(f) or []
        if not isinstance(events, list):
            raise ValueError("Events file must contain a YAML list")
        return events
    except FileNotFoundError:
        return []


def _save(file_path, events):
    with open(file_path, 'w') as f:
        yaml.dump(events, f, default_flow_style=False, sort_keys=False)


def _validate(event):
    kind = event.get('event')
    if kind not in REQUIRED_FIELDS:
        raise ValueError(f"Unknown event type '{kind}'. Known types: {list(REQUIRED_FIELDS)}")
    missing = [f for f in REQUIRED_FIELDS[kind] if not event.get(f)]
    if missing:
        raise ValueError(f"Missing required fields for '{kind}': {missing}")


def add_event(file_path, event):
    _validate(event)
    events = _load(file_path)
    events.append(event)
    _save(file_path, events)
    return len(events) - 1  # index of the new event


def update_event(file_path, index, updates):
    events = _load(file_path)
    if index < 0 or index >= len(events):
        raise IndexError(f"No event at index {index} (file has {len(events)} events)")
    events[index].update(updates)
    _validate(events[index])
    _save(file_path, events)
    return events[index]
