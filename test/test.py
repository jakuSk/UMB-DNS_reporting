import requests

url = "https://reports.api.umbrella.com/v2/organizations/7943805/activity/dns"

payload = None

headers = {
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjIwMTktMDEtMDEiLCJ0eXAiOiJKV1QifQ.eyJleHAiOjE2Mzg3NjQyMDcsImlhdCI6MTYzODc2MDYwNywiaXNzIjoidW1icmVsbGEtYXV0aHovYXV0aHN2YyIsIm5iZiI6MTYzODc2MDYwNywic3ViIjoib3JnLzc5NDM4MDUvdXNlci8xMTg1Mjk1OSIsInNjb3BlIjoicm9sZTpyb290LWFkbWluIiwiYXV0aHpfZG9uZSI6ZmFsc2V9",
    "Accept": "application/json"
}

response = requests.request('GET', url, headers=headers, data = payload)

print(response.text.encode('utf8'))





payload = None

headers = {
    "Accept": "application/json",
    "x-traffic-type": null
}

response = requests.request('GET', url, headers=headers, data = payload)

print(response.text.encode('utf8'))