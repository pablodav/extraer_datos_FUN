from tabula import read_pdf

# Specify the path to your PDF file
# pdf_file = 'data/res_731_2122.pdf'
pdf_file = 'data/res_731_2125.pdf'

# Use the read_pdf function to extract tables
tables = read_pdf(pdf_file, pages='all')

# Print a descriptive message to indicate that the tables have been extracted
print("Tables have been successfully extracted from the PDF file.")

# Loop through each table and print a message indicating its number
for i, table in enumerate(tables):
    print(f"Table {i+1}:")
    print("\n")

    # Print the table for easier viewing
    print(table)
    print("\n")

    # Save the table to a CSV file for future analysis (if required)
    table.to_csv(f"data/extract3/table_{i+1}.csv", index=False)
