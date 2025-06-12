import requests

TOKEN = 'G7CKzmhX9ZmQdgRhWwcPXLjggHDV2ebXA7Lxw0KK'

headers = {'Authorization': f'Bearer {TOKEN}'}

params = {
    'q' : 'author : "Mooley" ',
    'fl' : 'author,title,pubdate,abstract,bibcode,volume,page,pub',
    'rows' : 200,
    'sort' : 'pubdate desc'
}

response = requests.get('https://api.adsabs.harvard.edu/v1/search/query', headers=headers, params=params)


data=response.json()



try: 
    papers = data['response']['docs']
except KeyError:
    print("Error: Could not find 'response' in API result.")
    print(data)
    exit()

with open('template.html', mode='r',encoding='utf-8') as x:
    html_template=x.read()

def short_form_pub(pub):
    if pub == "The Astrophysical Journal Supplement Series" :
        return 'ApJSS'
    elif pub == "Monthly Notices of the Royal Astronomical Society" :
        return 'MNRAS'
    elif pub== "The Astrophysical Journal" :
        return 'ApJ'
    else :
        return pub

def filter_journal(journal):
    words_to_check = [
    "coordinates",
    "dataset",
    "vizier",
    "meeting",
    "proposal",
    "award",
    "telegram"
    ]
    journal = journal.lower()
    for word in words_to_check:
        if word in journal :
            return True
    return False

edit_html=""
i=0
for paper in papers:
    journal=paper['pub']
    if filter_journal(journal) == False:
        i=i+1
        edit_html += "<div class ='paper'>"
        first_author = paper['author'][0]
        pub_year = paper['pubdate']
        pub_year = pub_year[:4]
        edit_html += f"<p> { i }{')'} {first_author}  et al {pub_year} , {paper['title'][0]} </p>"
        paper_page = paper.get('page', ['NA'])
        paper_page = paper_page[0]
        paper_pub = short_form_pub(paper['pub'])
        edit_html += f"<p> <a href='https://ui.adsabs.harvard.edu/abs/{paper['bibcode']}' >{paper_pub} {','} {paper.get('volume', 'NA')} {','} {paper_page}</a></p>"
        edit_html += "</div>"

new_html=html_template.replace("<!-- PLACEHOLDER_FOR_PUBLICATIONS -->", edit_html)

with open(file="index.html", mode='w', encoding='utf-8') as a:
    a.write(new_html)

print("values written in the index.html")
