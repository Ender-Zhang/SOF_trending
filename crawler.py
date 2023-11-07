import requests

url = "https://api.stackexchange.com/2.3/questions?order=desc&sort=creation&site=stackoverflow&fromdate=1698883200&todate=1698969600&page=1&pagesize=20"  # pagesize changed to 2

payload = {}
headers = {
    'Cookie': 'prov=b36537f7-1afc-48d6-9500-5046f726ae1b'
}

response = requests.request("GET", url, headers=headers, data=payload)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()

    # Check if there are at least two items
    if len(data['items']) >= 2:
        # Loop through the first two items
        for index, item in enumerate(data['items'], start=1):
            link = item['link']
            page_response = requests.get(link)

            # Ensure the request for the page was successful
            if page_response.status_code == 200:
                filename = f'data/html/webpage_c{index}.html'  # Dynamic filename for each link
                # Write the content to the file
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(page_response.text)
                print(f'Saved {link} as {filename}')
            else:
                print(f'Failed to retrieve content from {link}')
else:
    print('Failed to retrieve data from Stack Exchange API')
