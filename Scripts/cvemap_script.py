import os
import json
import subprocess

with open('cwes.txt', 'r') as fp:
    os.system('rm -f temp_cvemap_op.json')

    for line in fp:
        n = line.rstrip('\n')
        print('running for ', n)
        process = subprocess.Popen(['cvemap', '-silent', '--json', '-cwe-id', n], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if stderr:
            print(f'Error occurred while processing CWE {n}: {stderr.decode()}')
            continue

        data = json.loads(stdout.decode())
        
        if data:
            with open('cves.txt', 'a') as fp2:
                for i in data:
                    if(i['is_template']):
                        cve = i['cve_id']
                        fp2.write(f'{cve},')
        else:
            print(f'No data returned for CWE {n}')

print('Finished processing all CWEs')
