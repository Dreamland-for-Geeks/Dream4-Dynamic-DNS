import requests
from utils.common_functions import readfile

def main():
    file = '..responses/ionos_response.json'
    current_dict = readfile(file)
    for key in current_dict['updateUrl'].keys():
        message = 'Updating public ip for {} domain id'.format(key)
        print(message)
        url = current_dict['updateUrl'][key]
        request = requests.get(url=url)
        if request.status_code == 200:
            message = 'Public ip for {} domain name has been updated successfully'.format(key)
            print(message)

if __name__ == '__main__':
    main()