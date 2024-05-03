import os
import subprocess
import time
from zapv2 import ZAPv2
import json


def start_zap_daemon(zap_path):
    # Start ZAP in daemon mode
    if os.name == 'nt':  # Windows
        subprocess.Popen(
            ['start', 'cmd', '/k', '""{}\\zap.bat" -daemon"'.format(zap_path)], shell=True)
    else:  # Unix-like systems
        subprocess.Popen(['gnome-terminal', '--', 'bash', '-c',
                          '{}/zap.sh -daemon &'.format(zap_path)])


def zap_scan(target, api_key, result_file):
    # Initialize ZAP instance
    zap = ZAPv2(apikey=api_key, proxies={
                'http': 'http://127.0.0.1:1025', 'https': 'http://127.0.0.1:1025'})

    # Load the policy for OWASP Top 10
    zap.ascan.set_option_attack_policy('policyName', 'OWASP Top 10')

    # Spider the target
    print('Spidering target {}'.format(target))
    zap.spider.scan(target)
    while int(zap.spider.status()) < 100:
        # Loop until the spider has finished
        print('Spider progress %: {}'.format(zap.spider.status()))
        time.sleep(5)
    print('Spider completed')

    # Active Scan the target
    print('Active Scanning target {} for OWASP Top 10 vulnerabilities'.format(target))
    zap.ascan.scan(target)
    while int(zap.ascan.status()) < 100:
        # Loop until the scanner has finished
        print('Active Scan progress %: {}'.format(zap.ascan.status()))
        time.sleep(5)
    print('Active Scan completed')

    # Collect alerts
    alerts = zap.core.alerts(baseurl=target)

    # Write alerts to file
    with open(result_file, 'w') as f:
        f.write("Alerts found for target {}:\n\n".format(target))
        for index, alert in enumerate(alerts, start=1):
            f.write("Alert {}:\n".format(index))
            f.write("- Name: {}\n".format(alert['name']))
            f.write("- Description: {}\n".format(alert['description']))
            f.write("- URL: {}\n".format(alert['url']))
            f.write("- Confidence: {}\n".format(alert['confidence']))
            f.write("- Risk: {}\n".format(alert['risk']))
            f.write("- Reference: {}\n".format(alert['reference']))
            f.write("\n")

    return alerts


if __name__ == "__main__":
    # Update this with the correct path to your ZAP installation
    zap_path = '"C:/Program Files/ZAP/Zed Attack Proxy"'
    target = 'https://www.youtube.com/'
    api_key = 'jhruomht0d438c8hej49nqphtt'
    result_file = 'scan_results.txt'

    start_zap_daemon(zap_path)

    alerts = zap_scan(target, api_key, result_file)
