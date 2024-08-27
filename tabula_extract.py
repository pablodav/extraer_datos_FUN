from tabula import read_pdf

# Specify the path to your PDF file
pdf_file = '../data/res_731_2122.pdf'

# Use the read_pdf function to extract tables
tables = read_pdf(pdf_file, pages='all')

# Print the extracted tables
for i, table in enumerate(tables):
    print(f"Table {i+1}:")
    print(table)
    print("\n")
