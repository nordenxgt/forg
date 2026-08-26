import json
import bs4
import requests

url = "https://fileinfo.com/filetypes/common"

try:
    response = requests.get(url)
    response.raise_for_status()
except requests.RequestException as e:
    print(e)
    raise

soup = bs4.BeautifulSoup(response.text, "html.parser")

heading_elements = soup.select("h2")
extension_elements = soup.select(".extcol")

headings = tuple(heading.get_text().removesuffix(" Files") for heading in heading_elements)

current_group, extension_groups = [], []

for extension_element in extension_elements:
    extension_text = extension_element.get_text()
    if extension_text == "Extension":
        if current_group:
            extension_groups.append(tuple(current_group))
            current_group = []
    else:
        current_group.append(extension_text)
if current_group:
    extension_groups.append(tuple(current_group))

extension_dict = dict(zip(headings, extension_groups))
with open("extensions.json", "w", encoding="utf-8") as f:
    json.dump(extension_dict, f, indent=2)
    print("Scraping successfull")
