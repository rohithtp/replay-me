import sys
from replayer.engine import process_events
from replayer.parser import parse_events

def main():
    if len(sys.argv) != 2:
        print("Usage: replay <events_file>")
        sys.exit(1)

    events_file = sys.argv[1]
    events = parse_events(events_file)
    resume = process_events(events)
    print(resume)

if __name__ == "__main__":
    main()
