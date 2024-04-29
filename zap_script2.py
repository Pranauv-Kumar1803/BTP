from typing import Tuple
import typer
from typing_extensions import Annotated
import os
import json
import time
import subprocess
from pprint import pprint
from zapv2 import ZAPv2

zap_api_key = 'u4c9ua43rb2ua97ika3113vl6e'

def start_zap_daemon():
    # for Windows
    if os.name == 'nt':
        os.chdir("E:/Zed Attack Proxy")
        process = subprocess.Popen(['zap.bat', '-daemon'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # for Linux based systems
    else: 
        os.system('zaproxy -daemon')


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


# os.system('echo Starting ZAP Daemon...... ')
# start_zap_daemon()
# time.sleep(10)
os.system('starting the scan now/.........')
zap_scan("https://www.goibibo.com", zap_api_key)
generate_zap_report(zap_api_key)