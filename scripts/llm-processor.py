import os
import json
import requests

def generate_report(vuln_data):
    """Generate vulnerability report using free LLM APIs"""
    # Try Groq first (free tier)
    if os.getenv("GROQ_API_KEY"):
        return groq_report(vuln_data)
    
    # Fallback to Together.ai
    return together_report(vuln_data)

def groq_report(vuln_data):
    """Generate report using Groq API"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""
    Create professional vulnerability report:
    Target: {vuln_data['host']}
    Vulnerability: {vuln_data['info']['name']}
    Severity: {vuln_data['info']['severity']}
    
    Include:
    1. Technical explanation (50 words)
    2. Business impact
    3. Step-by-step fix guide
    4. Suggested donation: $3-5 (optional support)
    """
    
    payload = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response.json()['choices'][0]['message']['content']
    except:
        return None

def together_report(vuln_data):
    """Fallback to Together.ai API"""
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('TOGETHER_API_KEY')}",
        "Content-Type": "application/json"
    }
    
    prompt = f"Generate vulnerability report for {vuln_data['host']} - {vuln_data['info']['name']}"
    
    payload = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 512
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response.json()['choices'][0]['message']['content']
    except:
        return "Error generating report"
