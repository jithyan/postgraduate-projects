import re
import requests
import subprocess
from multiprocessing import Pool

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


def read_file_text(file_path):
   with open(file_path, "r") as f:
      return f.read();


def parse_urls(text):
   url_reg = re.compile(r"PP\d+.pdf https://drive.google.com/uc\?export=download&id=[\w-]+\s")
   matches = re.findall(url_reg, text)
   file_url_list = [match.rstrip().split(' ') for match in matches]
   file_to_url = {}
   for item in file_url_list:
      file_to_url[item[0]] = item[1]
   
   return file_to_url

def download_files(file_urls, download_location):
   for file_name, url in file_urls.items():
      resp = requests.get(url, verify=False)
      with open("{0}{1}".format(download_location, file_name), "wb") as f:
         f.write(resp.content)

def write_pdf_to_txt_file(pdf_path):
      txt_path = re.sub(".pdf", ".txt", pdf_path)
      print(txt_path)
      with open(txt_path, "w", encoding="utf-16") as txt_file:
         txt_file.write(convert_pdf_to_txt(pdf_path))

def convert_list(pdf_paths):
   for pdf_path in pdf_paths:
      write_pdf_to_txt_file(pdf_path)

if __name__ == "__main__":
   i = 0
   j = 20
   increment = 20
   pfdtext = read_file_text(r"D:\Workspace\postgraduate-projects\data-wrangling-asg2\Group059.txt")
   urls = parse_urls(pfdtext)
   #download_files(urls, "D:\\Workspace\\postgraduate-projects\\data-wrangling-asg2\\")
   pool = Pool(processes=10)
   pdfs = list(map(lambda fn: r"D:\Workspace\postgraduate-projects\data-wrangling-asg2\{0}".format(fn), list(urls.keys())))
   while j <= 200:
      res = pool.apply_async(convert_list, [pdfs[i:j]])
      i = i + increment
      j = j + increment
      res.get()
   print("fin")
   """
   pdf_to_text = {}
   for filename, path in urls.items():
      i += 1
      pdf_to_text[filename] = convert_pdf_to_txt(r"D:\Workspace\postgraduate-projects\data-wrangling-asg2\{0}".format(filename))
      if (i == 2):
         break

   print(len(pdf_to_text.keys()))
   print(pdf_to_text.values())
   """