from fpdf import FPDF 
pdf = FPDF()      
# Add a page 
pdf.add_page()  
# set style and size of font  
# that you want in the pdf 
pdf.set_font("Arial", size = 15)
# open the text file in read mode 
f = open("path where text file is stored\\File_name.txt", "r") 
# insert the texts in pdf 
for x in f: 
    pdf.cell(50,5, txt = x, ln = 1, align = 'C') 
# save the pdf with name .pdf 
pdf.output("path where you want to store pdf file\\File_name.pdf")