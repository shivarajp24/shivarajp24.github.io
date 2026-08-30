import requests
import json
import os
from datetime import datetime

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("SHIVARAJCYBER_BOT")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

today = datetime.now().strftime("%B %d, %Y")
day_num = datetime.now().timetuple().tm_yday

topics = [
    "Phishing Attacks", "SQL Injection", "Password Security", "Two-Factor Authentication",
    "Social Engineering", "Ransomware", "VPN Security", "Firewall Basics",
    "Zero Day Exploits", "Man in the Middle Attack", "DDoS Attacks", "Malware Types",
    "Dark Web Basics", "Encryption Explained", "XSS Attacks", "CSRF Attacks",
    "Brute Force Attacks", "Keyloggers", "Spyware", "Trojan Horse",
    "Network Sniffing", "WiFi Security", "Public WiFi Risks", "Cookie Hijacking",
    "DNS Spoofing", "ARP Poisoning", "Port Scanning", "Vulnerability Assessment",
    "Penetration Testing Basics", "Bug Bounty Hunting", "OWASP Top 10",
    "Incident Response", "Digital Forensics", "Cyber Laws in India",
    "Identity Theft", "Credit Card Fraud", "SIM Swapping", "Deepfake Threats",
    "IoT Security", "Cloud Security Basics", "Blue Team vs Red Team",
    "CTF Competitions", "Kali Linux Tools", "Metasploit Basics", "Burp Suite Intro",
    "Nmap Tutorial", "Wireshark Basics", "John the Ripper", "Hashcat Tutorial",
    "OSINT Techniques", "Steganography", "Cryptography Basics", "PKI & Certificates",
    "HTTPS vs HTTP", "Secure Coding Practices", "DevSecOps", "Threat Intelligence",
    "SOC Operations", "SIEM Tools", "Endpoint Security", "Mobile Security",
    "Android Hacking Basics", "iOS Security", "Email Security"
]

topic = topics[day_num % len(topics)]

