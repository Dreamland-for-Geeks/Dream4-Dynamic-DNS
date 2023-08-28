import json

def readfile(file):
    current_dict:dict
    with open(file=file, mode='r') as outfile:
        current_dict = json.loads(outfile.read())
        outfile.close()
    return current_dict

def exportresponse(file, domain_prefix, response):
    with open(file=file, mode='x') as outfile:
                json_dict = json.loads(response.content.decode())              
                json_dict['bulkId'] = {
                    domain_prefix: json_dict['bulkId']
                }       
                json_dict['updateUrl'] = {
                    domain_prefix:json_dict['updateUrl']
                }
                json_string = str(json_dict).replace("'", '"')
                outfile.write(json_string)
                outfile.close

def updateresponse(file, domain_prefix, response):
    current_dict = readfile(file)
    with open(file=file, mode='w+') as outfile:
        json_dict = json.loads(response.content.decode())
        domain_prefix = domain_prefix
        current_dict['bulkId'][domain_prefix] = json_dict['bulkId']
        current_dict['updateUrl'][domain_prefix] = json_dict['updateUrl']
        current_dict['domains'].extend(json_dict['domains'])
        json_string = str(current_dict).replace("'", '"')
        outfile.write(json_string)
        outfile.close()