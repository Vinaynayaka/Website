import requests

TOKEN = 'G7CKzmhX9ZmQdgRhWwcPXLjggHDV2ebXA7Lxw0KK'

headers = {'Authorization': f'Bearer {TOKEN}'}

params = {
    'q' : 'author : "Mooley" ',
    'fl' : 'author,title,pubdate,abstract,bibcode',
    # 'rows' : 10,
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

with open('index.html', mode='r',encoding='utf-8') as x:
    html_template=x.read()

edit_html=""
for paper in papers:
    edit_html += "<div class='paper'>"
    edit_html += f"<h2><a href='https://ui.adsabs.harvard.edu/abs/{paper['bibcode']}' target='_blank'>{paper['title'][0]}</a></h2>"
    edit_html += f"<p><strong>Authors:</strong> {', '.join(paper['author'])}</p>"
    edit_html += f"<p><strong>Published:</strong> {paper['pubdate']}</p>"
    edit_html += f"<p><strong>Abstract:</strong> {paper.get('abstract', 'No abstract available.')}</p>"
    edit_html += "</div><hr>"

new_html=html_template.replace("<!-- PLACEHOLDER_FOR_PUBLICATIONS -->", edit_html)

with open(file="index.html", mode='w', encoding='utf-8') as a:
    a.write(new_html)

print("values written in the html")