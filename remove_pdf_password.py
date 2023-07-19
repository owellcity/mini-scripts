import os
import pikepdf # install via pip

# Removes pdf password
# Assumes pdf files have the same password and in the same directory with this script
pdf_files = os.listdir()
pdf_files = [x for x in pdf_files if ".pdf" in x]

cwd = os.getcwd()

pdf_pass = ""
for i in pdf_files:
    pdf_path = "{}/{}".format(cwd, i)
    print(pdf_path)
    pdf = pikepdf.open(pdf_path, password=pdf_pass, allow_overwriting_input=True)
    pdf.save(pdf_path)

    print("Password removed!")

#reference: https://medium.com/geekculture/simply-removing-pdf-password-using-python-8966700089c9
