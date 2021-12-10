from umbrella_apis import UmbrellaApis
from webex_client import WebexClient
from config_provider import ConfigProvider

def main():
    """Main method of the program all of the high-level logic is here"""
    config = ConfigProvider()
    risk_categories = config.get_property('risk_categories')

    umbrella = UmbrellaApis(config)
    webex = WebexClient(config)

    report_data = umbrella.get_report(risk_categories)
    dns_information = umbrella.process_dns_queries(
        report_data, risk_categories)
    report_data = []
    for domain in dns_information['domain_info']:
        report_data.append(
            umbrella.get_investigate_data(domain['domain']))

    webex.send_report_to_room(report_data)


if __name__ == '__main__':
    main()
