import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
import re

def parse_time(time_str):
    if pd.isna(time_str) or str(time_str).strip() in ['Tiempo de Finales', 'DQ', '']:
        return pd.NaT
    time_str = str(time_str).replace('x', '').strip()
    try:
        if ':' in time_str:
            minutes, rest = time_str.split(':')
            seconds, milliseconds = rest.split(',')
            total_seconds = int(minutes) * 60 + int(seconds) + float(f"0.{milliseconds}")
        else:
            seconds, milliseconds = time_str.split(',')
            total_seconds = int(seconds) + float(f"0.{milliseconds}")
        return pd.Timedelta(seconds=total_seconds)
    except ValueError:
        print(f"Warning: Unable to parse time '{time_str}'. Returning NaT.")
        return pd.NaT

def parse_data(content):
    events = []
    current_event = None
    
    for line in content.split('\n'):
        if line.strip().startswith('Evento'):
            if current_event:
                events.append(current_event)
            current_event = {'title': line.strip(), 'data': []}
        elif current_event and ',' in line:
            current_event['data'].append(line)
    
    if current_event:
        events.append(current_event)
    
    return events

def identify_columns(df):
    # Try to identify columns based on content
    name_col = df.apply(lambda x: x.astype(str).str.contains(r'\d+\s*"?[A-Za-z]').any()).idxmax()
    time_col = df.apply(lambda x: x.astype(str).str.contains(r'\d+[,.:]\d+').any()).idxmax()
    team_col = df.apply(lambda x: x.astype(str).str.contains(r'Club|Centro|Piscinas').any()).idxmax()
    
    return name_col, time_col, team_col

def create_dataframe(event):
    data = StringIO('\n'.join(event['data']))
    try:
        df = pd.read_csv(data, header=None, quotechar='"', on_bad_lines='warn')
    except pd.errors.EmptyDataError:
        print(f"Warning: No parseable data found for event {event['title']}")
        return pd.DataFrame()

    df = df.dropna(how='all')  # Drop empty rows
    
    name_col, time_col, team_col = identify_columns(df)
    
    if name_col is not None and time_col is not None and team_col is not None:
        df = df[[name_col, team_col, time_col]]
        df.columns = ['Name', 'Team', 'Time']
        
        # Clean and extract name and age
        df['Name'] = df['Name'].astype(str).str.replace(r'^\d+\s*', '', regex=True)
        df[['Name', 'Age']] = df['Name'].str.extract(r'([^,]+),\s*(.+)')
        df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
        
        df['Time'] = df['Time'].apply(parse_time)
        df = df.dropna(subset=['Time'])
        return df
    else:
        print(f"Warning: Could not identify required columns for event {event['title']}")
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

def plot_event(event, df):
    if df.empty:
        print(f"\nSkipping plotting for {event['title']} due to parsing issues.")
        return
    
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='Team', y='Time', data=df)
    plt.title(f"Time Distribution by Team - {event['title']}")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Age', y='Time', hue='Team', data=df)
    plt.title(f"Time vs Age by Team - {event['title']}")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

def main(content):
    events = parse_data(content)
    
    for event in events:
        df = create_dataframe(event)
        analyze_event(event, df)
        plot_event(event, df)


# Sample usage
# if needed you can use:
# sample_content = ''' 
# content here
# '''
with open('output.txt', 'r') as file:
    sample_content = file.read()

if __name__ == "__main__":
    main(sample_content)
