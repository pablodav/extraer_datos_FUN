# debug_helpers.py

def print_extraction_summary(extractor):
    """Print a summary of extracted data for debugging"""
    print("\n=== Extraction Summary ===")
    
    print("\nEvents:")
    for event in extractor.events[:3]:  # Show first 3 events
        print(f"Event {event['number']}: {event['type']} - {event['details'][:50]}...")
    
    print(f"\nTotal Events: {len(extractor.events)}")
    
    print("\nSample Individual Results:")
    for swimmer in extractor.swimmers[:3]:  # Show first 3 swimmers
        print(f"{swimmer.name} ({swimmer.age}) - {swimmer.team} - {swimmer.time}")
    
    print(f"\nTotal Individual Results: {len(extractor.swimmers)}")
    
    print("\nSample Relay Teams:")
    for relay in extractor.relay_teams[:3]:  # Show first 3 relay teams
        print(f"\n{relay.team_name} - {relay.time}")
        for i, swimmer in enumerate(relay.swimmers, 1):
            print(f"  {i}. {swimmer['name']} ({swimmer['gender']}{swimmer['age']})")
    
    print(f"\nTotal Relay Teams: {len(extractor.relay_teams)}")

def verify_data_consistency(extractor):
    """Check for common data issues"""
    issues = []
    
    # Check for missing data in individual results
    for i, swimmer in enumerate(extractor.swimmers):
        if not swimmer.name or not swimmer.team or not swimmer.time:
            issues.append(f"Incomplete data for swimmer at index {i}: {swimmer}")
    
    # Check relay teams
    for i, relay in enumerate(extractor.relay_teams):
        if len(relay.swimmers) != 4:
            issues.append(f"Relay team at index {i} has {len(relay.swimmers)} swimmers instead of 4")
    
    # Check for duplicate event numbers
    event_numbers = [event['number'] for event in extractor.events]
    if len(event_numbers) != len(set(event_numbers)):
        issues.append("Duplicate event numbers found")
    
    return issues

# Example usage in main.py:
"""
def main():
    pdf_path = 'res_731_2125.pdf'
    extractor = process_pdf(pdf_path)
    
    # Print detailed summary
    print_extraction_summary(extractor)
    
    # Check for data issues
    issues = verify_data_consistency(extractor)
    if issues:
        print("\nData Issues Found:")
        for issue in issues:
            print(f"- {issue}")
    else:
        print("\nNo data issues found!")
"""