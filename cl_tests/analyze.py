import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO

def parse_time(time_str):
    if pd.isna(time_str):
        return pd.NaT
    time_str = time_str.replace('x', '').strip()
    try:
        minutes, rest = time_str.split(':')
        seconds, milliseconds = rest.split(',')
        total_seconds = int(minutes) * 60 + int(seconds) + float(f"0.{milliseconds}")
        return pd.Timedelta(seconds=total_seconds)
    except ValueError:
        print(f"Warning: Unable to parse time '{time_str}'. Returning NaT.")
        return pd.NaT

def parse_data(content):
    events = []
    current_event = None
    
    for line in content.split('\n'):
        if line.startswith('Evento'):
            if current_event:
                events.append(current_event)
            current_event = {'title': line.strip(), 'data': []}
        elif current_event and ',' in line and len(line.split(',')) > 3:
            current_event['data'].append(line)
    
    if current_event:
        events.append(current_event)
    
    return events

def create_dataframe(event):
    data = StringIO('\n'.join(event['data']))
    df = pd.read_csv(data, header=None, quotechar='"')
    df.columns = ['Name', 'Age', 'Team', 'Unused', 'Time', 'Points']
    df['Time'] = df['Time'].apply(parse_time)
    df = df.dropna(subset=['Time'])
    return df

def analyze_event(event, df):
    print(f"\nAnalyzing {event['title']}")
    print(f"Number of participants: {len(df)}")
    print(f"Average time: {df['Time'].mean()}")
    print(f"Fastest time: {df['Time'].min()}")
    print(f"Slowest time: {df['Time'].max()}")

def plot_event(event, df):
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='Team', y='Time', data=df)
    plt.title(f"Time Distribution by Team - {event['title']}")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Age', y='Time', hue='Team', data=df)
    plt.title(f"Time vs Age by Team - {event['title']}")
    plt.tight_layout()
    plt.show()

def main(content):
    events = parse_data(content)
    
    for event in events:
        df = create_dataframe(event)
        analyze_event(event, df)
        plot_event(event, df)

# Sample usage
sample_content = '''
Evento 98  Mujeres 14-15 100 CC Metro Estilo de Pecho
"1 Hurst, Belen",14,Club Nacional Nueva Helvecia,,"1:24,84",9
"2 Bertinat, Fiorella",14,Club Nacional Nueva Helvecia,,"1:30,08",7
"3 Ashby, Julieta",14,Centro Sportivo Laureles,,"1:32,83",6
"4 Gomensoro, Malena",15,Carrasco Lawn Tennis Club,,"1:33,24",5
"5 Martinez, Mercedes",14,Carrasco Lawn Tennis Club,,"1:38,18",4
"6 Espindola, Aldana",15,Club Social y Deportivo Delfin,,"1:39,40",3

Evento 99  Hombres 14-15 100 CC Metro Estilo de Pecho
"1 Paez, Juan Pedro",15,Carrasco Lawn Tennis Club,,"1:22,44",9
"2 Sonderegger, Paulino",15,Club Nacional Nueva Helvecia,,"1:29,48",7
"3 Voelker, Felipe",15,Centro Sportivo Laureles,,"1:30,14",6
"4 Ferres, Benjamin",14,Club Social y Deportivo Delfin,,"1:30,66",5
"5 Demasi, Valentino",15,Club Social y Deportivo Delfin,,"1:32,62",4
"6 Martinez, Ignacio",14,Club Social y Deportivo Delfin,,"x1:33,97",
'''

if __name__ == "__main__":
    main(sample_content)

# import os

# def read_csv_files(directory):
#     content = ""
#     for filename in os.listdir(directory):
#         if filename.endswith(".csv"):
#             with open(os.path.join(directory, filename), 'r') as file:
#                 content += file.read() + "\n"
#     return content

# # Replace 'your_directory_path' with the path to the directory containing your CSV files
# data_content = read_csv_files('your_directory_path')
# main(data_content)
