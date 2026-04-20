import sys
from replayer.engine import process_events
from replayer.parser import parse_events
from replayer.creator import add_event, update_event

HELP = """Hey! Use replay <command> [options]

Commands:
  <events_file>              Parse and print resume from events file
  add-event <file> [fields]  Append a new event to the events file
  update-event <file> <idx>  Update fields of an existing event by index

Add-event field format (key=value pairs):
  replay add-event events.yaml event=work company=Acme title=Engineer \\
    start_date=2020-01-01 end_date=2022-12-31

Update-event example:
  replay update-event events.yaml 0 title="Senior Engineer"

Options:
  --help, -h   Show this help message and exit
"""


def _parse_kv(args):
    result = {}
    for arg in args:
        if '=' not in arg:
            print(f"Invalid field format '{arg}', expected key=value")
            sys.exit(1)
        k, v = arg.split('=', 1)
        result[k.strip()] = v.strip()
    return result


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('--help', '-h'):
        print(HELP)
        sys.exit(0)

    command = sys.argv[1]

    if command == 'add-event':
        if len(sys.argv) < 4:
            print("Usage: replay add-event <events_file> event=<type> [field=value ...]")
            sys.exit(1)
        file_path = sys.argv[2]
        fields = _parse_kv(sys.argv[3:])
        try:
            idx = add_event(file_path, fields)
            print(f"Event added at index {idx} in {file_path}")
        except (ValueError, OSError) as e:
            print(f"Error: {e}")
            sys.exit(1)

    elif command == 'update-event':
        if len(sys.argv) < 5:
            print("Usage: replay update-event <events_file> <index> [field=value ...]")
            sys.exit(1)
        file_path = sys.argv[2]
        try:
            index = int(sys.argv[3])
        except ValueError:
            print(f"Index must be an integer, got '{sys.argv[3]}'")
            sys.exit(1)
        updates = _parse_kv(sys.argv[4:])
        try:
            event = update_event(file_path, index, updates)
            print(f"Updated event at index {index}: {event}")
        except (ValueError, IndexError, OSError) as e:
            print(f"Error: {e}")
            sys.exit(1)

    else:
        events_file = command
        events = parse_events(events_file)
        if not events:
            print("No valid events found.")
            sys.exit(1)
        print(process_events(events))


if __name__ == "__main__":
    main()
