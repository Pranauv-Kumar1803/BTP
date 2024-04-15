from typing import Tuple
import typer
from typing_extensions import Annotated
import os
import json
import time
import subprocess
from pprint import pprint
from zapv2 import ZAPv2

zap_api_key = '2fcmdarba4478gn2rijv67qrti'

def start_zap_daemon():
    # for windows
    if os.name == 'nt':
        os.chdir("E:/Zed Attack Proxy")
        subprocess.run(f'zap.bat -daemon', shell=True)
    # for Linux based systems
    else: 
        subprocess.run(f'zaproxy -daemon', shell=True)

def zap_scan(target, api_key):
    zap = ZAPv2(apikey=api_key, proxies={
                'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'})

    print('Spidering target {}'.format(target))
    zap.spider.scan(target)
    while int(zap.spider.status()) < 100:
        # Loop until the spider has finished
        print('Spider progress %: {}'.format(zap.spider.status()))
        time.sleep(5)
    print('Spider completed')

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

def main(dns: Annotated[str, typer.Option(help="This option is used for doing a DNS recon on a given domain name.\n Use this option followed by a domain name to get details of DNS records associated with that domain")] = "", zap: Annotated[str, typer.Option(help="This option is used for doing a ZAP Spider Active Scan on a given target.\n Use this option followed by a domain name to do an active scan on the domain")] = "", nikto: Annotated[str, typer.Option(help="This option is used for doing a Nikto Active Scan on a given target(Web Server).\n Use this option followed by a ip address to do an scan on the ip's web server")] = "" , nuclei: Annotated[str, typer.Option(help="This option is used for doing a Nuclei Active Scan on a given target.\n Use this option followed by a domain name to do an scan on the domain's web server")] = "", wapiti: Annotated[str, typer.Option(help="This option is used for doing a Nuclei Active Scan on a given target.\n Use this option followed by a domain name to do an scan on the domain's web server")] = ""):
    domain = dns
    z = zap
    ni = nikto
    nuc = nuclei

    if dns:
        fileName = time.time()
        os.system('echo Starting dnsrecon....... ')
        os.system(f'dnsrecon -d {domain} -j {fileName}_dns.json')

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
        # zap_scan(z, zap_api_key)
        # generate_zap_report(zap_api_key)

    if ni:
        print(ni)
        fileName = time.time()
        os.system('echo Starting Nikto Scanner......')
        os.system(f'nikto -h {ni} -o {fileName}_nikto.json -Format json -Display on')
        os.system('echo Done with the Nikto Scanning')

    if nuc:
        fileName = time.time()
        os.system('echo Starting Nuclei Scanner......')
        os.system(f'nuclei -id ./CVE.txt -u {nuc} -json-export {fileName}_nuclei.json')
        os.system('echo Done with the Nuclei Scanning')
    
if __name__ == "__main__":
    typer.run(main)
    