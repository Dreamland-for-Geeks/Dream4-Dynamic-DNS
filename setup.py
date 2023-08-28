from setuptools import find_packages, setup

setup(
    name='dyndns - Dynamic DNS',
    version='0.0.1',
    description='',
    author='Luis Arce',
    author_email='contacto@dreamlandforgeeks.com',
    url='',
    data_files=[
        ('.config', ['.config/.env']),
        ('resources', ['resources/ionos_multirequest.json']),
        ('responses', ['responses/.gitkeep'])
    ],
    py_modules=[
        'models.dyndns',
        'utils.common_functions',
        'utils.env_var',
        'ionos_dyndns',
        'godaddy_dyndns',
        'cronjobs.update_ip_dns'
        ],
    packages=find_packages(
        ['requests', 'python-dotenv']
    ),
    install_requires=[
        'python-dotenv',
        'request'
        ]
)