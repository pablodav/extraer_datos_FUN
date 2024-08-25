import camelot

data = '../data/res_731_2122.pdf'

# Read PDF file
tables = camelot.read_pdf(data, pages='all')

# Check if tables were found
if tables:
	for i, table in enumerate(tables):
		print(f"Table {i}")
		print(table.df)  # Print the DataFrame
		table.to_csv(f"output_{i}.csv")  # Export to CSV
else:
	print("No tables found")
 