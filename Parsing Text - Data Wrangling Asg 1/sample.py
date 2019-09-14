import pandas as pd
import re
import json

class Patent:
   __inventors_tag_p = re.compile(r'<inventors>[\s\S]*<\/inventors>')
   __applicant_cited_p = re.compile(r'<category>cited by applicant<\/category>')
   __inventor_tag_lazy_p = re.compile(r'<inventor .*>[\s\S]*?<\/inventor>')
   __inventor_first_name_p = re.compile(r'<first-name>.*<\/first-name>')
   __inventor_last_name_p = re.compile(r'<last-name>.*<\/last-name>')

   __claims_tag_p = re.compile(r"<claims.*>[\s\S]*<\/claims>")
   __every_claim_lazy_p = re.compile(r'<claim id.*>[\s\S]*?<\/claim>')
   __claim_text_tag_p = re.compile(r'<claim-text>[\s\S]*<\/claim-text>')
   __remove_newline_whitespace_p = re.compile(r"\n+\s*")

   __us_patent_grant_tag_p = re.compile(r"<us-patent-grant.*>")
   __docnum_filename_p = re.compile(r'file="[A-Z0-9]*')
   __file_and_dash_p = re.compile(r'file="')

   __invention_title_tag_p = re.compile(r'<invention-title\sid=".*">.*<\/invention-title>')
   __only_invention_title_tag_p = re.compile(r'(<invention-title\sid=".*">|<\/invention-title>)')

   __abstract_tag_p = re.compile(r'<abstract id="abstract">[\s\S]*<\/abstract>')
   __non_abstract_text = re.compile(r'(<abstract id="abstract">|<\/abstract>|<p.*">|<\/p>)')
   __num_claims_p = re.compile(r'<number-of-claims>\d*<\/number-of-claims>')
   __cited_by_examiner_p = re.compile(r"<category>cited by examiner<\/category>")

   __publish_and_application_reference_p = re.compile(r"(<(publication|application)-reference.*>[\s\S]*<\/(publication|application)-reference>)")
   __app_type_tag = re.compile(r'<application-reference appl-type="\w+">')
   __app_type_only = re.compile(r'"\w+"')
   __kind_tag = re.compile(r"<kind>\w+<\/kind>")

   __remove_tags_p = re.compile(r'(<[\s\w\W=\-"]*?>|<\/[-\w]+>)')
   __remove_tags_old = re.compile(r'(<[\s\w=\-"]*>|<\/[-\w]+>)')

   __patent_templ = "{0} Patent Grant ({1} published application) issued on or after January 2, 2001{2}"

   kind_generator = {
      "plant": (lambda kindcode: Patent.__patent_templ.format("Plant", "with a", "") if kindcode == "P3" else Patent.__patent_templ.format("Plant", "no", "")),
      "utility": (lambda kindcode: Patent.__patent_templ.format("Utility", "with a", ".") if kindcode == "B2" else Patent.__patent_templ.format("Utility", "no", ".")),
   }

   __codes = [{"find": re.compile(r"&#x2018;"), "replace":"\u2018"},
   {"find": re.compile(r"&#x2019;"), "replace":"\u2019"},
   {"find": re.compile(r"&#xe7;"), "replace":"\u00e7"}, 
   {"find": re.compile(r"&#xb0;"), "replace":"\u00b0"},
   {"find": re.compile(r"&#x2261;"), "replace":"\u2261"},
   {"find": re.compile(r"&#x2212;"), "replace":"\u2212"},
   {"find": re.compile(r"&#x3c;"), "replace":"\u003c"},
   {"find": re.compile(r"&#x394;"), "replace":"\u0394"},
   {"find": re.compile(r"&#x2003;"), "replace":"\u2003"},
   {"find": re.compile(r"&#x2032;"), "replace":"\u2032"},
   {"find": re.compile(r"&#x201d;"), "replace":"\u0201d"},
   {"find": re.compile(r"&#x201c;"), "replace":"\u0201c"},
   {"find": re.compile(r"&#x3b3;"), "replace":"\u03b3"},
   {"find": re.compile(r"&#x3b2;"), "replace":"\u03b2"},
   {"find": re.compile(r"&#x3b1;"), "replace":"\u03b1"},
   {"find": re.compile(r"&#x22c5;"), "replace":"\u22c5"},
   {"find": re.compile(r"&#x2062;"), "replace":"\u2062"},
   {"find": re.compile(r"&#x2014;"), "replace":"\u2014"},
   {"find": re.compile(r"&#xd7;"), "replace":"\u00d7"},
   {"find": re.compile(r"&#xee;"), "replace":"\u00ee"},
   {"find": re.compile(r"&#x2208;"), "replace":"\u2208"},
   {"find": re.compile(r"&#x2264;"), "replace":"\u2264"},
   {"find": re.compile(r"&#x2243;"), "replace":"\u2243"},
   {"find": re.compile(r"&#x2260;"), "replace":"\u2260"},
   {"find": re.compile(r"&#xbd;"), "replace":"\u00bd"},
   {"find": re.compile(r"&#x2192;"), "replace":"\u2192"},
   {"find": re.compile(r"&#x22ef;"), "replace":"\u22ef"},
   {"find": re.compile(r"&#x2026;"), "replace":"\u2026"},
   {"find": re.compile(r"&#x2115;"), "replace":"\u2115"},
   {"find": re.compile(r"&#x22ee;"), "replace":"\u22ee"},
   {"find": re.compile(r"&#x22f1;"), "replace":"\u22f1"},
   {"find": re.compile(r"&#x211d;"), "replace":"\u211d"},
   {"find": re.compile(r"&#x2102;"), "replace":"\u2102"},
   {"find": re.compile(r"&#x2211;"), "replace":"\u2211"},
   {"find": re.compile(r"&#x2061;"), "replace":"u\2061"},
   {"find": re.compile(r"&#x2a53;"), "replace":"u\2a53"},
   {"find": re.compile(r"&#x2200;"), "replace":"u\2200"},
   {"find": re.compile(r"&#x3c4;"), "replace":"u\03c4"},
   {"find": re.compile(r"&#x175;"), "replace":"u\0175"},
   {"find": re.compile(r"&#xe1;"), "replace":"u\00e1"},
   {"find": re.compile(r"&#x2dc;"), "replace":"u\02dc"},
   {"find": re.compile(r"&#x212b;"), "replace":"u\212b"},
   {"find": re.compile(r"&#x3bc;"), "replace":"u\03bc"},
   {"find": re.compile(r"&#xfd;"), "replace":"u\00fd"},
   {"find": re.compile(r"&#xfa;"), "replace":"u\00fa"},
   {"find": re.compile(r"&#xe9;"), "replace":"u\00e9"},
   {"find": re.compile(r"&#x26;"), "replace":"u\0026"},
   {"find": re.compile(r"&#xfc;"), "replace":"u\00fc"},
   {"find": re.compile(r"&#xf6;"), "replace":"u\00f6"},
   {"find": re.compile(r"&#x3e;"), "replace":"u\003e"},
   {"find": re.compile(r"&#x3b8;"), "replace":"u\03b8"},
   {"find": re.compile(r"&#x3b7;"), "replace":"u\03b7"},
   {"find": re.compile(r"&#xb7;"), "replace":"u\00b7"},
   {"find": re.compile(r"&#xef;"), "replace":"u\00ef"},
   {"find": re.compile(r"&#x3c3;"), "replace":"u\03c3"},
   {"find": re.compile(r"&#x221a;"), "replace":"u\221a"},
   ]

   ordered_attr_list = ["grant_id","patent_title","kind","number_of_claims","inventors",
   "citations_applicant_count","citations_examiner_count","claims_text","abstract"]

   def __init__(self, raw_xml):
      self.grant_id = self.__extract_grant_id(raw_xml)
      self.patent_title = self.__extract_patent_title(raw_xml)
      self.kind = self.__extract_kind(raw_xml)      
      self.number_of_claims = self.__extract_number_of_claims(raw_xml)
      self.inventors = self.__extract_inventors(raw_xml)
      self.citations_applicant_count = self.__extract_citations_app_count(raw_xml)
      self.citations_examiner_count = self.__extract_citations_examiner_count(raw_xml)
      self.claims_text = self.__extract_claims_text(raw_xml)
      self.abstract = self.__extract_abstract(raw_xml)
      self.ordered_val_list = [self.grant_id, self.patent_title, self.kind, self.number_of_claims, self.inventors, self.citations_applicant_count, self.citations_examiner_count, self.claims_text, self.abstract]


   def to_json_format(self):
      values = []
      for pair in zip(Patent.ordered_attr_list, self.ordered_val_list):
         if pair[0] != "grant_id":
            if isinstance(pair[1], int):
               field_value = '"{0}":{1}'.format(pair[0], pair[1])
            else:
               field_value = '"{0}":"{1}"'.format(pair[0], pair[1])

            values.append(field_value)

      jsonObj = {getattr(self, "grant_id"): "{" + ",".join(values) + "}"}
      return jsonObj
      


   def __extract_grant_id(self, raw_xml): 
      patent_grant_tag = re.search(Patent.__us_patent_grant_tag_p, raw_xml).group()
      docnum_filename  = re.search(Patent.__docnum_filename_p, patent_grant_tag).group()
      g_id = re.sub(Patent.__file_and_dash_p, "", docnum_filename)
      
      return g_id


   def __extract_patent_title(self, raw_xml):
      invention_title_tag = re.search(Patent.__invention_title_tag_p, raw_xml).group()
      title = re.sub(Patent.__only_invention_title_tag_p, "", invention_title_tag)
      return Patent.html_hex_to_unicode(title)


   def __extract_abstract(self, raw_xml):
      abstract_tag = re.search(Patent.__abstract_tag_p, raw_xml)

      if abstract_tag == None:
         return "NA"
      else:
         abstract = Patent.remove_tags(abstract_tag.group())         
         return Patent.html_hex_to_unicode(abstract)


   def __extract_kind(self, raw_xml):
      p_a_tags = re.findall(Patent.__publish_and_application_reference_p, raw_xml)
      app_tag = re.findall(Patent.__app_type_tag, p_a_tags[0][0])      
      app_type = re.findall(Patent.__app_type_only, app_tag[0])

      kind_patent = app_type[0].strip('"')

      __kind_tag = re.search(Patent.__kind_tag, p_a_tags[0][0]).group()
      kind_code = Patent.remove_tags(__kind_tag).strip()

      if kind_patent in Patent.kind_generator:
         return Patent.kind_generator[kind_patent](kind_code)
      else:
         return "%s Patent"%(kind_patent[0].upper() + kind_patent[1:])


   def __extract_number_of_claims(self, raw_xml):
      num_claims_tag = re.search(Patent.__num_claims_p, raw_xml).group()
      num_claims = Patent.remove_tags(num_claims_tag)

      return int(Patent.html_hex_to_unicode(num_claims))


   def __extract_inventors(self, raw_xml):
      inventors_tag = re.search(Patent.__inventors_tag_p, raw_xml).group()
      inventors = re.findall(Patent.__inventor_tag_lazy_p, inventors_tag)

      name_template = "{0} {1}"
      inventor_names = []

      for inventor in inventors:
         first_name_tag = re.search(Patent.__inventor_first_name_p, inventor).group()
         last_name_tag = re.search(Patent.__inventor_last_name_p, inventor).group()
         first_name = Patent.html_hex_to_unicode(Patent.remove_tags(first_name_tag))
         last_name = Patent.html_hex_to_unicode(Patent.remove_tags(last_name_tag))
         inventor_names.append(name_template.format(first_name, last_name))

      return "[%s]"%(','.join(inventor_names))


   def __extract_citations_app_count(self, raw_xml):
      applicant_citations = re.findall(Patent.__applicant_cited_p, raw_xml)
      return len(applicant_citations)


   def __extract_citations_examiner_count(self, raw_xml):      
      examiner_citations = re.findall(Patent.__cited_by_examiner_p, raw_xml)
      return len(examiner_citations)


   def __extract_claims_text(self, raw_xml):
      claims_tag = re.search(Patent.__claims_tag_p, raw_xml).group()
      claims = re.findall(Patent.__every_claim_lazy_p, claims_tag)
      
      claims_text = []
      for claim in claims:
         claim_txt_dirty = re.search(Patent.__claim_text_tag_p, claim).group()
         claim_txt = Patent.html_hex_to_unicode(Patent.remove_tags(claim_txt_dirty))
         claim_txt = re.sub(Patent.__remove_newline_whitespace_p, "", claim_txt)
         claims_text.append(claim_txt)

      return "[{0}]".format(','.join(claims_text))

   @staticmethod
   def html_hex_to_unicode(string):
      for code_map in Patent.__codes:
         string = re.sub(code_map["find"], code_map["replace"], string)

      return string.strip()

   
   @staticmethod
   def remove_tags(string):
      return re.sub(Patent.__remove_tags_p, "", string)


