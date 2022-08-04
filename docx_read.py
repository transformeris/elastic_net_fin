import docx
doc=docx.Document('C:/Users\梁海镇\Desktop\执照考证题库.docx')
# docx.opendocx('C:/Users\梁海镇\Desktop\执照考证题库.docx')
zz=doc.paragraphs[120].text
res={}
for num in range(100):#range(len(doc.paragraphs)):
    print(doc.paragraphs[num].text)
    if '.' in doc.paragraphs[num].text:
        timu=doc.paragraphs[num].text.split('.')
        try:
            float(timu[0])
            res[num]=timu
        except:
            pass