import pandas as pd
import re
import json

class Patent:      
   __us_patent_grant_tag_p = re.compile("<us-patent-grant.*>")
   __docnum_filename_p = re.compile('file="[A-Z0-9]*')
   __file_and_dash_p = re.compile('file="')
   __invention_title_tag_p = re.compile('<invention-title\sid=".*">.*<\/invention-title>')
   __only_invention_title_tag_p = re.compile('(<invention-title\sid=".*">|<\/invention-title>)')
   __abstract_tag_p = re.compile('<abstract id="abstract">[\s\S]*<\/abstract>')

   def __init__(self, raw_xml):
      self.raw = raw_xml
      self.grant_id = self.__extract_grant_id()
      self.patent_title = self.extract_patent_title()
      self.kind = self.extract_kind()      
      self.number_of_claims = self.extract_number_of_claims()
      self.inventors = self.extract_inventors()
      self.citations_app_count = self.extract_citations_app_count()
      self.citations_examiner_count = self.extract_citations_examiner_count()
      self.claims_text = self.extract_claims_text()
      self.abstract = self.extract_abstract()
   
   def __extract_grant_id(self):
      enable_log = True   
      patent_grant_tag = re.findall(Patent.__us_patent_grant_tag_p, self.raw)
      debug(patent_grant_tag, Patent.__us_patent_grant_tag_p, enable_log)      
      docnum_filename  = re.findall(Patent.__docnum_filename_p, patent_grant_tag[0])
      debug(docnum_filename, Patent.__docnum_filename_p, enable_log)
      
      gid = re.sub(Patent.__file_and_dash_p, "", docnum_filename[0])
      
      return gid

   def extract_patent_title(self):
      enable_log = True
      invention_title_tag = re.findall(Patent.__invention_title_tag_p, self.raw)
      debug(invention_title_tag, Patent.__invention_title_tag_p, enable_log)

      title = re.sub(Patent.__only_invention_title_tag_p, "", invention_title_tag[0])
      title_1 = re.sub("(&#x2018;)", "\u2018", title)
      return re.sub("(&#x2019;)", "\u2019", title_1)

   def extract_abstract(self):

      return "None"

   def extract_kind(self):
      return "None"

   def extract_number_of_claims(self):
      return "None"

   def extract_inventors(self):
      return "None"

   def extract_citations_app_count(self):
      return "None"

   def extract_citations_examiner_count(self):
      return "None"

   def extract_claims_text(self):
      return "None"


def main(sample):
   xmlpattern = re.compile(r"<us-patent-grant[\s\S]*?</us-patent-grant>")
   docs = re.findall(xmlpattern, sample)
   patents = []

   i = 0
   while i < len(docs):
      p = Patent(docs[i])
      patents.append(p)
      i += 1

   return patents

def test_field(patents, sample, field_name): 
   num_grants = len(sample.keys())
   num_correct = 0

   for patent in patents:
      if patent.grant_id not in sample:
         print("FAIL: grant id (%s) not in sample output" %(patent.grant_id))
      else:
         sample_field = sample[patent.grant_id][field_name]
         patent_field = getattr(patent,field_name)
         if sample_field == patent_field:
            num_correct += 1
         else:
            print("Field %s :(%s) does not match one in sample (%s) [%s]" %(field_name, patent_field, sample_field, patent.grant_id))
   
   if num_grants == len(patents) and num_correct == num_grants:
      print("PASS: Correctly identified all '%s' in sample" %(field_name))
   else:
      print("FAILED '%s' test with %d failures" %(field_name, num_grants - num_correct))


def test_grant_id(patents, sample):   
   num_grants = len(sample.keys())
   correct_ids = 0

   for patent in patents:
      if patent.grant_id not in sample:
         print("FAIL: grant id (%s) not in sample output" %(patent.grant_id))
      else:
         correct_ids += 1
   
   if num_grants == len(patents) and correct_ids == num_grants:
      print("PASS: Identified all grant ids in sample")
   else:
      print("FAILED grant_id test with %d failures" %(num_grants - correct_ids))

def debug(matches, pattern, enabled):
   if enabled == False:
      return

   match_len = len(matches)
   if match_len != 1:
      print("Number of matches (%s) for pattern (%s)" %(match_len, pattern))

if __name__ == "__main__":
   xml_file = open("D:\\Workspace\\postgraduate-projects\\data-wrangling-asg1\\Sample_input.xml", "r")
   sample_input = xml_file.read()
   xml_file.close()

   json_file =  open('D:\\Workspace\\postgraduate-projects\\data-wrangling-asg1\\sample_output.json')
   sample_output = json.load(json_file)
   json_file.close()

   patents = main(sample_input)
   test_grant_id(patents, sample_output)
   test_field(patents, sample_output, 'patent_title')
   #test_field(patents, sample_output, 'abstract')

