import fitz  # PyMuPDF

data = '../data/res_731_2122.pdf'

# Open the PDF file
pdf_document = fitz.open(data)

for page_num in range(len(pdf_document)):
	page = pdf_document.load_page(page_num)
	text = page.get_text("text")
	print(f"Page {page_num + 1}")
	print(text)
 