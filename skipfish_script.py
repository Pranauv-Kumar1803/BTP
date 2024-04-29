import subprocess
import os

def run_skipfish(url, output_directory):
    # Ensure the output directory exists or create it
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Construct the Skipfish command
    # Typical usage: skipfish -o [output_path] [target_url]
    command = ["skipfish", "-o", output_directory, url]
    
    try:
        # Execute the Skipfish scan
        print("Starting Skipfish scan...")
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Get output and error (if any)
        stdout, stderr = process.communicate()

        print("Skipfish scan completed.")
        print("Output saved in:", output_directory)

        # Printing the output of Skipfish (usually not needed but good for debugging)
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
