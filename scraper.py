import scraperwiki
import string
import unicodedata
import time
import xml

import pip

package_name='selenium'
pip.main(['install', package_name])

from bs4 import BeautifulSoup
pip install beautifulsoup4

headers = ["Name","Department","Total Ratings","Overall Quality","Easiness","Hot"]
#Dictionary of school ids (keys) that map to tuple of school name and number of pages
colleges = {"137":("Brown",24), "278":("Columbia",36), "298":("Cornell",104), "1339":("Dartmouth",12), "399":("Harvard",24), "1275":("UPennsylvania",30), "780":("Princeton",16), "1222":("Yale",23)}

for sid in colleges.keys():
    college,pages = colleges[sid]
    print college
    for i in xrange(1,pages+1):
        response = scraperwiki.scrape("http://www.ratemyprofessors.com/SelectTeacher.jsp?sid=%s&pageNo=%s" % (sid,str(i)))
        time.sleep(5)
        soup = BeautifulSoup(response)
        rows = soup.find_all("div",{"class":"entry odd vertical-center"})
        rows.extend(soup.find_all("div",{"class":"entry even vertical-center"}))
        for row in rows:
            columns = row.find_all('div')
            columns = columns[3:]
            variables = {}
            for i,col in enumerate(columns):
                value = unicodedata.normalize('NFKD', col.text).encode('ascii', 'ignore')
                variables[headers[i]] = value
            variables["College"] = college
            scraperwiki.sqlite.save(unique_keys=['Name',"Department"], data = variables)
