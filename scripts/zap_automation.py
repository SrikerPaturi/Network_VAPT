from zapv2 import ZAPv2
import time
import argparse

# Function to perform ZAP scanning
def perform_zap_scan(target_url, api_key, report_file):
    try:
        zap = ZAPv2(apikey=api_key)
        
        print(f"Starting spidering on: {target_url}")
        zap.urlopen(target_url)
        zap.spider.scan(target_url)
        
        while int(zap.spider.status) < 100:
            print(f"Spidering progress: {zap.spider.status}%")
            time.sleep(2)
        print("Spidering completed.")

        print("Starting active scan...")
        zap.ascan.scan(target_url)
        
        while int(zap.ascan.status) < 100:
            print(f"Active scan progress: {zap.ascan.status}%")
            time.sleep(2)
        print("Active scan completed.")

        print(f"Generating report at {report_file}...")
        report = zap.core.htmlreport()
        with open(report_file, "w") as file:
            file.write(report)
        print("Report generated successfully.")
    except Exception as e:
        print(f"Error during ZAP scan: {e}")

# Main function to handle CLI arguments
def main():
    parser = argparse.ArgumentParser(description="Automate OWASP ZAP scans and generate reports.")
    parser.add_argument("-u", "--url", required=True, help="Target URL for scanning.")
    parser.add_argument("-k", "--apikey", required=True, help="API key for OWASP ZAP.")
    parser.add_argument("-r", "--report", default="zap_report.html", help="Path to save the HTML report.")

    args = parser.parse_args()
    perform_zap_scan(args.url, args.apikey, args.report)

if __name__ == "__main__":
    main()