def extract_patents(contents):
   xmlpattern = re.compile(r"<us-patent-grant[\s\S]*?</us-patent-grant>")
   docs = re.findall(xmlpattern, contents)
   patents = []

   i = 0
   for xml_doc in docs:
      p = Patent(xml_doc)
      patents.append(p)

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


def convert_to_json_string(dic):
   patents = []
   for p in zip(dic.keys(), dic.values()):
      patents.append('"{0}":{1}'.format(p[0], p[1]))
      
   return "{" + ",".join(patents) + "}"


def comp(str1, str2):
   lens1 = len(str1)
   lens2 = len(str2)

   if lens1 != lens2:
      print("Both strings are not an equal length")
   
   i = 0
   while i < lens1:
      
      if str1[i] != str2[i]:
         print("First non-match: [%s] to [%s]" %(str1[i], str2[i]))
         with open("D:\\Workspace\\postgraduate-projects\\data-wrangling-asg1\\debug.txt", "w", encoding='utf-8') as xml_file:
            xml_file.write("{0}\n{1}\n\n".format(str1[i], str2[i]))
            xml_file.write(str1  + "\n\n\n===str2===\n\n")
            xml_file.write(str2)

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


if __name__ == "__main__":
   #xml_file = open("D:\\Workspace\\postgraduate-projects\\data-wrangling-asg1\\Sample_input.xml", "r")
   xml_file = open("D:\\Workspace\\postgraduate-projects\\data-wrangling-asg1\\Group059.txt", "r")
   sample_input = xml_file.read()
   xml_file.close()
   """
   json_file =  open('D:\\Workspace\\postgraduate-projects\\data-wrangling-asg1\\sample_output.json', encoding='utf-8')
   sample_output = json.load(json_file)
   json_file.close()
   """
   
   patents = extract_patents(sample_input)
   with open("D:\\Workspace\\postgraduate-projects\\data-wrangling-asg1\\new2.json", "w", encoding="utf-8") as fp:
      a = pd.DataFrame([p.ordered_val_list for p in patents])
      a.columns = Patent.ordered_attr_list
      a.to_csv("new2.csv", sep=',', encoding='utf-8', index=False)
      j = {}
      for p in patents:
        j.update(p.to_json_format())
      fp.write(convert_to_json_string(j))
      fp.close()
   
   with open("new2.csv", "r", encoding="utf-8") as q:
      content = q.read()
      content = re.sub("\s{2,}", " ", content);
      with open("cleaned.csv", "w", encoding="utf-8") as tf:
         tf.write(content)
   
   with open("new2.json", "r", encoding="utf-8") as wj:
         jc = wj.read()
         jc = re.sub("\s{2,}", " ", jc);
         with open("cleaned.json", "w", encoding="utf-8") as wf:
            wf.write(jc)
   

   """ 
   test_grant_id(patents, sample_output)
   test_field(patents, sample_output, 'patent_title')
   test_field(patents, sample_output, 'abstract')
   test_field(patents, sample_output, 'number_of_claims')
   test_field(patents, sample_output, 'citations_examiner_count')
   test_field(patents, sample_output, 'kind')
   test_field(patents, sample_output, 'citations_applicant_count')
   test_field(patents, sample_output, 'inventors')   
   test_field(patents, sample_output, 'claims_text')
   """
   
