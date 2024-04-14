import PyPDF2
import pandas as pd

# Function to split text into sections based on a keyword
def split_text_into_sections(text, keyword):
    sections = []
    current_section = []

    for line in text.split('\n'):
        if keyword.lower() in line.lower():
            if current_section:
                sections.append(' '.join(current_section))
                current_section = []
        current_section.append(line)

    if current_section:
        sections.append(' '.join(current_section))

    return sections

# Open the PDF file
pdf_file = open('example.pdf', 'rb')

# Create a PDF reader object
pdf_reader = PyPDF2.PdfFileReader(pdf_file)

# Initialize an empty list to store extracted text
text_data = []

# Iterate through each page in the PDF
for page_num in range(pdf_reader.numPages):
    # Extract text from the page
    page_text = pdf_reader.getPage(page_num).extractText()
    # Append the extracted text to the list
    text_data.append(page_text)

# Close the PDF file
pdf_file.close()

# Specify the keyword to separate sections
keyword = 'Keyword'

# Initialize an empty list to store sectioned text
sectioned_data = []

# Split each page's text into sections based on the keyword
for text in text_data:
    sections = split_text_into_sections(text, keyword)
    sectioned_data.extend(sections)

# Convert the list of sectioned text data into a pandas DataFrame
df = pd.DataFrame(sectioned_data, columns=['Text'])

# Write the DataFrame to an Excel file
df.to_excel('output.xlsx', index=False)
