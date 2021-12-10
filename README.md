# Umbrella DNS reporting by Jakub Škoda

## Usage

### Requirements

Only python 3.0 or newer is required

### Launch

```bash
python app.py
```

or

```bash
python3 app.py
```

### For periodic report can be set into crontab (linux only)

```bash
sudo -u report_user crontab -e

0 9 * * * bash '/srv/app/prod/umbrella_report/lib/app.py'
```

## Configuration

### config.json

``` json
{
    "risk_categories": [
        74,
        75,
        76,
        77
    ],
    "key": "XXX",
    "room_name": "Umbrella reporting"
}
```

#### Properties

- __risk_categories__ defines a list of categories we want to analyze closer. If empty or missing all DNS queries are fetched from the API
  - Note: also when not defined only latest 10000 dns queries are fetched from the API
- __key__ is obtained from Cisco umbrella alongside secret and is used to get authorization token from auth API.
- __room_name__ defines the name of the webex room where the final report is posted

### Environment variables

Secrets are stored inside environment variables. It is expected to be run under application with limited acces. It can be accessed easily like ```os.environ['auth_secret']``` where the string value is returned.

#### Variables

- __auth_secret__ is obtained from Cisco umbrella alongside secret and is used to get authorization token from auth API.
- __investigate_toen__ is obtained from Cisco umbrella and is used to get information from investigate API
- __webex_bot_token__ is obtained when creating the bot in Cisco Webex and is used to authorize the bot actions - Get rooms names/ids, send messages

#### How to set env variables

##### Linux/Unix

```bash
export env_name=value
```

##### Windows

```powershell
Powershell: $env:env_name = 'value'

cmd: setx env_name "value"
```

## TO DO

Add token handling [Tip here](https://github.com/CiscoDevNet/cloud-security/blob/master/Umbrella/client-samples/python/README.md)

## Investigate

<https://github.com/chrivand/UmbrellaPythonSamples/blob/master/UmbrellaInvestigateGetRequest.py>
<https://github.com/opendns/investigate-examples/blob/master/scripts.py>
