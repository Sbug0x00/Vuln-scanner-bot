import os
import json
import requests
from utils import load_targets, save_results
from llm_processor import generate_report
from telegram_bot import send_report

def scan_target(target):
    """Scan a single target using Nuclei"""
    print(f"Scanning: {target}")
    
    # Run Nuclei scan (XSS and SQLi templates)
    os.system(f"nuclei -u {target} -t config/nuclei-templates/ -severity medium,high,critical -json -o results/{target.replace('://', '_')}.json")
    
    # Process results
    with open(f"results/{target.replace('://', '_')}.json", 'r') as f:
        vulns = [json.loads(line) for line in f.readlines()]
    
    # Generate AI reports for found vulnerabilities
    for vuln in vulns:
        report = generate_report(vuln)
        send_report(report)

if __name__ == "__main__":
    targets = load_targets("config/targets.txt")
    for target in targets:
        scan_target(target)
    print("Scan completed! Reports sent to Telegram.")
