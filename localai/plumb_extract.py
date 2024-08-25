import pdfplumber

data = '../data/res_731_2122.pdf'

# Open PDF file
with pdfplumber.open(data) as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                print(row)
