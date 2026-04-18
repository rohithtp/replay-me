import sys
from replayer.engine import process_events
from replayer.parser import parse_events

def main():
    if len(sys.argv) < 2:
        print("Usage: replay [--help] <events_file>")
        print("Options:")
        print("  --help, -h   Show this help message and exit")
        sys.exit(1)

    if sys.argv[1] in ['--help', '-h']:
        print("Usage: replay [--help] <events_file>")
        print("Options:")
        print("  --help, -h   Show this help message and exit")
        sys.exit(0)

    events_file = sys.argv[1]
    events = parse_events(events_file)
    if not events:
        print("No valid events found.")
        sys.exit(1)
    resume = process_events(events)
    print(resume)

if __name__ == "__main__":
    main()
