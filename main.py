from typing import Tuple
import typer
from typing_extensions import Annotated
import os
import json
import time
from pprint import pprint
from zapv2 import ZAPv2

def zapSpider(str):
    print("inside ",str)
    apiKey = 'lkssshb47bkq8d04gm4p8gabj9'
    target = 'https://public-firing-range.appspot.com'
    zap = ZAPv2(apikey=apiKey, proxies={'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'})

    print('Active Scan target {}'.format(target))

    scanID = zap.ascan.scan(target)
    print(scanID)

    while int(zap.ascan.status(scanID)) < 100:
        print('Scan progress %: {}'.format(zap.ascan.status(scanID)))
        time.sleep(5)

    print('Scan has completed!')

    print('Hosts: {}'.format(', '.join(zap.core.hosts)))
    print('Alerts: ')
    pprint(zap.core.alerts(baseurl=target))


def main(dns: Annotated[str, typer.Option(help="This option is used for doing a DNS recon on a given domain name.\n Use this option followed by a domain name to get details of DNS records associated with that domain")] = "", zap: Annotated[str, typer.Option(help="This option is used for doing a ZAP Spider Active Scan on a given target.\n Use this option followed by a domain name to do an active scan on the domain")] = "", nikto: Annotated[str, typer.Option(help="This option is used for doing a Nikto Active Scan on a given target(Web Server).\n Use this option followed by a ip address to do an scan on the ip's web server")] = "" , nuclei: Annotated[str, typer.Option(help="This option is used for doing a Nuclei Active Scan on a given target.\n Use this option followed by a domain name to do an scan on the domain's web server")] = "" ):
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
        os.system('echo Starting ZAP Proxy Active Scan....... ')
        os.system('E:')
        zapSpider(z)

    if ni:
        print(ni)
        fileName = time.time()
        os.system('echo Starting Nikto Scanner......')
        os.system(f'nikto -h {ni} -o {fileName}_nikto.json -Format json')
        os.system('echo Done with the Nikto Scanning')

    if nuc:
        fileName = time.time()
        os.system('echo Starting Nuclei Scanner......')
        os.system(f'nuclei -u {nuc} -json-export {fileName}_nuclei.json')
        os.system('echo Done with the Nuclei Scanning')
    
if __name__ == "__main__":
    typer.run(main)
    