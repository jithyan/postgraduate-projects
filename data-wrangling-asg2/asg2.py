import re
import requests
from multiprocessing import Pool
from collections import namedtuple

from itertools import chain
from nltk.tokenize import RegexpTokenizer
import nltk.data

# Related to PDFminer
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

CURR_DIR = "D:\\Workspace\\postgraduate-projects\\data-wrangling-asg2\\"
PaperDetail = namedtuple("PaperDetail", "id url")


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = "utf-8"
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, "rb")
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(
        fp,
        pagenos,
        maxpages=maxpages,
        password=password,
        caching=caching,
        check_extractable=True,
    ):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


def read_file_text(file_path):
    with open(file_path, "r", encoding="utf-16") as f:
        return f.read()


def parse_paper_details(text):
    url_reg = re.compile(
        r"PP\d+.pdf https://drive.google.com/uc\?export=download&id=[\w-]+\s"
    )
    matches = re.findall(url_reg, text)

    file_url_list = [match.rstrip().split(" ") for match in matches]
    file_details = []

    for item in file_url_list:
        file_details.append(PaperDetail(re.sub(".pdf", "", item[0]), item[1]))

    return file_details


def download_files(paper_details):
    for detail in paper_details:
        resp = requests.get(detail.url)
        with open("{0}{1}.pdf".format(CURR_DIR, detail.id), "wb") as f:
            f.write(resp.content)


def write_pdf_to_txt_file(pdf_path):
    txt_path = re.sub(".pdf", ".txt", pdf_path)
    print(txt_path)
    with open(txt_path, "w", encoding="utf-16") as txt_file:
        txt_file.write(convert_pdf_to_txt(pdf_path))


def convert_pdfs(pdf_paths):
    for pdf_path in pdf_paths:
        write_pdf_to_txt_file(pdf_path)


def parse_download_convert_pdfs():
    pool = Pool(processes=6)
    chunk_size = 20

    write_pdf_to_txt_file(CURR_DIR + "Group059.pdf")
    print("converted url pdf to txt")

    paper_details = parse_paper_details(read_file_text(CURR_DIR + "Group059.txt"))

    for i in range(0, len(paper_details), chunk_size):
        res = pool.apply_async(download_files, [paper_details[i : i + chunk_size]])
        res.get()
    print("finished downloading")

    pdfs = ["{0}{1}.pdf".format(CURR_DIR, pd.id) for pd in paper_details]
    for i in range(0, len(pdfs), chunk_size):
        res = pool.apply_async(convert_pdfs, [pdfs[i : i + chunk_size]])
        res.get()
    print("finished conversion")

    pool.close()


class Paper:
    __body_r = re.compile(r"1 Paper Body[\s\S]+2 References")
    __ref_title = re.compile(r"2 References")
    __paper_body_title = re.compile(r"1 Paper Body\s")
    __title_r = re.compile("")
    __abstract_r = re.compile("")
    __author_r = re.compile("")

    @staticmethod
    def __extract_body(text):
        body = re.search(Paper.__body_r, text).group()
        body = re.sub(Paper.__ref_title, "", body)
        body = re.sub(Paper.__paper_body_title, "", body)

        return body.strip()

    @staticmethod
    def __extract_abstract(text):
        return text

    @staticmethod
    def __extract_title(text):
        return text

    @staticmethod
    def __extract_authors(text):
        return []

    def __init__(self, raw_text, id):
        self.id = id
        self.body = Paper.__extract_body(raw_text)
        self.title = Paper.__extract_title(raw_text)
        self.abstract = Paper.__extract_abstract(raw_text)
        self.authors = Paper.__extract_authors(raw_text)


def parse_papers():
    paper_details = parse_paper_details(read_file_text(CURR_DIR + "Group059.txt"))
    papers = []
    for detail in paper_details:
        full_text = read_file_text("{0}{1}.txt".format(CURR_DIR, detail.id))
        papers.append(Paper(full_text, detail.id))

    return papers


def load_stopwords():
    with open(CURR_DIR + "stopwords_en.txt", "r") as f:
        txt = f.read()
        return set(txt.split("\n"))


def filter_tokens(f, token_list):
    return [t for t in token_list if f(t) is True]


def extract_unigram_tokens(paper_body, stopwords):
    tokenizer = RegexpTokenizer(r"[A-Za-z]\w+(?:[-'?]\w+)?")
    sent_detector = nltk.data.load("tokenizers/punkt/english.pickle")

    sentences = sent_detector.tokenize(paper_body)    
    tokenized_sentences = [tokenizer.tokenize(s) for s in sentences]
    for s in tokenized_sentences:
        if len(s) > 0:
            s[0] = s[0].lower()

    tokenized_sents_no_stopwords = [
        filter_tokens(lambda token: token not in stopwords, s)
        for s in tokenized_sentences
    ]

    tokenized_sents_gt_2_no_stopwords = [
        filter_tokens(lambda token: len(token) > 2, s) 
        for s in tokenized_sents_no_stopwords
    ]
    return list(chain.from_iterable(tokenized_sents_gt_2_no_stopwords))


def get_top_200_bigrams(token_list):
    return []


def multiword_tokenizer(token_list, bigram_list):
    return []


def stem_tokens(token_list):
    return token_list


def filter_rare_tokens(token_list):
    return token_list


def generate_vocab(token_list):
    return {}


def gen_sparse_vector(token_list):
    return {}


if __name__ == "__main__":
    #parse_download_convert_pdfs()
    papers = parse_papers()
    stopwords = load_stopwords()

    tokenized_bodies = {}

    for paper in papers:
        tokenized_bodies[paper.id] = extract_unigram_tokens(paper.body, stopwords)
    print(tokenized_bodies["PP3387"])
