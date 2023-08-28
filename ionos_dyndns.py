import requests
import utils.env_var as env
import utils.common_functions as fn
from os import path
from models.dyndns import dyndns
from argparse import ArgumentParser, SUPPRESS

class ionosdyndns(dyndns):

    def __init__(self):
        super().__init__()
        self.public_key = env.public_key
        self.secret_key = env.secret_key

    def updateheaders(self):
        api_key = '{}.{}'.format(self.public_key, self.secret_key)
        extra_headers = {
            'X-API-Key':api_key
            }
        self.createheaders(extra_headers=extra_headers)
    
    def updatedata(self, hosting:str, domains:list[str], description:str):
        self.createbody(hosting=hosting, domains=domains, description=description)

    def request(self, timeout=10):
        print('Sending request to ionos api.')
        return requests.post(url = self.dyn_dns_url, json = self.body, headers = self.headers, timeout=timeout)

def main(domain_id:str, domains:list[str]):
    dynamic_dns = ionosdyndns()
    dynamic_dns.updateheaders()
    description = 'Request to enable dynamic dns and update ip for the given domains.'
    dynamic_dns.updatedata(hosting='ionos', domains=domains, description=description)
    response = dynamic_dns.request()
    if response.status_code == 200:
        message = 'Url use to updated ip for {} domain id in dns server retrieved succesfully, response will be exported to responses folder.'.format(domain_id)
        print(message)
        file = 'responses/ionos_response.json'
        try:
            fn.exportresponse(file, domain_id, response)
            print('Response file generated succesfuly.')
        except FileExistsError:
            print('Response file already exist, updating values.')
            fn.updateresponse(file, domain_id, response)
            print('Values on response file has been updated successfully')
    else:
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
    argparser.add_argument('--domain-id', type=str, required=False, help=help_domain_id)
    argparser.add_argument('--domains', type=list[str], nargs='+', required=False, help=help_domains)
    argparser.add_argument('--multi-request', type=bool, choices=[True], default=False, help=help_multi_request)
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
    argparser=argparserins()
    argparservars(argparser)
    args = vars(argparser.parse_args())
    for key in args:
        locals()[key] = args[key]
    if domain_id and domains:
        main(domain_id=domain_id, domains=domains)
        argparser.exit(status=0)
    elif domain_id and not domains:
        argparser.error('--domains argument needed if --domain-id is present.')
    elif multi_request:
        print('Running script in multi request mode, existing domain-ids in ionos_responses.json file will be ignore (keep existing url).')
        file = 'resources/ionos_multirequest.json'
        multirequest_dict = fn.readfile(file)
        file2 = 'responses/ionos_response.json'
        if path.exists(file2):
            file_validator = fn.readfile(file2)
            for key in multirequest_dict.keys():
                if multirequest_dict[key] in file_validator['domains']:
                    pass
                main(domain_id=key, domains=multirequest_dict[key])
        else:
            for key in multirequest_dict.keys():
                main(domain_id=key, domains=multirequest_dict[key])
        argparser.exit(status=0, message='Multi-request finished - logger to implement in a future.')
    else:
        print('No parameters given, use --help to display available parameters')