import os
import json
import requests
from utils import load_targets, save_results
from llm_processor import generate_report
from telegram_bot import send_report
import subprocess
import sys

def scan_target(target):
    try:
        cmd = f"nuclei -u {target} -t config/nuclei-templates/ -json -o results/{target.replace('://', '_')}.json"
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,  # Tự động raise exception nếu lỗi
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"✅ Scan thành công: {target}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi scan {target}:")
        print(e.stderr)
        sys.exit(1)  # Dừng luồng nếu lỗi nghiêm trọng

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
