import requests

url = "https://seaofthieves.fandom.com/robots.txt"

response = requests.get(url)
if response.status_code == 200:
    robots_txt = response.text
    print(robots_txt)
else:
    print("Failed to fetch robots.txt")
