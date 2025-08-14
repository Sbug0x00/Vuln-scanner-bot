# Vuln-scanner-bot
# AI Vulnerability Scanner

Automated vulnerability scanner with AI-powered reporting

## Setup
1. Create GitHub repo and upload these files
2. Set secrets in repo settings:
   - `TELEGRAM_BOT_TOKEN` (from @BotFather)
   - `TELEGRAM_CHAT_ID` (use @userinfobot to get ID)
   - `GROQ_API_KEY` (from https://console.groq.com/)
3. Add target domains in `config/targets.txt`
4. Workflow will run daily at 2AM UTC

## Manual Run
Go to Actions > Vulnerability Scan Schedule > Run workflow

## Customization
- Add custom Nuclei templates in `config/nuclei-templates/`
- Modify scan parameters in `scripts/scanner.py`
