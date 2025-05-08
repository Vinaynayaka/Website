import requests

TOKEN = 'G7CKzmhX9ZmQdgRhWwcPXLjggHDV2ebXA7Lxw0KK'

headers = {'Authorization': f'Bearer {TOKEN}'}

params = {
    'q' : 'author : "Mooley" ',
    # 'fl' : '*',
    'fl' : 'author,title,pubdate,abstract,bibcode,volume,page,pub',
    'rows' : 100,
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
        return 'APJSS'
    elif pub == "Monthly Notices of the Royal Astronomical Society" :
        return 'MNRAS'
    elif pub== "The Astrophysical Journal" :
        return 'APJ'
    else :
        return pub

edit_html=""
i=0
for paper in papers:
    i=i+1
    edit_html += "<div class='paper'>"
    edit_html += f"<h2><a href='https://ui.adsabs.harvard.edu/abs/{paper['bibcode']}' target='_blank'>{ i }{')'} {paper['title'][0]}</a></h2>"
    first_author = paper['author'][0]
    other_authors = ', '.join(paper['author'][1:])
    edit_html += f"<p><strong>Author:</strong> {first_author} <span class='more-authors' style='display:none;'>, {other_authors}</span> <a href='#' onclick='this.previousElementSibling.style.display=\"inline\"; this.style.display=\"none\"; return false;'>[+more]</a></p>"
    pub_date = paper['pubdate']
    pub_date = pub_date[:7]
    edit_html += f"<p><strong>Published:</strong> {pub_date}</p>"
    abstract = paper.get('abstract', 'No abstract available.')
    if abstract != 'No abstract available.':
        short_abstract = abstract[:200] + "..." if len(abstract) > 200 else abstract
        edit_html += f"<p><strong>Abstract:</strong> {short_abstract} <a href='https://ui.adsabs.harvard.edu/abs/{paper['bibcode']}' target='_blank'>[Read more]</a></p>"
    paper_page = paper.get('page', ['  '])
    paper_page = paper_page[0]
    paper_pub = short_form_pub(paper['pub'])
    edit_html += f"<p><strong>{paper_pub} {'-'} {paper.get('volume', '  ')} {'-'} {paper_page}</strong></p>"
    edit_html += "</div><hr>"

new_html=html_template.replace("<!-- PLACEHOLDER_FOR_PUBLICATIONS -->", edit_html)

with open(file="index.html", mode='w', encoding='utf-8') as a:
    a.write(new_html)

print("values written in the index.html")



