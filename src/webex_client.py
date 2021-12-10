import os
import requests
import sys

class WebexClient:
    def __init__(self, config_provider):
        print('Init Webex')
        self.__config = config_provider
        # Auth token for bot stored inside os environment variables for security reasons
        self.__bot_token = os.environ['webex_bot_token']
        # While initializing the WebexClient we check existence of our room before doing any work. If the room doesn't exist we print out the error and exit the program.
        room_list = self.__get_room_list()
        self.__room_id = self.__get_room_id(room_list, self.__config.get_property('room_name'))

        if self.__room_id == None:
            print('Room does not exist')
            sys.exit(-1)

    def __get_room_list(self) -> dict:
        try:
            url = "https://webexapis.com/v1/rooms/"

            api_headers = {}
            api_headers['Authorization'] = f'Bearer {self.__bot_token}'
            api_headers['Accept'] = 'application/json'

            response = requests.get(url, headers=api_headers, verify=True)
            if response.status_code != 200:
                print(f'Non 200 status code - {response.status_code}')
                sys.exit(1)

            print(f'Webexapix - Rooms: Status code: {response.status_code}')
            return response.json()

        except Exception as err:
            print("Problem big TIME: " + str(err))
            sys.exit(3)

    def __get_room_id(self, room_list:dict, room_name: str) -> str:
        """From the provided room_list we iterate throught the 'items' object to find our room by name and return it's ID. If room is not found then None is returned"""
        for rooms in room_list['items']:
            if rooms['title'] == room_name:
                return rooms['id']

        return None

    def send_report_to_room(self, report_data: []):
        """Method to format the report data into a markdown report. Webex doesn't support markdown tables so each domain and it's risk_score is in the h2. For format refer to report.md"""
        message_body = {}
        message_body['roomId'] = self.__room_id
        message_markdown = "# Umbrella DNS Report"

        for report_entry in report_data:
            message_markdown += f'\n## {report_entry["domain"]} - __{report_entry["risk_score"]}__\n- Registrar name: {report_entry["registrar_name"]}\n- Name servers: {report_entry["name_servers"]}\n- Registrant name: {report_entry["registrant_name"]}'

        message_body['markdown'] = message_markdown

        try:
            url = "https://webexapis.com/v1/messages/"

            api_headers = {}
            api_headers['Authorization'] = f'Bearer {self.__bot_token}'
            api_headers['Accept'] = 'application/json'
            response = requests.post(url, headers=api_headers, verify=True, data=message_body)
            if response.status_code != 200:
                print(f'Non 200 status code - {response.status_code}')
                sys.exit(1)

            print(f'Status code: {response.status_code}')
            return response.json()

        except Exception as err:
            print("Problem big TIME: " + str(err))
            sys.exit(3)
