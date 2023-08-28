import json
import requests
import utils.env_var as env
from models.dyndns import dyndns
from argparse import ArgumentParser, SUPPRESS

class godaddydyndns(dyndns):

    def __init__(self):
        super().__init__()
        self.public_key = env.public_key
        self.secret_key = env.secret_key

    def updateheaders(self, is_reseller:bool=False):
        if is_reseller and env.shopper_id:
            shopper_id = env.shopper_id
            extra_headers = {
                'X-Shopper-Id': shopper_id
                }
        else:
            api_key = 'sso-key {}:{}'.format(self.public_key, self.secret_key)
            extra_headers = {
                'Authorization': api_key
                }
        self.createheaders(extra_headers=extra_headers)
    
    def updatedata(self, hosting:str, godaddy_response:dict):
        self.createbody(hosting=hosting, godaddy_response=godaddy_response)
    
    def request(self, method, name, domain:str, type:str='A', timeout=10):
        print('Sending request to ionos api.')
        url = self.dyn_dns_url.format(domain, type, name)
        if method == 'GET':
            return requests.request(method = method, url = url, headers = self.headers, timeout=timeout)
        elif method == 'PUT':
            return requests.request(method = method, url = url, json = self.body, headers = self.headers, timeout=timeout)

def main(name, domain:str, type:str='A'):
    dynamic_dns = godaddydyndns()
    dynamic_dns.updateheaders()
    current_record = dynamic_dns.request('GET', name, domain, type)
    if current_record.status_code == 200:
        json_response = json.loads(response.content.decode())
        dynamic_dns.updatedata(hosting='godaddy', godaddy_response=json_response)
        response = dynamic_dns.request('PUT', name, domain, type)
        if response.status_code == 200:
            print('DNS record updated successfully.')
    elif current_record.status_code == 404:
        print('Resource not found.')
        print('status code: ' + str(response.status_code))
        print(response.content)

def helpers():
    help_domain_id = '''(Sub)domain identifier, string use to separate and identify responses/values in the ionos_response.json file. 
    This argument is optional. Example: --domain-id firstresponse | --domain-id secondresponse | --domain-id mysubdomain'''
    help_domains = '''List of (sub)domain(s) separeted by a white space, example: www.mydomain.com mydomain.com.
    Domain, example mydomain.com, can be replaced by a @ symbol. This argument is required if --domain-id is present. '''
    help_multi_request = '''
Argument used to process multiple (sub)domain(s) that share same domain name, 
they share bulk_id so you can generated different updateUrls for each and 
update them at convenience, example:
{
    "domainid1": [@, subdomain, subdomain...],
    "domainid2": [subdomain, subdomain, subdomain...],
    "domainid3": [domain, subdomain, subdomain...]
}
'''
    return help_domain_id, help_domains, help_multi_request

def argparservars(argparser:ArgumentParser):
    (help_domain_id,
    help_domains,
    help_multi_request) = helpers()
    argparser.add_argument('--domain', type=str, required=True, help=help_domain_id)
    argparser.add_argument('--type', type=str, required=True, help=help_domains)
    argparser.add_argument('--name', type=str, required=True, help=help_multi_request)
    argparser.add_argument('--version', action='version', version='IP updater - Dynamic DNS v0.0.1')

def argparserins():
    return ArgumentParser(
        usage=SUPPRESS,
        prog='dyndns - Dynamic DNS for ionos',
        description='''This script enables dynamic dns using ionos api for a especific 
        (sub)domain(s) and generates url needed to update the public ip in ionos dns server.
        If subdomain doesn't exist, ionos will create it for you.''',
        epilog='Need more help?'
    )

if __name__ == '__main__':
    type:str
    argparser=argparserins()
    argparservars(argparser)
    args = vars(argparser.parse_args())
    for key in args:
        locals()[key] = args[key]
    print(type)
    main(name=name, domain=domain, type=type)
    argparser.exit(status=0)