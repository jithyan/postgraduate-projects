import pandas as pd
import re
import json

class Patent:
   inventors_tag_p = re.compile('<inventors>[\s\S]*<\/inventors>')
   applicant_cited_p = re.compile('<category>cited by applicant<\/category>')
   inventor_tag_lazy_p = re.compile('<inventor .*>[\s\S]*?<\/inventor>')
   inventor_first_name_p = re.compile('<first-name>.*<\/first-name>')
   inventor_last_name_p = re.compile('<last-name>.*<\/last-name>')

   claims_tag_p = re.compile("<claims.*>[\s\S]*<\/claims>")
   every_claim_lazy_p = re.compile('<claim id.*>[\s\S]*?<\/claim>')
   claim_text_tag_p = re.compile('<claim-text>[\s\S]*<\/claim-text>')

   __us_patent_grant_tag_p = re.compile("<us-patent-grant.*>")
   __docnum_filename_p = re.compile('file="[A-Z0-9]*')
   __file_and_dash_p = re.compile('file="')

   __invention_title_tag_p = re.compile('<invention-title\sid=".*">.*<\/invention-title>')
   __only_invention_title_tag_p = re.compile('(<invention-title\sid=".*">|<\/invention-title>)')

   __abstract_tag_p = re.compile(r'<abstract id="abstract">[\s\S]*<\/abstract>')
   __non_abstract_text = re.compile(r'(<abstract id="abstract">|<\/abstract>|<p.*">|<\/p>)')
   __remove_tags_p = re.compile(r'(<[\s\w=\-"]*>|<\/[-\w]+>)')
   __num_claims_p = re.compile(r'<number-of-claims>\d*<\/number-of-claims>')
   __cited_by_examiner_p = re.compile(r"<category>cited by examiner<\/category>")

   publish_and_application_reference_p = re.compile("(<(publication|application)-reference.*>[\s\S]*<\/(publication|application)-reference>)")
   app_type_tag = re.compile('<application-reference appl-type="\w+">')
   app_type_only = re.compile(r'"\w+"')
   kind_tag = re.compile("<kind>\w+<\/kind>")

   __patent_templ = "{0} Patent Grant ({1} published application) issued on or after January 2, 2001{2}"
   gen_kind = {
      "plant": (lambda kindcode: Patent.__patent_templ.format("Plant", "with a", "") if kindcode == "P3" else Patent.__patent_templ.format("Plant", "no", "")),
      "utility": (lambda kindcode: Patent.__patent_templ.format("Utility", "with a", ".") if kindcode == "B2" else Patent.__patent_templ.format("Utility", "no", ".")),
   }

   __codes = [{"find": re.compile("&#x2018;"), "replace":"\u2018"},
   {"find": re.compile("&#x2019;"), "replace":"\u2019"}]

   ordered_attr_list = ["grant_id","patent_title","kind","number_of_claims","inventors","citations_applicant_count","citations_examiner_count","claims_text","abstract"]

   def __init__(self, raw_xml):
      self.raw = raw_xml
      self.grant_id = self.__extract_grant_id()
      self.patent_title = self.extract_patent_title()
      self.kind = self.extract_kind()      
      self.number_of_claims = self.extract_number_of_claims()
      self.inventors = self.extract_inventors()
      self.citations_applicant_count = self.extract_citations_app_count()
      self.citations_examiner_count = self.extract_citations_examiner_count()
      self.claims_text = self.extract_claims_text()
      self.abstract = self.extract_abstract()
      self.ordered_val_list = [self.grant_id, self.patent_title, self.kind, self.number_of_claims, self.inventors, self.citations_applicant_count, self.citations_examiner_count, self.claims_text, self.abstract]

   
   def toJsonString(self):
      innerObj = {}
      for attr in ordered_attr_list:
         if attr != "grant_id":
            innerObj[attr] = getattr(self,attr)
      
      jsonObj = {getattr(self, "grant_id"): innerObj}

      return str(jsonObj)
      
   
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
      return self.cleanup(title)

   def extract_abstract(self):
      enable_log = True
      abstract_tag = re.findall(Patent.__abstract_tag_p, self.raw)

      if len(abstract_tag) == 0:
         return "NA"
      else:
         debug(abstract_tag, Patent.__abstract_tag_p, enable_log)
         abstract = re.sub(Patent.__remove_tags_p, "", abstract_tag[0])         
         return self.cleanup(abstract)

   def extract_kind(self):
      enable_log = True
      p_a_tags = re.findall(Patent.publish_and_application_reference_p, self.raw)
      debug(p_a_tags, Patent.publish_and_application_reference_p, enable_log)

      app_tag = re.findall(Patent.app_type_tag, p_a_tags[0][0])      
      debug(app_tag, Patent.app_type_tag, enable_log)
      
      app_type = re.findall(Patent.app_type_only, app_tag[0])
      debug(app_type, Patent.app_type_only, enable_log)

      kind_patent = app_type[0].strip('"')

      kind_tag = re.findall(Patent.kind_tag, p_a_tags[0][0])
      kind_code = re.sub(Patent.__remove_tags_p, "", kind_tag[0]).strip()

      if kind_patent in Patent.gen_kind:
         return Patent.gen_kind[kind_patent](kind_code)
      else:
         return "%s Patent"%(kind_patent[0].upper() + kind_patent[1:])

   def extract_number_of_claims(self):
      num_claims_tag = re.findall(Patent.__num_claims_p, self.raw)
      num_claims = re.sub(Patent.__remove_tags_p, "", num_claims_tag[0])
      return int(self.cleanup(num_claims))

   def extract_inventors(self):
      inventors_tag = re.findall(Patent.inventors_tag_p, self.raw)
      inventors = re.findall(Patent.inventor_tag_lazy_p, inventors_tag[0])
      name_template = "{0} {1}"

      inventor_names = []

      for inventor in inventors:
         first_name = re.match(Patent.inventor_first_name_p, inventor)
         last_name = re.match(Patent.inventor_last_name_p, inventor)
         inventor_names.append(name_template.format(first_name, last_name))
      

      return "[%s]"%(','.join(inventor_names))

   def extract_citations_app_count(self):
      applicant_citations = re.findall(Patent.applicant_cited_p, self.raw)
      return len(applicant_citations)


   def extract_citations_examiner_count(self):      
      examiner_citations = re.findall(Patent.__cited_by_examiner_p, self.raw)
      return len(examiner_citations)


   def extract_claims_text(self):
      claims_tag = re.findall(Patent.claims_tag_p, self.raw)
      #has to be findall below
      claims = re.findall(Patent.every_claim_lazy_p, claims_tag[0])
      claims_text = []

      for claim in claims:
         claim_txt = re.findall(Patent.claim_text_tag_p, self.raw)
         claims_text.append(self.cleanup(claim_txt[0]))
      
      return "[{0}]".format(','.join(claims_text))

   def cleanup(self, string):
      i = 0
      while i < len(Patent.__codes):
         string = re.sub(Patent.__codes[i]["find"], Patent.__codes[i]["replace"], string)
         i += 1
      return string.rstrip().lstrip()

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
            #comp(patent_field, sample_field)
            print("Field %s :(%s) does not match one in sample (%s) [%s]" %(field_name, patent_field, sample_field, patent.grant_id))
   
   if num_grants == len(patents) and num_correct == num_grants:
      print("PASS: Correctly identified all '%s' in sample" %(field_name))
   else:
      print("FAILED '%s' test with %d failures" %(field_name, num_grants - num_correct))

def comp(str1, str2):
   lens1 = len(str1)
   lens2 = len(str2)

   if lens1 != lens2:
      print("Both strings are not an equal length")
   
   i = 0
   while i < lens1:
      
      if str1[i] != str2[i]:
         print("First non-match: [%s] to [%s]" %(str1[i], str2[i]))
         return
      i+=1
   
   print("Both strings are equal")

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

   json_file =  open('D:\\Workspace\\postgraduate-projects\\data-wrangling-asg1\\sample_output.json', encoding='utf-8')
   sample_output = json.load(json_file)
   json_file.close()

   patents = main(sample_input)
   test_grant_id(patents, sample_output)
   test_field(patents, sample_output, 'patent_title')
   test_field(patents, sample_output, 'abstract')
   test_field(patents, sample_output, 'number_of_claims')
   test_field(patents, sample_output, 'citations_examiner_count')
   test_field(patents, sample_output, 'kind')
   test_field(patents, sample_output, 'citations_applicant_count')
   #test_field(patents, sample_output, 'inventors')   
   #test_field(patents, sample_output, 'claims_text')
