import requests
import utils.env_var as env

class dyndns:
    
    headers:dict
    body:dict

    def __init__(self):
        self.dyn_dns_url = env.dyn_dns_url

    def createheaders(self, accept:str = 'application/json', content_type:str = 'application/json', extra_headers:dict=None):
        print('Creating headers')
        self.headers = {
            'accept': accept,
            'Content-Type': content_type,
            }
        self.headers.update(extra_headers)
    
    def createbody(self, hosting:str, domains:list[str], description:str, godaddy_response:dict=None):
        print('Creating payload')
        if hosting == 'ionos':
            self.body = {
                'domains': domains,
                "description": description
                }
        elif hosting == 'godaddy':
            godaddy_response.pop('name')
            godaddy_response.pop('type')
            self.body = godaddy_response
    