from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.converter import PDFPageAggregator
import io
# Open a PDF file.
fp = open(r'D:\onedrive\文档\WXWork Files\File\2023-04\图纸\图纸\500 千伏鳌峰开关站扩建第一台主变工程电气二次图纸\D0202\446-B50081S-D0202-19 主变小室监控交换机屏一端子排图.pdf', 'rb')
# Create a PDF parser object associated with the file object.
parser = PDFParser(fp)
# Create a PDF document object that stores the document structure.
document = PDFDocument(parser)
# Check if the document allows text extraction. If not, abort.

# Create a PDF resource manager object that stores shared resources.
rsrcmgr = PDFResourceManager()
# Create a PDF device object.
device = PDFDevice(rsrcmgr)
# Create a PDF interpreter object.
interpreter = PDFPageInterpreter(rsrcmgr, device)
# Process each page contained in the document.
for page in PDFPage.create_pages(document):
    # Create a PDF page aggregator object.
    aggregator = PDFPageAggregator(rsrcmgr, laparams=LAParams())
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, aggregator)
    # Use the interpreter to process the page.
    interpreter.process_page(page)
    # Get the text data from the page aggregator.
    layout = aggregator.get_result()
    for lt_obj in layout:
        if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
            text = lt_obj.get_text()
            print(text.encode('utf-8').decode('utf-8'))