def generate_content():
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    prompt = f"""You are a cybersecurity educator. Create a professional daily cybersecurity awareness post about: {topic}

Return ONLY a JSON object with these exact keys:
{{
  "topic": "{topic}",
  "headline": "catchy headline max 10 words",
  "intro": "2 sentence introduction",
  "what_is_it": "2-3 sentences explaining what it is",
  "how_it_works": "3-4 sentences explaining how it works",
  "real_world_example": "1 real world example in 2 sentences",
  "protection_tips": ["tip 1", "tip 2", "tip 3", "tip 4", "tip 5"],
  "did_you_know": "1 surprising fact",
  "threat_level": "LOW or MEDIUM or HIGH or CRITICAL"
}}

Return ONLY the JSON, no extra text."""

    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers=headers,
        json={
            "model": "claude-sonnet-4-6",
            "max_tokens": 1500,
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    data = response.json()
    return json.loads(data["content"][0]["text"])

def build_html(content):
    tips_html = "".join(f"<li>{tip}</li>\n" for tip in content["protection_tips"])
    threat_colors = {"LOW":"#00c032","MEDIUM":"#ffb300","HIGH":"#ff6b00","CRITICAL":"#ff3b30"}
    tc = threat_colors.get(content["threat_level"], "#00ff41")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{content['topic']} | Cyber Awareness — Shivaraj Patil</title>
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Inter:wght@400;600;700&family=Orbitron:wght@700;900&display=swap" rel="stylesheet"/>
<style>
:root{{--bg:#060a06;--bg2:#0c120c;--panel:#0f180f;--border:#1a2e1a;--green:#00ff41;--green-mute:#00601a;--cyan:#00e5ff;--text:#c8e6c9;--text-dim:#6a9b6a;--text-muted:#3a5c3a;--white:#f0fff0;--font-mono:'Share Tech Mono',monospace;--font-body:'Inter',sans-serif;--font-head:'Orbitron',monospace}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--text);font-family:var(--font-body);line-height:1.7}}
body::before{{content:'';position:fixed;inset:0;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,255,65,0.012) 2px,rgba(0,255,65,0.012) 4px);pointer-events:none;z-index:9999}}
nav{{position:fixed;top:0;left:0;right:0;z-index:1000;background:rgba(6,10,6,0.92);backdrop-filter:blur(12px);border-bottom:1px solid var(--border);padding:0 2rem;height:56px;display:flex;align-items:center;justify-content:space-between}}
.nav-logo{{font-family:var(--font-head);font-size:0.85rem;color:var(--green);letter-spacing:0.15em}}
.nav-back{{font-family:var(--font-mono);font-size:0.75rem;color:var(--text-dim);text-decoration:none}}
.nav-back:hover{{color:var(--green)}}
.hero{{min-height:55vh;display:flex;flex-direction:column;justify-content:center;padding:80px 2rem 3rem;position:relative;overflow:hidden}}
.hero-grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(0,255,65,0.04) 1px,transparent 1px),linear-gradient(90deg,rgba(0,255,65,0.04) 1px,transparent 1px);background-size:40px 40px;pointer-events:none}}
.hero-inner{{max-width:800px;margin:0 auto;width:100%;position:relative}}
.badge{{font-family:var(--font-mono);font-size:0.7rem;background:rgba(0,255,65,0.06);border:1px solid var(--green-mute);padding:0.3rem 0.8rem;border-radius:2px;display:inline-block;margin-bottom:1rem;letter-spacing:0.15em}}
.date-badge{{color:var(--green)}}
.threat-badge{{color:{tc};background:rgba(0,0,0,0.3);border-color:{tc}44;margin-left:0.5rem}}
h1{{font-family:var(--font-head);font-size:clamp(1.5rem,5vw,2.8rem);color:var(--white);margin-bottom:0.5rem;line-height:1.1}}
.topic-label{{font-family:var(--font-mono);font-size:0.8rem;color:var(--green);letter-spacing:0.1em;margin-bottom:1rem}}
.intro{{font-size:1rem;color:var(--text-dim);max-width:600px;border-left:2px solid var(--green-mute);padding-left:1rem;margin-top:1rem}}
.container{{max-width:800px;margin:0 auto;padding:3rem 2rem}}
.card{{background:var(--panel);border:1px solid var(--border);border-radius:4px;padding:1.6rem;margin-bottom:1.4rem;position:relative;overflow:hidden}}
.card::before{{content:'';position:absolute;left:0;top:0;bottom:0;width:2px;background:var(--green)}}
.card-title{{font-family:var(--font-head);font-size:0.75rem;color:var(--green);letter-spacing:0.15em;margin-bottom:0.8rem}}
.card p{{color:var(--text-dim);font-size:0.92rem;line-height:1.8}}
.tips-list{{list-style:none;padding:0}}
.tips-list li{{color:var(--text-dim);font-size:0.9rem;padding:0.5rem 0;border-bottom:1px solid var(--border);display:flex;gap:0.7rem}}
.tips-list li::before{{content:'→';color:var(--green);font-family:var(--font-mono);flex-shrink:0}}
.fact-card{{background:rgba(0,255,65,0.04);border:1px solid var(--green-mute);border-radius:4px;padding:1.4rem;margin-bottom:1.4rem}}
.fact-card .card-title{{color:var(--cyan)}}
.fact-card p{{color:var(--text);font-style:italic;font-size:0.92rem}}
.back-btn{{display:inline-flex;align-items:center;gap:0.5rem;font-family:var(--font-mono);font-size:0.78rem;color:var(--green);border:1px solid var(--green-mute);padding:0.6rem 1.2rem;border-radius:4px;text-decoration:none;margin-top:1rem;transition:all 0.2s}}
.back-btn:hover{{background:rgba(0,255,65,0.05);border-color:var(--green);color:var(--white)}}
footer{{background:var(--bg);border-top:1px solid var(--border);padding:1.5rem 2rem;text-align:center;font-family:var(--font-mono);font-size:0.68rem;color:var(--text-muted)}}
@media(max-width:600px){{.container{{padding:2rem 1rem}}.hero{{padding:70px 1rem 2rem}}}}
</style>
</head>
<body>
<nav>
  <div class="nav-logo">SP // SECURITY</div>
  <a href="index.html" class="nav-back">← Portfolio</a>
