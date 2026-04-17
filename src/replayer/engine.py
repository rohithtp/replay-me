def process_events(events):
    # Enhanced processing logic based on event types
    resume = []
    for event in events:
        if event['event'] == 'work':
            resume.append(f"Worked at {event['company']} as a {event['title']} from {event['start_date']} to {event['end_date']}")
        elif event['event'] == 'education':
            resume.append(f"Studied at {event['institution']} for {event['degree']} from {event['start_date']} to {event['end_date']}")
    return "\n".join(resume)
