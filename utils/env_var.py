import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.config/.env')

dyn_dns_url = os.getenv('DYN_DNS_URL')
public_key = os.getenv('PUBLIC_KEY')
secret_key = os.getenv('SECRET_KEY')
shopper_id = os.getenv('SHOPPER_ID')