</nav>
<div class="hero">
  <div class="hero-grid"></div>
  <div class="hero-inner">
    <span class="badge date-badge">📅 {today}</span>
    <span class="badge threat-badge">⚠️ {content['threat_level']}</span>
    <div class="topic-label">// DAILY CYBER AWARENESS</div>
    <h1>{content['headline']}</h1>
    <p class="intro">{content['intro']}</p>
  </div>
</div>
<div class="container">
  <div class="card">
    <div class="card-title">// WHAT IS IT?</div>
    <p>{content['what_is_it']}</p>
  </div>
  <div class="card">
    <div class="card-title">// HOW IT WORKS</div>
    <p>{content['how_it_works']}</p>
  </div>
  <div class="card">
    <div class="card-title">// REAL WORLD EXAMPLE</div>
    <p>{content['real_world_example']}</p>
  </div>
  <div class="card">
    <div class="card-title">// PROTECTION TIPS</div>
    <ul class="tips-list">
{tips_html}    </ul>
  </div>
  <div class="fact-card">
    <div class="card-title">// DID YOU KNOW?</div>
    <p>{content['did_you_know']}</p>
  </div>
  <a href="index.html" class="back-btn">← Back to Portfolio</a>
</div>
<footer>
  <span style="color:var(--green)">root@shivaraj:~$</span> Daily Cyber Awareness · shivarajp24.github.io
</footer>
</body>
</html>"""

def update_index(content):
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()
        banner = f"""
<!-- DAILY AWARENESS BANNER -->
<div style="position:fixed;bottom:0;left:0;right:0;z-index:999;background:#0c120c;border-top:1px solid #1a2e1a;padding:0.6rem 1.5rem;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:0.5rem">
  <span style="font-family:'Share Tech Mono',monospace;font-size:0.72rem;color:#6a9b6a">📡 TODAY:</span>
  <a href="daily.html" style="font-family:'Share Tech Mono',monospace;font-size:0.75rem;color:#00ff41;text-decoration:none">{content['topic']} — {content['headline']} →</a>
  <span style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:#3a5c3a">{today}</span>
</div>"""
        if "<!-- DAILY AWARENESS BANNER -->" in html:
            start = html.index("<!-- DAILY AWARENESS BANNER -->")
            end = html.index("</div>", start) + 6
            html = html[:start] + banner.strip() + html[end:]
        else:
            html = html.replace("</body>", banner + "\n</body>")
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("✅ index.html updated")
    except Exception as e:
        print(f"⚠️ index update skipped: {e}")

def send_telegram(content):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Telegram credentials missing")
        return
    message = f"""🔐 *Daily Cyber Awareness*
📅 {today}

🎯 *Topic:* {content['topic']}
⚠️ *Threat Level:* {content['threat_level']}

📖 *{content['headline']}*

{content['intro']}

🌐 Read more: https://shivarajp24.github.io/daily.html

_By Shivaraj Patil | Cybersecurity Portfolio_"""

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        response = requests.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        })
        if response.status_code == 200:
            print("✅ Telegram message sent!")
        else:
            print(f"❌ Telegram error: {response.text}")
    except Exception as e:
        print(f"❌ Telegram error: {e}")

def main():
    print(f"🚀 Generating content for: {topic}")
    content = generate_content()
    print(f"✅ Content: {content['headline']}")
    with open("daily.html", "w", encoding="utf-8") as f:
        f.write(build_html(content))
    print("✅ daily.html created")
    update_index(content)
    send_telegram(content)
    print("🎉 Done!")

if __name__ == "__main__":
    main()
