### owner : chuezzang (mchiwoo@naver.com)
### date : dec.05, 2018

import urllib.request
import urllib.parse
import urllib.error
import json
import sqlite3
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'http://api.plos.org/search?q=title:DNA'
#Taking response and request from url

connection = urllib.request.urlopen(url, context=ctx)
data = connection.read().decode()

js = json.loads(data)
#js_dumps = json.dumps(js, indent=2)

json_response = js['response']
json_docs = js['response']['docs']

# json_response = json.dumps(json_response, indent = 2)
# json_docs = json.dumps(json_docs, indent = 2)

conn = sqlite3.connect('docs_db.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS docs')
cur.execute('''CREATE TABLE IF NOT EXISTS docs
             (id text, journal text, eissn text, 
             publication_date text, article_type text, author_display text, 
             abstract text, title_display text, score real)''')

for doc_data in json_docs:  # parsing the data
        doc_list = { #filter the data
            "id": doc_data.get('id'),
            "journal": doc_data.get('journal'),
            "eissn": doc_data.get('eissn'),
            "publication_date": doc_data.get('publication_date'),
            "article_type": doc_data.get('article_type'),
            "author_display": doc_data.get('author_display'),
            "abstract": doc_data.get('abstract'),
            "title_display": doc_data.get('title_display'),
            "score": doc_data.get('score'),
        }

    #    cur.execute('''INSERT INTO docs  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', doc_list)

        cur.execute('''INSERT INTO docs (id, journal, eissn, publication_date, article_type,
            author_display, abstract, title_display, score) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                    (doc_list['id'], doc_list['journal'], doc_list['eissn'], doc_list['publication_date'], doc_list['article_type'], ",".join(doc_list['author_display']), ",".join(doc_list['abstract']), doc_list['title_display'], doc_list['score']))

conn.commit()
cur.execute("select * from docs")

print(cur.fetchall())

