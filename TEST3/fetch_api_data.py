import requests

TOKEN = 'IvMJqfQFon1K0gRy18ZaeMD5dTUJlBvw1gllqqNd'

headers = {'Authorization': f'Bearer {TOKEN}'}

params = {
    'q': 'author : "Mooley" ',
    'fl': 'author,title,pubdate,abstract,bibcode,volume,page,pub',
    'rows': 280,  # Highest value should be 280
    'sort': 'pubdate desc'
}

response = requests.get('https://api.adsabs.harvard.edu/v1/search/query', headers=headers, params=params)

data = response.json()

try:
    papers = data['response']['docs']
except KeyError:
    print("Error: Could not find 'response' in API result.")
    print(data)
    exit()

with open('template.html', mode='r', encoding='utf-8') as x:
    html_template = x.read()

def short_form_pub(pub):
    if pub == "The Astrophysical Journal Supplement Series":
        return 'ApJSS'
    elif pub == "Monthly Notices of the Royal Astronomical Society":
        return 'MNRAS'
    elif pub == "The Astrophysical Journal":
        return 'ApJ'
    elif pub == "Astronomische Nachrichten":
        return 'Astronomische Nachrichten'
    elif pub == "Science":
        return 'Science'
    elif pub == "Frontiers in Astronomy and Space Sciences":
        return 'Frontiers in Astronomy and Space Sciences'
    elif pub == "Nature":
        return 'Nature'
    elif pub == "arXiv e-prints":
        return 'arXiv e-prints'
    elif pub == "Publications of the Astronomical Society of the Pacific":
        return 'Publications of the Astronomical Society of the Pacific'
    else:
        return pub

def filter_journal(journal):
    words_to_check = [
    "coordinates",
    "dataset",
    "vizier",
    "meeting",
    "proposal",
    "award",
    "telegram",
    "conference",
    "software",
    "aas",
    "cospar"
    ]
    journal = journal.lower()
    for word in words_to_check:
        if word in journal:
            return True
    return False

edit_html = "<section><ol class='publications-list'>" 
i = 0

for paper in papers:
    journal = paper['pub']
    if not filter_journal(journal):
        i += 1
        first_author = paper['author'][0]
        pub_year = paper['pubdate'][:4]
        title = paper['title'][0]
        paper_page = paper.get('page', ['NA'])[0]
        paper_pub = short_form_pub(journal)
        volume = paper.get('volume', 'NA')
        bibcode = paper['bibcode']

        # Construct the HTML for each publication as an <li> containing an <article>
        edit_html += "<li><article>"
        edit_html += f"<p>{first_author} et al {pub_year}, <strong>{title}</strong></p>"
        edit_html += f"<p><a href='https://ui.adsabs.harvard.edu/abs/{bibcode}'>{paper_pub}, {volume}, {paper_page}</a></p>"
        edit_html += "</article></li>"

edit_html += "</ol></section>" # Close the ordered list and section

# CHANGE THIS LINE:
new_html = html_template.replace("This is the palce", edit_html)

with open(file="index.html", mode='w', encoding='utf-8') as a:
    a.write(new_html)

print("Values written to index.html")