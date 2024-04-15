import requests
import json
import re

def fetch_template_data(url):
    """Fetch the template data from a remote JSON file."""
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

def search_owasp_in_templates(template_path):
    """Search through templates for OWASP-related content and save IDs."""
    owasp_keywords = {
        'A1': ['injection', 'sql injection', 'command injection'],
        'A2': ['broken authentication', 'session management'],
        'A3': ['sensitive data exposure'],
        'A4': ['xxe', 'external entities'],
        'A5': ['broken access control'],
        'A6': ['security misconfiguration'],
        'A7': ['xss', 'cross site scripting'],
        'A8': ['insecure deserialization'],
        'A9': ['known vulnerabilities', 'component with vulnerabilities'],
        'A10': ['insufficient logging', 'monitoring']
    }
    
    ids = []
    patterns = {key: re.compile('|'.join(words), re.IGNORECASE) for key, words in owasp_keywords.items()}

    with open('../nuclei-templates/cves.json', 'r', encoding='utf-8') as fp:
        for line in fp:
            try:
                template = json.loads(line.strip())
                # print(template)
                name = template['Info']['Name']
                description = template['Info']['Description']
                for key, pattern in patterns.items():
                    if pattern.search(name) or pattern.search(description):
                        ids.append(template['ID'])
                        break

            except json.JSONDecodeError as e:
                print(f"Error parsing JSON : {e}")

    return ids

def save_ids_to_file(ids, filename):
    with open(filename, 'a') as file:
        for id in ids:
            file.write(id + ',')


templates = 'cves.json'
if templates:
    owasp_ids = search_owasp_in_templates(templates)
    # print(len(owasp_ids))
    save_ids_to_file(owasp_ids, 'owasp_ids.txt')
    # print(f"Saved {len(owasp_ids)} IDs to owasp_ids.txt")
