import subprocess

def run_wapiti_scan(target_url):
    try:
        print('coming till here!')
        # run Wapiti
        # some common parameters:
        # -u : specify the URL
        # --flush-session : start a new session (ignore previous results)
        # --output : specify the output directory
        command = ["wapiti", "-u", target_url, "--flush-session", "--output", "wapiti_output", "--level", "2"]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stderr = process.communicate()

        print("Wapiti Output:")
        print(stdout.decode())

        if stderr:
            print("Errors:")
            print(stderr.decode())

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    target = input("Enter the URL to scan: ")
    run_wapiti_scan(target)
