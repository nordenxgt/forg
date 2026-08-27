import json
import bs4
import requests
import sys

URL = "https://fileinfo.com/filetypes/common"

def main():
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(exc)
        sys.exit(2)

    soup = bs4.BeautifulSoup(response.text, "html.parser")
    heading_elements = soup.select("h2")
    extension_elements = soup.select(".extcol")
    headings = tuple(heading.get_text().removesuffix(" Files") for heading in heading_elements)

    i, data = 0, {}
    for extension_element in extension_elements[1:]:
        extension = extension_element.get_text().lower()
        if extension == "extension":
            i += 1
        else: 
            data[extension] = headings[i]

    with open("extensions.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        print("Scraping successfull")

if __name__ == "__main__":
    main()
