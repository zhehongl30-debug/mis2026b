import requests
from bs4 import BeautifulSoup
url = "https://mis2026b-iota.vercel.app/me"
Data = requests.get(url)
#print(Data.text)
sp = BeautifulSoup(Data.text, "html.parser")
result=sp.select("td source")
for item in result:
	print(item.get("src"))
