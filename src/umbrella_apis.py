import requests
import os
import sys


class UmbrellaApis:
    def __init__(self, config_provider):
        print('Init Umbrella')
        self.__config = config_provider
        self.__api_report_token = self.__get_token()

    def __get_token(self) -> str:
        """Method to get autorization token from auth api"""
        url = "https://management.api.umbrella.com/auth/v2/oauth2/token"
        key = self.__config.get_property('key')
        secret = os.environ['auth_secret']
        headers = {'Accept': 'application/json'}

        token_request = requests.post(
            url, headers=headers, auth=requests.auth.HTTPBasicAuth(key, secret))

        token = token_request.json().get('access_token')

        if token == None:
            print("Auth_token not found. Exiting...")
            sys.exit()
        else:
            return(token)

    def get_report(self, categories: list = None) -> dict:
        """Method to fetch data from reports api on umbrella."""
        try:
            if categories == None:
                # If category is not passed from the outside we query all the data from the API
                url = "https://reports.api.umbrella.com/v2/organizations/7943805/activity/dns?from=-7days&to=now&limit=5000"
            else:
                # For API we need the category IDs delimited by a comma. For this reason we simply add them to a string and remove the last character, which is the last comma.
                categories_string = ''
                for category in categories:
                    categories_string += f'{category},'

                l = len(categories_string)
                query_categories = categories_string[:l-1]

                url = f"https://reports.api.umbrella.com/v2/organizations/7943805/activity/dns?from=-7days&to=now&limit=5000&categories={query_categories}"

            api_headers = {}
            # We need to add the Bearer auth token into the headers dictionary here
            api_headers['Authorization'] = f'Bearer {self.__api_report_token}'
            api_headers['Accept'] = 'application/json'

            response = requests.get(url, headers=api_headers, verify=True)
            # If we get different response then HTTP200 we shut the program down and print the error from the API
            if response.status_code != 200:
                print(f'Non 200 status code - {response.status_code}')
                print(response.json())
                sys.exit(1)

            print(f'Status code: {response.status_code}')
            return response.json()

        except Exception as err:
            print("Problem big TIME: " + str(err))
            sys.exit()

    def process_dns_queries(self, report_data: dict, risk_categories: list) -> dict:
        """We have to parse domain, category and internal IP"""
        data_objects = report_data['data']
        return_dict = {}
        return_dict['domain_info'] = []

        # Iterate through the dictionary of domains and check if the analyzed dns query fits our risk category
        for dns_log in data_objects:
            categories_string = ''
            for categories in dns_log['categories']:
                if self.__is_id_on_list(categories['id'], risk_categories):
                    categories_string += f'\tId: {str(categories["id"])} Name {str(categories["label"])}'

            log_dict = {'domain': f'{dns_log["domain"]}',
                        'internal_ip': f'{dns_log["internalip"]}',
                        'categories': f'{categories_string}'}
            return_dict['domain_info'].append(log_dict)

        return return_dict

    def __is_id_on_list(self, id: int, list_to_search: list) -> bool:
        """Simple method to iterate through the list and find a matching ID. Here it is used to find if dns query fits our category"""
        for id_on_list in list_to_search:
            if id_on_list == id:
                return True

        return False

    def get_investigate_data(self, domain: str) -> dict:
        """Get data from Investigate API. Returns dict with risk_score value and information about domain servers and registrar_name"""
        return_dict = {}
        return_dict['domain'] = domain
        try:
            # Secrets are saved in the OS environment variables for security reasons
            api_token = os.environ['investigate_token']
            url = f'https://investigate.api.umbrella.com/domains/risk-score/{domain}'

            api_headers = {}
            api_headers['Authorization'] = f'Bearer {api_token}'
            api_headers['Accept'] = 'application/json'

            response = requests.get(url, headers=api_headers, verify=True)
            if response.status_code != 200:
                print(f'Non 200 status code - {response.status_code}')
                print(response.json())
                sys.exit(1)

            # Here we add the risk_score for the domain into out return_dict
            return_dict['risk_score'] = response.json()['risk_score']

        except Exception as err:
            print("Problem while getting risk score: " + str(err))
            sys.exit()

        try:
            # Secrets are saved in the OS environment variables for security reasons
            api_token = os.environ['investigate-token']
            url = f'https://investigate.api.umbrella.com/whois/{domain}'

            api_headers = {}
            api_headers['Authorization'] = f'Bearer {api_token}'
            api_headers['Accept'] = 'application/json'

            response = requests.get(url, headers=api_headers, verify=True)
            if response.status_code != 200:
                print(f'Non 200 status code - {response.status_code}')
                print(response.json())
                sys.exit(1)

            # Here we add the needed parameters from the WHOIS query
            return_dict['registrar_name'] = response.json()['registrarName']
            return_dict['name_servers'] = response.json()['nameServers']
            return_dict['registrant_name'] = response.json()['registrantName']

        except Exception as err:
            print("Problem while whois data: " + str(err))
            sys.exit()

        return return_dict
