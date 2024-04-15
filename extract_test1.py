import os
from pypdf import PdfReader
from os import path
import pandas as pd

# Get the directory of the current script
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
# Extract text
extracted_text = page.extract_text(extraction_mode='layout', layout_mode_scale_weight=0.5)
lines = extracted_text.splitlines()
lines_after_removal = lines[4:]

# Join the lines back together
extracted_text = '\n'.join(lines_after_removal)

# Create a dataframe with the extracted text
data = {'Extracted Text': [extracted_text]}
df = pd.DataFrame(data)
print(df)

