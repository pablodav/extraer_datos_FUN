To extract tables from a PDF using Python, you have several options. While tabula is a popular choice, you can also use other libraries like camelot-py or pdfplumber. Here's a brief overview of each:

```python
import tabula

# Read PDF file
df = tabula.read_pdf("sample.pdf", pages='all')

# Convert PDF into CSV
tabula.convert_into("sample.pdf", "output.csv", output_format="csv", pages='all')
```

Using camelot-py
camelot-py is another library that can extract tables from PDFs. It works well with PDFs that have a consistent structure.

```python
import camelot

# Read PDF file
tables = camelot.read_pdf("sample.pdf", pages='all')

# Export tables to CSV
for i, table in enumerate(tables):
    table.to_csv(f"output_{i}.csv")
```
Using pdfplumber
pdfplumber is a library that allows you to extract text, tables, and metadata from PDFs.

```python
import pdfplumber

# Open PDF file
with pdfplumber.open("sample.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                print(row)
```

Summary
* tabula-py: Good for simple table extraction.
* camelot-py: Better for PDFs with consistent table structures.
* pdfplumber: More flexible and can handle complex PDFs.

Choose the library that best fits your needs based on the structure and complexity of your PDF files.

