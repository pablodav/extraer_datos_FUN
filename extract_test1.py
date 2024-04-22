import os
from pypdf import PdfReader
from os import path
import pandas as pd

# Get the directory of the current script
# use os.getcwd() if working interactively instead
script_dir = os.path.dirname(os.path.realpath(__file__))

# print("Current working directory:", os.getcwd())
print("Directory of the current script:", script_dir)

# get full path for data path folder
data_path = path.join(script_dir, 'data')
# Resultados por prueba
resultado_prueba_pdf = path.join(data_path, 'res_731_2125.pdf')

# Reader pdf
reader = PdfReader(resultado_prueba_pdf)
page = reader.pages[0]
print(page.extract_text(extraction_mode='layout', layout_mode_scale_weight=0.5))

# create a dataframe with the extracted text
# Extract text without the first 4 lines
extracted_text = page.extract_text(extraction_mode='layout', layout_mode_scale_weight=0.5)
lines = extracted_text.splitlines()
lines_after_removal = lines[4:]

# Join the lines back together
extracted_text = '\n'.join(lines_after_removal)

def create_dataframes_from_sections(text, keyword='Evento '):
    """Creating sections from text and return pandas dataframes of these

    Args:
        text (_type_): Text with a section keyword on an specific line
        keyword (str, optional): keyword for the section. Defaults to 'Evento '.

    Returns:
        list: list of dataframes
    """
    # Split the text into sections
    sections = text.split(keyword)

    # Initialize an empty list to hold the dataframes
    dataframes = []

    # Process each section
    for section in sections:
        # Split the section into lines
        lines = section.splitlines()
        
        # Use the first line as the "evento" data and the rest as the dataframe data
        evento = lines[0]
        # Split each line into columns and store the results in a list of lists
        data = [line.split() for line in lines[1:]]

        # Create a dataframe from the list of lists and add it to the list of dataframes
        df = pd.DataFrame(data)
        
        # Add the "evento" data as a new column
        df['evento'] = evento
        
        dataframes.append(df)

    return dataframes

# Create a dataframe with the extracted text
data = {'Extracted Text': [extracted_text]}

# Create dataframes from the extracted text
dataframes = create_dataframes_from_sections(extracted_text)

# Print the dataframes
for df in dataframes:
    print(df)

