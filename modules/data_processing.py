import pandas as pd
from io import StringIO

# Example widths of data
#      1  Gallino, Camila                        17  Piscinas Barriales DE Salto                                     2:27,63                 9
# widths = [9, 39, 5, 64, 23, 2]
widths = [7, 37, 5, 63, 22, 10] 

def create_dataframes_from_sections(text, keyword='Evento '):
    """Creating sections from text and return pandas dataframes of these

    Args:
        text (_type_): Text with a section keyword on an specific line
        keyword (str, optional): keyword for the section. Defaults to 'Evento '.

    Returns:
        list: list of dataframes
    """
    # Define the column names
    column_names = ['Number', 'Name', 'Age', 'Team', 'Time', 'Points']

    # Define the widths of the fields
    widths = [7, 37, 5, 63, 22, 10] 
 
    # Split the text into sections
    sections = text.split(keyword)

    # Initialize an empty list to hold the dataframes
    dataframes = []

    # Process each section
    for section in sections:
        # Split the section into lines
        lines = section.splitlines()
        # Skip empty lines
        if not lines:
            continue
        
        # Use the first line as the "evento" data and the rest as the dataframe data
        evento = lines[0]
        # Remove the parentheses from the "evento" data
        evento = evento.replace('(', '')
        evento = evento.replace(')', '')
        # Split each line into columns and store the results in a list of lists
        # data = [line.split() for line in lines[1:]]
        # Start from second line section to skip section headers
        data = '\n'.join(section.splitlines()[2:])

        # Create a dataframe from the data using the defined column names and field widths
        df = pd.read_fwf(StringIO(data), widths=widths, names=column_names)

        # df = pd.DataFrame(data)
        
        # Add the "evento" data as a new column
        df['evento'] = evento
        df['evento_short'] = evento[:24]
        
        dataframes.append(df)

    return dataframes
