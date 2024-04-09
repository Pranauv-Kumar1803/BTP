from typing import Tuple
import typer
from typing_extensions import Annotated
import os
import json
import time
import subprocess
from pprint import pprint
from zapv2 import ZAPv2

zap_api_key = 'lkssshb47bkq8d04gm4p8gabj9'

def start_zap_daemon():
    # for windows
    if os.name == 'nt':
        os.chdir("E:/Zed Attack Proxy")
        subprocess.run(f'zap.bat -daemon', shell=True)
    # for Linux based systems
    else: 
        subprocess.Popen(['gnome-terminal', '--', 'bash', '-c',
                          '{} -daemon &'.format(zap_path)])

def zap_scan(target, api_key):
    zap = ZAPv2(apikey=api_key, proxies={
                'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'})

    print('Passive Scanning target {}'.format(target))
    zap.ascan.scan(target, scanpolicyname="Default Policy")
    while int(zap.ascan.status()) < 100:
        print('Active Scan progress %: {}'.format(zap.ascan.status()))
        time.sleep(5)
    print('Active Scan completed')

    print('Alerts: ')
    for alert in zap.core.alerts(baseurl=target):
        print(alert)

def generate_zap_report(api_key):
    zap = ZAPv2(apikey=api_key, proxies={
                'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'})

    json_report = zap.core.jsonreport()
    fileName = time.time()
    with open(f'{fileName}_zap.json', 'w') as fp:
        fp.write(json_report)
        print("ZAP scan report saved as json file")

def main(dns: Annotated[str, typer.Option(help="This option is used for doing a DNS recon on a given domain name.\n Use this option followed by a domain name to get details of DNS records associated with that domain")] = "", zap: Annotated[str, typer.Option(help="This option is used for doing a ZAP Spider Active Scan on a given target.\n Use this option followed by a domain name to do an active scan on the domain")] = "" ):
    domain = dns
    z = zap
    if dns:
        fileName = time.time()
        os.system('echo Starting dnsrecon....... ')
        os.system(f'dnsrecon -d {domain} -j {fileName}.json')

        with open(f'{fileName}.json', 'r') as file:
            data = file.read()
            json_data = json.loads(data)

        l=[]
        for j in json_data:
            if j['type'] == 'A':
                l += [j['address']]

        print('The IP addresses of the domain name given are: ', l)
        os.system('echo "dnsrecon finsished successfully!" ')

    if z:
        print(z)
        os.system('echo Starting ZAP Daemon and scanning the target...... ')
        start_zap_daemon()
        zap_scan(z, zap_api_key)
        generate_zap_report(zap_api_key)
    
if __name__ == "__main__":
    typer.run(main)
    