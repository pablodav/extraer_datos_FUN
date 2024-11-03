# main.py
import re
from dataclasses import dataclass
from typing import List, Dict, Optional
import sqlite3
import csv

try:
    from PyPDF2 import PdfReader
except ImportError:
    print("PyPDF2 is required. Install it using: pip install PyPDF2")

@dataclass
class Swimmer:
    name: str
    age: Optional[int]
    team: str
    time: str
    points: Optional[float]
    gender: str
    event_number: int
    event_name: str
    
@dataclass
class RelayTeam:
    team_name: str
    relay_order: int
    swimmers: List[Dict[str, str]]  # List of swimmer info dictionaries
    time: str
    points: Optional[float]
    event_number: int
    event_name: str

class SwimmingDataExtractor:
    def __init__(self, text_content):
        self.content = text_content
        self.events = []
        self.swimmers = []
        self.relay_teams = []

    def extract_events(self):
        """Extract all events from the content"""
        event_pattern = r"\s*Evento\s+(\d+)\s+(Mujeres|Hombres|Niñas|Niños|Mixto)\s+(.+?)(?=\s*Evento|\Z)"
        events = re.finditer(event_pattern, self.content, re.DOTALL)
        #import pdb; pdb.set_trace()
        
        for event in events:
            event_num = int(event.group(1))
            event_type = event.group(2)
            event_details = event.group(3).strip()
            self.events.append({
                'number': event_num,
                'type': event_type,
                'details': event_details
            })
            
            # Process event data based on type
            if 'Relevo' in event_details or event_type == 'Mixto':
                self._process_relay_event(event.group(0), event_num)
            else:
                self._process_individual_event(event.group(0), event_num)

    def _process_individual_event(self, event_text: str, event_num: int):
        """Process individual swimming event"""
        lines = event_text.split('\n')
        
        # Get the event title (first line after "Evento X")
        event_title = None
        for line in lines:
            if 'Evento' in line:
                event_title = line.split('Evento')[1].split(None, 2)[2].strip()
                break
                
        # Skip header lines and process results
        start_processing = False
        for line in lines:
            # Skip until we find actual data (after headers)
            if 'Edad' in line or 'Tiempo de Finales' in line:
                start_processing = True
                continue
                
            if start_processing and line.strip():
                # Enhanced pattern to capture team name with spaces
                try:
                    # First, separate the team name (which might contain spaces)
                    team_parts = []
                    age = None
                    name = None
                    time = None
                    points = None
                    
                    parts = line.strip().split()
                    
                    # Process parts from the end (since we know the format of time and points)
                    if parts:
                        # Try to get points (last element if it exists and is numeric)
                        if parts[-1].replace('.', '').isdigit():
                            points = float(parts[-1])
                            parts = parts[:-1]
                            
                        # Get time (will be in format like 2:27,63)
                        if parts and ':' in parts[-1] or ',' in parts[-1]:
                            time = parts[-1].lstrip('x')  # Remove 'x' prefix if present
                            parts = parts[:-1]
                            
                        # Get age and name
                        # Look for a number that could be age (between 10-99)
                        for i, part in enumerate(parts):
                            if part.isdigit() and 10 <= int(part) <= 99:
                                age = int(part)
                                # Everything before this is team name, everything after is swimmer name
                                team_parts = parts[:i]
                                name_parts = parts[i+1:]
                                name = ' '.join(name_parts)
                                break
                                
                        if team_parts and age and name and time:
                            team = ' '.join(team_parts)
                            
                            # Clean up the name (remove position number if present)
                            name = re.sub(r'^\d+\s*', '', name)
                            
                            swimmer = Swimmer(
                                name=name.strip(),
                                age=age,
                                team=team.strip(),
                                time=time.strip(),
                                points=points,
                                gender=self._determine_gender(event_title),
                                event_number=event_num,
                                event_name=event_title
                            )
                            self.swimmers.append(swimmer)
                            
                except Exception as e:
                    print(f"Error processing line in event {event_num}: {line}")
                    print(f"Error details: {str(e)}")
                    continue

    def _process_relay_event(self, event_text: str, event_num: int):
        """Process relay event data"""
        # Extract relay team pattern
        team_pattern = r"([A-Za-z\s]+?)\s+([0-9:,]+)\s+(\d+)"
        swimmer_pattern = r"\d\)\s+([A-Za-zñáéíóúÁÉÍÓÚ\s,]+?)\s+([MW])(\d+)"
        
        lines = event_text.split('\n')
        current_team = None
        
        for line in lines:
            team_match = re.search(team_pattern, line)
            if team_match:
                team_name = team_match.group(1).strip()
                time = team_match.group(2)
                points = float(team_match.group(3))
                current_team = {
                    'name': team_name,
                    'time': time,
                    'points': points,
                    'swimmers': []
                }
            
            swimmer_match = re.search(swimmer_pattern, line)
            if swimmer_match and current_team:
                current_team['swimmers'].append({
                    'name': swimmer_match.group(1).strip(),
                    'gender': 'F' if swimmer_match.group(2) == 'W' else 'M',
                    'age': int(swimmer_match.group(3))
                })
                
                # If we have 4 swimmers, create the relay team
                if len(current_team['swimmers']) == 4:
                    relay_team = RelayTeam(
                        team_name=current_team['name'],
                        relay_order=len(self.relay_teams) + 1,
                        swimmers=current_team['swimmers'],
                        time=current_team['time'],
                        points=current_team['points'],
                        event_number=event_num,
                        event_name=lines[0].strip()
                    )
                    self.relay_teams.append(relay_team)
                    current_team = None

    def _determine_gender(self, event_header: str) -> str:
        """Determine gender from event header"""
        if any(gender in event_header for gender in ['Mujeres', 'Niñas']):
            return 'F'
        return 'M'

    def save_to_sqlite(self, db_path: str):
        """Save extracted data to SQLite database"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create tables
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            event_number INTEGER PRIMARY KEY,
            event_type TEXT,
            event_details TEXT
        )''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS swimmers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            team TEXT,
            time TEXT,
            points REAL,
            gender TEXT,
            event_number INTEGER,
            event_name TEXT,
            FOREIGN KEY (event_number) REFERENCES events (event_number)
        )''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS relay_teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_name TEXT,
            relay_order INTEGER,
            time TEXT,
            points REAL,
            event_number INTEGER,
            event_name TEXT,
            FOREIGN KEY (event_number) REFERENCES events (event_number)
        )''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS relay_swimmers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            relay_team_id INTEGER,
            swimmer_order INTEGER,
            name TEXT,
            gender TEXT,
            age INTEGER,
            FOREIGN KEY (relay_team_id) REFERENCES relay_teams (id)
        )''')

        # Insert data
        for event in self.events:
            cursor.execute('INSERT INTO events VALUES (?, ?, ?)',
                         (event['number'], event['type'], event['details']))

        for swimmer in self.swimmers:
            cursor.execute('''
                INSERT INTO swimmers (name, age, team, time, points, gender, event_number, event_name)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (swimmer.name, swimmer.age, swimmer.team, swimmer.time, 
                 swimmer.points, swimmer.gender, swimmer.event_number, swimmer.event_name))

        for relay in self.relay_teams:
            cursor.execute('''
                INSERT INTO relay_teams (team_name, relay_order, time, points, event_number, event_name)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (relay.team_name, relay.relay_order, relay.time, 
                 relay.points, relay.event_number, relay.event_name))
            
            relay_id = cursor.lastrowid
            for i, swimmer in enumerate(relay.swimmers, 1):
                cursor.execute('''
                    INSERT INTO relay_swimmers (relay_team_id, swimmer_order, name, gender, age)
                    VALUES (?, ?, ?, ?, ?)
                ''', (relay_id, i, swimmer['name'], swimmer['gender'], swimmer['age']))

        conn.commit()
        conn.close()

    def save_to_csv(self, base_filename: str):
        """Save extracted data to CSV files"""
        # Save events
        with open(f'{base_filename}_events.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['event_number', 'event_type', 'event_details'])
            for event in self.events:
                writer.writerow([event['number'], event['type'], event['details']])

        # Save individual swimmers
        with open(f'{base_filename}_swimmers.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'age', 'team', 'time', 'points', 'gender', 'event_number', 'event_name'])
            for swimmer in self.swimmers:
                writer.writerow([swimmer.name, swimmer.age, swimmer.team, swimmer.time,
                               swimmer.points, swimmer.gender, swimmer.event_number, swimmer.event_name])

        # Save relay teams
        with open(f'{base_filename}_relay_teams.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['team_name', 'relay_order', 'time', 'points', 'event_number', 'event_name',
                           'swimmer1', 'gender1', 'age1',
                           'swimmer2', 'gender2', 'age2',
                           'swimmer3', 'gender3', 'age3',
                           'swimmer4', 'gender4', 'age4'])
            
            for relay in self.relay_teams:
                row = [relay.team_name, relay.relay_order, relay.time, relay.points,
                      relay.event_number, relay.event_name]
                for swimmer in relay.swimmers:
                    row.extend([swimmer['name'], swimmer['gender'], swimmer['age']])
                writer.writerow(row)

def process_pdf(pdf_path: str):
    """Process a PDF file and extract swimming competition data"""

    try:
        # Read PDF file
        reader = PdfReader(pdf_path)
        content = ""
        
        # Extract text from all pages
        print("Extracting text from PDF...")
        for page_num, page in enumerate(reader.pages, 1):
            page_text = page.extract_text()
            content += page_text
            print(f"Page {page_num}: Extracted {len(page_text)} characters")
        
        print("\nSample of extracted text (first 500 characters):")
        print(content[:500])
        print("\nTotal characters extracted:", len(content))
        
        # Look for event markers in the text
        event_count = content.count("Evento ")
        print(f"\nFound {event_count} potential events (counting 'Evento ' occurrences)")
        
        # Create extractor instance
        extractor = SwimmingDataExtractor(content)
        
        # Extract all events
        print("\nExtracting events...")
        extractor.extract_events()
        
        # Save to both SQLite and CSV
        print(f"Found {len(extractor.events)} events")
        print(f"Found {len(extractor.swimmers)} individual results")
        print(f"Found {len(extractor.relay_teams)} relay teams")
        
        # Save to SQLite
        #db_path = pdf_path.rsplit('.', 1)[0] + '.db'
        #print(f"Saving to SQLite database: {db_path}")
        #extractor.save_to_sqlite(db_path)
        
        # Save to CSV
        csv_base = pdf_path.rsplit('.', 1)[0]
        print(f"Saving to CSV files with base name: {csv_base}")
        extractor.save_to_csv(csv_base)
        
        print("Processing completed successfully!")
        return extractor  # Return the extractor for potential further use

    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        raise

def check_pdf_structure(content: str):
    """Analyze the PDF content structure and look for potential issues"""
    print("\n=== PDF Structure Analysis ===")
    
    # Check for basic markers
    print("\nChecking basic markers:")
    markers = {
        "Evento": content.count("Evento"),
        "Equipo": content.count("Equipo"),
        "Tiempo": content.count("Tiempo"),
        "Puntos": content.count("Puntos"),
        "Metro": content.count("Metro"),
        "Estilo": content.count("Estilo")
    }
    
    for marker, count in markers.items():
        print(f"{marker}: {count} occurrences")
    
    # Check line endings
    print("\nAnalyzing line structure:")
    lines = content.split('\n')
    print(f"Total lines: {len(lines)}")
    print("\nFirst 10 lines:")
    for i, line in enumerate(lines[:10], 1):
        print(f"{i}: {line[:100]}")  # Show first 100 chars of each line
    
    # Look for event numbers
    event_numbers = re.findall(r"Evento\s+(\d+)", content)
    print(f"\nFound event numbers: {event_numbers[:10]}...")  # Show first 10
    
    # Check for potential encoding issues
    print("\nChecking for special characters:")
    special_chars = set(c for c in content if not c.isascii())
    if special_chars:
        print("Special characters found:", sorted(special_chars))
    
    # Return first occurrence of "Evento" with context
    evento_idx = content.find("Evento")
    if evento_idx >= 0:
        context_start = max(0, evento_idx - 50)
        context_end = min(len(content), evento_idx + 200)
        print("\nFirst 'Evento' occurrence context:")
        print(content[context_start:context_end])
    
    return markers

# Add to main.py:
def main():
    pdf_path = 'data/res_731_2125.pdf'
    
    # Read PDF and get content
    reader = PdfReader(pdf_path)
    content = ""
    for page in reader.pages:
        content += page.extract_text()
    
    # Check PDF structure before processing
    check_pdf_structure(content)
    
    # Process the PDF
    extractor = process_pdf(pdf_path)
    
    return extractor  # Return for further analysis if needed

if __name__ == "__main__":
    main()
