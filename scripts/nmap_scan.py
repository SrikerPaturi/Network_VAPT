import xml.etree.ElementTree as ET
import subprocess
import argparse

# Function to run an Nmap scan
def run_nmap_scan(target, output_file):
    try:
        print(f"Running Nmap scan on {target}...")
        command = ["nmap", "-sV", "--script", "vuln", "-oX", output_file, target]
        subprocess.run(command, check=True)
        print(f"Nmap scan completed. Results saved to {output_file}.")
    except subprocess.CalledProcessError as e:
        print(f"Error running Nmap scan: {e}")

# Function to parse Nmap XML output
def parse_nmap_output(file):
    try:
        print("Parsing Nmap results:\n")
        tree = ET.parse(file)
        root = tree.getroot()
        for host in root.findall('host'):
            ip = host.find('address').get('addr')
            print(f"Host: {ip}")
            for port in host.findall('ports/port'):
                port_id = port.get('portid')
                state = port.find('state').get('state')
                service = port.find('service').get('name') if port.find('service') else "Unknown"
                print(f"  - Port {port_id}: {state} ({service})")
    except Exception as e:
        print(f"Error parsing Nmap file: {e}")

# Main function to handle CLI arguments
def main():
    parser = argparse.ArgumentParser(description="Run and parse Nmap scans.")
    parser.add_argument("-t", "--target", required=True, help="Target IP or range for the scan.")
    parser.add_argument("-o", "--output", default="nmap_results.xml", help="File to save Nmap XML output.")

    args = parser.parse_args()
    run_nmap_scan(args.target, args.output)
    parse_nmap_output(args.output)

if __name__ == "__main__":
    main()
