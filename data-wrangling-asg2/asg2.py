import re
import requests
from multiprocessing import Pool
from collections import namedtuple
from itertools import chain
from collections import defaultdict

import json

from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import MWETokenizer
import nltk.data
from nltk.probability import FreqDist
from nltk.collocations import *
from nltk.stem import PorterStemmer

# Related to PDFminer
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

CURR_DIR = "D:\\Workspace\\postgraduate-projects\\data-wrangling-asg2\\"
PaperDetail = namedtuple("PaperDetail", "id url")


def convert_pdf_to_txt(path):
    """
    Function to conveniently convert a PDF to text in Python itself.
    Lifted from:
    https://stackoverflow.com/questions/26494211/extracting-text-from-a-pdf-file-using-pdfminer-in-python
    """
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
    """
    Helper function to read the text in UTF-16 from a file
    """
    with open(file_path, "r", encoding="utf-16") as f:
        return f.read()


def parse_paper_details(text):
    """
    Parse the IDs and URLs from the PDF with a list of URLs
    """
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
    """
    Download using the given URLs to a file with the name {paper_id}.pdf
    """
    for detail in paper_details:
        resp = requests.get(detail.url)
        with open("{0}{1}.pdf".format(CURR_DIR, detail.id), "wb") as f:
            f.write(resp.content)


def write_pdf_to_txt_file(pdf_path):
    """
    Convert a given PDF to a TXT file
    """
    txt_path = re.sub(".pdf", ".txt", pdf_path)
    print(txt_path)
    with open(txt_path, "w", encoding="utf-16") as txt_file:
        txt_file.write(convert_pdf_to_txt(pdf_path))


def convert_pdfs(pdf_paths):
    """
    Convert the pdfs in a given list of pdf paths to text files
    """
    for pdf_path in pdf_paths:
        write_pdf_to_txt_file(pdf_path)


def parse_download_convert_pdfs():
    """
    Convert the PDF with a list of URLs to text, parse the filenames and URLS,
    then download each PDF and convert the pdf to text.
    """
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
    """
    Read all the converted paper texts and parse their body, titles, abstract and authors.
    Returns a list of Paper objects
    """
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
    """
    Return a new list based on the result of the given function f
    """
    return [t for t in token_list if f(t) is True]


def extract_unigram_tokens(paper_body, stopwords):
    """
    Tokenize a paper body, remove context independent stopwords,
    filter tokens with length <= 2 and normalize only the first
    token of a sentence.

    Return the  processed unigram tokens
    """
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
    """
    Find the top 200 bigrams in a list of tokens
    """
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    bigram_finder = nltk.collocations.BigramCollocationFinder.from_words(token_list)
    bigram_finder.apply_freq_filter(20)
    return bigram_finder.nbest(bigram_measures.pmi, 200)


def multiword_tokenizer(token_list, bigram_list):
    """
    Tokenize a list of unigram tokens into bigram tokens,
    given a list of bigrams.
    Bigrams are separated with "__"
    """
    mwetokenizer = MWETokenizer(bigram_list, separator="__")
    return mwetokenizer.tokenize(token_list)


def stem_tokens(token_list):
    """
    Stem every tokenn that is not a bigram - bigrams are identified 
    as tokens with "__" in them.
    In order to preserve the casing of the token, the following code based on a
    stack overflow answer was used.
    https://stackoverflow.com/questions/57917203/maintain-proper-nouns-and-capitalised-words-while-stemming
    """
    stemmer = PorterStemmer()
    stemmed_list = []
    for token in token_list:
        if "__" not in token:
            if token == token.title():
                stemmed_token = stemmer.stem(token).capitalize()
            elif token.isupper():
                stemmed_token = stemmer.stem(token).upper()
            else:
                stemmed_token = stemmer.stem(token)
            stemmed_list.append(stemmed_token)
        else:
            stemmed_list.append(token)

    return stemmed_list


def gen_doc_freq(paper_tokens, vocab):
    """
    Return a count of the number of documents ever term in the
    vocab exists in,
    in a dictionary in the form:
        {
            term_1: num_documents_it_occurs,
            ...
            term_n: num_documents_it_occurs
        }
    """
    df = defaultdict(int)
    for word in vocab:
        for token_list in paper_tokens.values():
            if word in token_list:
                df[word] += 1

    return df


def write_vocab_to_file(vocab):
    """
    Write every vocab word in a line to a file in the format:
    word:word_id
    """
    vocab_id_list = [
        "{0}:{1}".format(v, vocab_id[v]) for v in sorted(list(vocab_id.keys()))
    ]
    with open(CURR_DIR + "GROUP059_vocab.txt", "w", encoding="utf-16") as v:
        v.write("\n".join(vocab_id_list))


def write_term_counts(tokenized_bodies, vocab_id):
    """
    Calculate the term frequencies of every paper body,
    map the terms to the ID in the vocab,
    then write the output in the format:
    paper_id,term1:term1_freq, ..., termn:termn_freq
    """
    with open(CURR_DIR + "GROUP059_count_vectors.txt", "w", encoding="utf-16") as t:
        for paper_id, token_list in tokenized_bodies.items():
            fd = FreqDist(token_list)
            counts = ["{0}:{1}".format(vocab_id[t], v) for t, v in fd.items()]
            line = [paper_id] + counts
            t.write(",".join(line) + "\n")


if __name__ == "__main__":
    """
    CORPUS EXTRACTION:
    - Parse PDF for research papers to download.
    - Download the papers, convert to text.
    - Read the converted texts, parse the abstract, bodies, titles and authors 
      into Paper objects
    """
    # parse_download_convert_pdfs()
    papers = parse_papers()
    stopwords = load_stopwords()

    """
    SPARSE FEATURE GENERATION
    Tokenize paper bodies - tokens won't contain stopwords, len(token) > 2 and 
    only first token of a sentence is normalized
    """
    tokenized_bodies = dict(
        (paper.id, extract_unigram_tokens(paper.body, stopwords)) for paper in papers
    )

    # Find the top 200 bigrams in the entire corpus
    corpus_tokens = list(chain.from_iterable(tokenized_bodies.values()))
    vocab_bigrams_200 = get_top_200_bigrams(corpus_tokens)

    # Re-tokenize the paper body tokens so that bigrams are presented
    # as a single token separated with "__"
    tokenized_bodies = dict(
        (paper_id, multiword_tokenizer(tokens, vocab_bigrams_200))
        for paper_id, tokens in tokenized_bodies.items()
    )

    # Stem every token that is not a bigram
    tokenized_bodies = dict(
        (paper_id, stem_tokens(tokens)) 
        for paper_id, tokens in tokenized_bodies.items()
    )

    """
    Determine the vocab of the entire corpus, then generate the document 
    frequency  of every stemmed term
    """
    vocab = set(chain.from_iterable(tokenized_bodies.values()))
    df = gen_doc_freq(tokenized_bodies, vocab)
    with open(CURR_DIR + "df.json", "w", encoding="utf-16") as j:
        json.dump(df, j)

    # Filter all terms who appear in under 3% or over 95% of documents from
    # vocab
    vocab = set(filter_tokens(lambda t: df[t] >= 6 and df[t] <= 190, vocab))

    # Filter tokens from bodies that are not in vocab
    tokenized_bodies = dict(
        (paper_id, filter_tokens(lambda t: t in vocab, tokens))
        for paper_id, tokens in tokenized_bodies.items()
    )

    # Assign an id to every vocab word
    vocab_id = dict(zip(vocab, range(len(vocab))))

    write_vocab_to_file(vocab)
    write_term_counts(tokenized_bodies, vocab_id)
