import requests

url = "https://seaofthieves.fandom.com/wiki/Megalodon"
search_text = "There is currently no text in this page. You can search for this page title in other pages, or search the related logs, but you do not have permission to create this page."

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

response = requests.get(url, headers=headers)

#response = requests.get(url)
if response.status_code == 200:
    page_content = response.text

    if search_text in page_content:
        print("The text is present on the page.")
    else:
        print("The text is not present on the page.")
else:
    print("Failed to fetch the page content.")
