import subprocess

def run_wapiti_scan(target_url):
    try:
        print('atleast coming till here!')
        # Specify the command to run Wapiti
        # Here we are using some common parameters:
        # -u : specify the URL
        # --flush-session : start a new session (ignore previous results)
        # --output : specify the output directory
        command = ["wapiti", "-u", target_url, "--flush-session", "--output", "wapiti_output", "--level", "2"]

        # Start the Wapiti scan process
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Wait for the process to complete and get the output and errors
        stdout, stderr = process.communicate()

        # Print the standard output and standard error from Wapiti
        print("Wapiti Output:")
        print(stdout.decode())

        if stderr:
            print("Errors:")
            print(stderr.decode())

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    target = input("Enter the URL to scan: ")
    run_wapiti_scan(target)
