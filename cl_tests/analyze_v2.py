import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
import re
import os

def parse_time(time_str):
    if pd.isna(time_str) or str(time_str).strip() in ['Tiempo de Finales', 'DQ', '', 'Puntos']:
        return pd.NaT
    time_str = str(time_str).replace('x', '').replace('X', '').strip()
    try:
        if ':' in time_str:
            parts = time_str.replace(',', '.').split(':')
            if len(parts) == 3:  # Format: hh:mm:ss.ms
                return pd.Timedelta(hours=float(parts[0]), minutes=float(parts[1]), seconds=float(parts[2]))
            elif len(parts) == 2:  # Format: mm:ss.ms
                return pd.Timedelta(minutes=float(parts[0]), seconds=float(parts[1]))
        elif ',' in time_str:
            seconds, milliseconds = time_str.split(',')
            return pd.Timedelta(seconds=float(seconds), milliseconds=float(milliseconds))
        else:
            return pd.Timedelta(seconds=float(time_str))
    except ValueError:
        return pd.NaT

def parse_data(content):
    events = []
    current_event = None
    
    for line in content.split('\n'):
        if line.strip().startswith('Evento'):
            if current_event:
                events.append(current_event)
            current_event = {'title': line.strip(), 'data': []}
        elif current_event:
            current_event['data'].append(line)
    
    if current_event:
        events.append(current_event)
    
    return events

def create_dataframe(event):
    data = StringIO('\n'.join(event['data']))
    try:
        df = pd.read_csv(data, header=None, quotechar='"', on_bad_lines='warn')
    except pd.errors.EmptyDataError:
        print(f"Warning: No parseable data found for event {event['title']}")
        return pd.DataFrame()

    df = df.dropna(how='all')  # Drop empty rows
    
    # Remove header rows and non-data rows
    df = df[df[0].str.contains(r'^\d+\s*"?[A-Za-z]', na=False)]
    
    # Identify the time column
    time_col = df.apply(lambda x: x.astype(str).str.contains(r'\d+[,.:]\d+').sum()).idxmax()
    
    if time_col is not None:
        # Assume the name is in the first column and the time is in the identified time column
        df = df[[0, time_col]]
        df.columns = ['Name', 'Time']
        
        # Clean and extract name and age
        df['Name'] = df['Name'].astype(str).str.replace(r'^\d+\s*', '', regex=True)
        df['Name'] = df['Name'].str.replace('"', '')
        df[['Name', 'Age']] = df['Name'].str.extract(r'([^,]+),\s*(.+)')
        df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
        
        df['Time'] = df['Time'].apply(parse_time)
        df = df.dropna(subset=['Time', 'Name'])
        return df
    else:
        print(f"Warning: Could not identify time column for event {event['title']}")
        return pd.DataFrame()

def analyze_event(event, df):
    if df.empty:
        print(f"\nSkipping analysis for {event['title']} due to parsing issues.")
        return
    
    print(f"\nAnalyzing {event['title']}")
    print(f"Number of participants: {len(df)}")
    print(f"Average time: {df['Time'].mean()}")
    print(f"Fastest time: {df['Time'].min()}")
    print(f"Slowest time: {df['Time'].max()}")

def plot_event(event, df, output_dir):
    if df.empty:
        print(f"\nSkipping plotting for {event['title']} due to parsing issues.")
        return
    
    event_name = re.sub(r'[^\w\-_\. ]', '_', event['title'])
    
    plt.figure(figsize=(12, 6))
    sns.histplot(df['Time'], kde=True)
    plt.title(f"Time Distribution - {event['title']}")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{event_name}_distribution.png"))
    plt.close()

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Age', y='Time', data=df)
    plt.title(f"Time vs Age - {event['title']}")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{event_name}_scatter.png"))
    plt.close()

def process_event(event, output_dir):
    df = create_dataframe(event)
    analyze_event(event, df)
    plot_event(event, df, output_dir)
    # Clear memory
    del df
    plt.close('all')

def main(content, output_dir, max_events=None):
    events = parse_data(content)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for i, event in enumerate(events):
        if max_events is not None and i >= max_events:
            break
        process_event(event, output_dir)

# Sample usage
output_directory = 'swimming_analysis_output'
max_events_to_process = 10  # Set to None to process all events

with open('output.txt', 'r') as file:
    sample_content = file.read()

if __name__ == "__main__":
    main(sample_content, output_directory, max_events_to_process)
