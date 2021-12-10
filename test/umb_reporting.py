import os
import sys
import requests
import urllib3

global key
global secret
global token



urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def GetToken():
    key = "e53ebc3ea3ba4c2f8fab27821052b4df"
    secret = "763bf817e2aa4f909299f1272f76326e"
    global token
    try:
        url = "https://management.api.umbrella.com/auth/v2/oauth2/token"
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url, headers=headers, auth=requests.auth.HTTPBasicAuth(key, secret), verify=False)
        token = r.json().get('access_token')
        # print("\nAuthentication SUCCESSFUL !!! \nAuth_Token: {}\n".format(token))
        if token == None:
            print("Auth_token not found. Exiting...")
            sys.exit()
        else:
            return(token)
        
    except Exception as err:
        print("Auth token error : " + str(err))
        sys.exit()


def GetReport():
    # token = GetToken()
    try:
        url = "https://reports.api.umbrella.com/v2/organizations/7943805/activity/dns?from=-2days&to=now&limit=10"
        headers = {'Authorization':'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjIwMTktMDEtMDEiLCJ0eXAiOiJKV1QifQ.eyJleHAiOjE2Mzg4MTIxNTIsImlhdCI6MTYzODgwODU1MiwiaXNzIjoidW1icmVsbGEtYXV0aHovYXV0aHN2YyIsIm5iZiI6MTYzODgwODU1Miwic3ViIjoib3JnLzc5NDM4MDUvdXNlci8xMTg1Mjk1OSIsInNjb3BlIjoicm9sZTpyb290LWFkbWluIiwiYXV0aHpfZG9uZSI6ZmFsc2V9.JuxAyrbjabffZZ7TIYmgf7Guy8w6_ReTaXJQaLejqZ2IPqDA-SfiZ2yeZHbJsXk64GK6raGCMf59RzNBj9BtN2_gwRpLH5x8Fkl6rmGb0yITTOtlrdp773ZnypPgYiG-6TIot93pSilbLobQHcewMLZspI-nwZoqDKppYJAGQBr0UZf52EY1oDpl9a5iPWi31GSzXeZ1rnZCmCvqqoWYKrc3eVv9mEIUcEsTkZx85vUKvgDPG5adrVtgM96Zf1GtX9nQN0e1gfV-zVvCyVEfoEDDZVgkIm-IyegPuSO9yDUqkfWecXndjupgtZpE_TxxMokikwo9dOZyo46ZGQipVA', 'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers, verify=False)
        print(response.text.encode('utf8'))

    except Exception as err:
        print("Problem big TIME : " + str(err))
        sys.exit()

# def Initial():
#     risk_score = input("Please input a risk score treshold [default value 50]: ")
#     domain_treshold = input("Please input a threshold of interests [default value 5 block per domain]: ")
#     time_range = "-1days"

# def GetSecCategory():
#     pass

if __name__ == '__main__':
    # Initial()
    # GetToken()
    # token = GetToken()
    # print(token)
    GetReport()


# url = "https://reports.api.umbrella.com/v2/organizations/7943805/activity/dns"
# 
# payload = None
# 
# headers = {
#     "Accept": "application/json",
#     "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjIwMTktMDEtMDEiLCJ0eXAiOiJKV1QifQ.eyJleHAiOjE2Mzg3NTIxODksImlhdCI6MTYzODc0ODU4OSwiaXNzIjoidW1icmVsbGEtYXV0aHovYXV0aHN2YyIsIm5iZiI6MTYzODc0ODU4OSwic3ViIjoib3JnLzc5NDM4MDUvdXNlci8xMTg1Mjk1OSIsInNjb3BlIjoicm9sZTpyb290LWFkbWluIiwiYXV0aHpfZG9uZSI6ZmFsc2V9.TJacBNLwp35c-NNexe0kiZc5HpW77ZI_t6As0wlmvwtCKuW5_IFHYp7IlfleZpGjqtLYiezgSzxO7SukvSro4UeEiE-yQNHaUHMcj6xUomaDlljX6ZYfEEgtODl1B6YYHTf5eEyhGwYNpOKE5XDUl8ZGnm3yv9sNcx_wNay-Wx5arwRJhh1M17rR7AFOxTch9WcFXy_F9QKg8FOQ__WCdu-8RZz--ftdLT5Kn9oDB3WFrTtScvIP79PVq4oyiBq1f_HF-LDWKTjyyuIM6A0sRBFRXhwUeykoIlBl5qqyBBLkOQsDZRfXXKGyyYS4iMdnTDDyOmjaCpIR18SzxmCWew"
# }
# 
# response = requests.request('GET', url, headers=headers, data = payload)
# 
# print(response.text.encode('utf8'))


