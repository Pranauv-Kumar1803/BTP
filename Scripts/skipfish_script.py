import subprocess
import os

def run_skipfish(url, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Skipfish command
    command = ["skipfish", "-o", output_directory, url]
    
    try:
        print("Starting Skipfish scan...")
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        stdout, stderr = process.communicate()

        print("Skipfish scan completed.")
        print("Output saved in:", output_directory)

        # Print the o/p of Skipfish scan 
        print(stdout.decode())
        if stderr:
            print("Errors during scan:")
            print(stderr.decode())

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    target_url = input("Enter the URL to scan: ")
    output_dir = input("Enter the output directory path: ")
    run_skipfish(target_url, output_dir)
