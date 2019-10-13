from urllib.request import urlopen
from bs4 import BeautifulSoup
import textdistance
import re
import pandas as pd
from heapq import heappop, heappush, heapify

from collections import namedtuple

SchoolRanking = namedtuple("SchoolRanking", "name rank")
SchoolIntermediate = namedtuple(
    "SchoolIntermediate", "name type lga_id lga_name lat lon"
)
School = namedtuple("School", "name type lga_id lga_name lat lon rank")


def extract_primary_school_rankings():
    html = urlopen("http://www.schoolcatchment.com.au/?p=12301")
    soup = BeautifulSoup(html, "lxml")
    rows = soup.find_all("tr")

    i = 0
    primary_school_rankings = []
    for row in rows[1:]:
        name = row.contents[2].text
        rank = int(row.contents[1].text)
        heappush(primary_school_rankings, (name, i, SchoolRanking(name, rank)))
        i += 1
    return primary_school_rankings


def extract_secondary_school_rankings():
    html = ""
    with open(
        r"D:\Workspace\postgraduate-projects\Data Integration\secondary_school_ranking.html",
        "r",
    ) as html_file:
        html = html_file.read()
    soup = BeautifulSoup(html, "lxml")
    all_ul = soup.find_all("ul")
    school_info = all_ul[2].find_all("li")

    secondary_school_rankings = []
    i = 0
    for school in school_info:
        info = school.find_all("div")
        name = info[0].text
        ranking = int(info[1].text)
        heappush(secondary_school_rankings, (name, i, SchoolRanking(name, ranking)))
        i += 1

    return secondary_school_rankings


def extract_schools():
    xml = ""
    with open(
        r"D:\Workspace\postgraduate-projects\Data Integration\schools.xml", "r"
    ) as schools_file:
        xml = schools_file.read()
    soup = BeautifulSoup(xml, "lxml")
    raw_schools = soup.find_all("school")

    i = 0
    schools = []
    for school in raw_schools:
        name = school.school_name.text
        type = school.school_type.text
        lga_id = school.lga_id.text
        lga_name = school.lga_name.text
        lat = school.y.text
        lon = school.x.text
        heappush(schools, (name, i, SchoolIntermediate(name, type, lga_id, lga_name, lat, lon)))
        i += 1
    return schools


secondary_school_rankings = extract_secondary_school_rankings()
primary_school_rankings = extract_primary_school_rankings()
schools = extract_schools()


def match_text(t1, t2):
    t1_normalized = re.sub(r"'", "", t1.upper())
    t2_normalized = re.sub(r"'", "", t2.upper())
    nw = textdistance.DamerauLevenshtein()
    return nw.normalized_distance(t1_normalized, t2_normalized)


buckets = {
    "Primary": primary_school_rankings,
    "Secondary": secondary_school_rankings
}
matched = []
review = []
threshold = 0.2
i = 0
l = len(schools)
while schools:
    school = heappop(schools)
    #i += 1

    school_type = school[2].type
    if school_type in buckets:
        updated_list = []
        while buckets[school_type]:
            i+=1
            s2 = heappop(buckets[school_type])
            dist = match_text(s2[0], school[0])
            if dist == 0.0:
                matched.append(School(school[2].name, school[2].type, school[2].lga_id, school[2].lga_name, school[2].lat, school[2].lon, s2[2].rank))
                break
            elif dist < threshold:
                review.append((school[2], s2[2]))
            updated_list.append(s2)
        updated_list.extend(buckets[school_type])
        heapify(updated_list)
        buckets[school_type] = updated_list
        print(len(buckets[school_type]))
