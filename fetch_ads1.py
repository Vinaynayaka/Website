import requests


TOKEN = 'G7CKzmhX9ZmQdgRhWwcPXLjggHDV2ebXA7Lxw0KK'

headers = {'Authorization' : f'Bearer {TOKEN}'}
params = {
    'q' : 'author:"mooley"',
    'fl' : 'author,title,abstract,pubdate',
    'rows' : 2,
    'sort' : 'pubdate desc'
}

response = requests.get('https://api.adsabs.harvard.edu/v1/search/query', headers=headers, params=params)

data=response.json()
# print(data)


papers= data['response']['docs']

with open('new_website.html','w',encoding="utf-8") as x :
    x.write("<html>")
    x.write("<head><title>WEBPAGE</title></head>")
    x.write("<body>")
    x.write("<h1>PUBLICATIONS</h1>")
    for paper in papers :
        x.write(f"<h2>{paper['title'][0]}</h2>")
        x.write(f"<p>Authors:{','.join(paper['author'])}</p>")
        x.write(f"<p>Published:{paper['pubdate']}</p>")
        x.write(f"<p>Abstract: {paper.get('abstract', 'No abstract available')}</p>")
    x.write("</body></html>")