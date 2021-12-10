import sys
import requests
import urllib3

def main():

    print('Start')
    # api_token = get_token()
    api_token = 'd605c1cc-36d1-4eef-b7b5-b0e9853b89b8'
    domain = 'pornhub.com'
    get_report(api_token, domain)



def get_report(api_token: str, domain: int = None) -> dict:

    try:
        if domain == None:
            # pokud neni kategorie tak to nefiltruji, pokud je tak filtruji v else
            url = "https://reports.api.umbrella.com/v2/organizations/7943805/activity/dns?from=-7days&to=now&limit=1000"
        else:
            url = f"https://investigate.api.umbrella.com/domains/categorization/{domain}?showlabels"

        api_headers = {}
        api_headers['Authorization'] = f'Bearer {api_token}'
        api_headers['Accept'] = 'application/json'

        response = requests.get(url, headers=api_headers, verify=True)
        if response.status_code != 200:
            print(f'Non 200 status code - {response.status_code}')
            sys.exit(1)

        print(f'Status code: {response.status_code}')
        return response.json()

    except Exception as err:
        print("Problem big TIME: " + str(err))
        sys.exit()

if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    main()
 