import requests
import json
import os
from datetime import datetime

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("SHIVARAJCYBER_BOT")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

today = datetime.now().strftime("%B %d, %Y")
day_num = datetime.now().timetuple().tm_yday

topics = [
    "Phishing Attacks","SQL Injection","Password Security","Two-Factor Authentication",
    "Social Engineering","Ransomware","VPN Security","Firewall Basics",
    "Zero Day Exploits","Man in the Middle Attack","DDoS Attacks","Malware Types",
    "Dark Web Basics","Encryption Explained","XSS Attacks","CSRF Attacks",
    "Brute Force Attacks","Keyloggers","Spyware","Trojan Horse",
    "Network Sniffing","WiFi Security","Public WiFi Risks","Cookie Hijacking",
    "DNS Spoofing","ARP Poisoning","Port Scanning","Vulnerability Assessment",
    "Penetration Testing Basics","Bug Bounty Hunting","OWASP Top 10",
    "Incident Response","Digital Forensics","Cyber Laws in India",
    "Identity Theft","Credit Card Fraud","SIM Swapping","Deepfake Threats",
    "IoT Security","Cloud Security Basics","Blue Team vs Red Team",
    "CTF Competitions","Kali Linux Tools","Metasploit Basics","Burp Suite Intro",
    "Nmap Tutorial","Wireshark Basics","Hashcat Tutorial","OSINT Techniques",
    "Cryptography Basics","HTTPS vs HTTP","Secure Coding","Threat Intelligence",
    "SOC Operations","SIEM Tools","Endpoint Security","Mobile Security",
    "Email Security","Steganography","DevSecOps","PKI and Certificates"
]

topic = topics[day_num % len(topics)]

def groq_call(prompt):
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "qwen/qwen3.6-27b",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 2000
        },
        timeout=30
    )
    result = response.json()
    if "error" in result:
        raise Exception(f"Groq Error: {result['error']}")
    text = result["choices"][0]["message"]["content"].strip()

    # Remove <think> tags if present
    import re
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()

    # Extract JSON from markdown
    if "```" in text:
        parts = text.split("```")
        for part in parts:
            if part.startswith("json"):
                text = part[4:].strip()
                break
            elif part.strip().startswith("{") or part.strip().startswith("["):
                text = part.strip()
                break

    # Find JSON start
    if text and text[0] not in ['{', '[']:
        start = -1
        for i, c in enumerate(text):
            if c in ['{', '[']:
                start = i
                break
        if start >= 0:
            text = text[start:]

    return text.strip()

def generate_daily_content():
    prompt = f"""Create a cybersecurity awareness post about: {topic}
Return ONLY valid JSON, no markdown, no extra text:
{{
  "topic": "{topic}",
  "headline": "short catchy headline under 10 words",
  "intro": "2 sentence introduction",
  "what_is_it": "2-3 sentences explaining what it is",
  "how_it_works": "3-4 sentences explaining how it works",
  "real_world_example": "a real world example in 2 sentences",
  "protection_tips": ["tip 1", "tip 2", "tip 3", "tip 4", "tip 5"],
  "did_you_know": "1 surprising fact",
  "threat_level": "HIGH"
}}"""
    return json.loads(groq_call(prompt))

def generate_news():
    prompt = f"""Generate 6 realistic cybersecurity news headlines for {today}.
Mix of: vulnerabilities, ransomware, India cyber news, patches, APT groups.
Return ONLY valid JSON array, no markdown:
[
  {{
    "title": "news headline",
    "desc": "2 sentence description",
    "category": "vulnerability",
    "severity": "CRITICAL",
    "source": "The Hacker News",
    "cat_color": "#ff3b30"
  }},
  {{
    "title": "news headline",
    "desc": "2 sentence description", 
    "category": "ransomware",
    "severity": "HIGH",
    "source": "BleepingComputer",
    "cat_color": "#ff6b00"
  }},
  {{
    "title": "news headline",
    "desc": "2 sentence description",
    "category": "india",
    "severity": "HIGH", 
    "source": "CERT-In",
    "cat_color": "#00e5ff"
  }},
  {{
    "title": "news headline",
    "desc": "2 sentence description",
    "category": "apt",
    "severity": "HIGH",
    "source": "Krebs on Security",
    "cat_color": "#ffb300"
  }},
  {{
    "title": "news headline",
    "desc": "2 sentence description",
    "category": "patch",
    "severity": "MEDIUM",
    "source": "NVD / NIST",
    "cat_color": "#00ff41"
  }},
  {{
    "title": "news headline",
    "desc": "2 sentence description",
    "category": "vulnerability",
    "severity": "HIGH",
    "source": "Dark Reading",
    "cat_color": "#ff6b00"
  }}
]"""
    return json.loads(groq_call(prompt))

def generate_ticker(news_list):
    items = []
    labels = {"vulnerability":"⚡ CVE","ransomware":"🔴 ALERT","india":"🇮🇳 INDIA","apt":"📡 INTEL","patch":"🛡️ PATCH"}
    for n in news_list:
        label = labels.get(n["category"], "⚡ NEWS")
        items.append(f'<span class="ticker-item"><span class="t-label">{label}:</span> {n["title"]} <span class="t-sep">|</span></span>')
    ticker_html = "\n    ".join(items * 2)
    return ticker_html

def build_news_html(news_list):
    cards_html = ""
    sev_classes = {"CRITICAL":"sev-critical","HIGH":"sev-high","MEDIUM":"sev-medium","INFO":"sev-info"}
    source_links = {
        "The Hacker News": "https://thehackernews.com",
        "BleepingComputer": "https://bleepingcomputer.com",
        "CERT-In": "https://cert-in.org.in",
        "Krebs on Security": "https://krebsonsecurity.com",
        "NVD / NIST": "https://nvd.nist.gov",
        "Dark Reading": "https://darkreading.com",
        "Security Week": "https://securityweek.com"
    }
    for n in news_list:
        sev_class = sev_classes.get(n["severity"], "sev-info")
        link = source_links.get(n["source"], "https://thehackernews.com")
        cards_html += f"""
    <a class="news-card" href="{link}" target="_blank" data-cat="{n['category']}">
      <div class="card-cat" style="color:{n['cat_color']}"><span class="cat-dot" style="background:{n['cat_color']}"></span>{n['category'].upper()} <span class="card-severity {sev_class}">{n['severity']}</span></div>
      <div class="card-title">{n['title']}</div>
      <div class="card-desc">{n['desc']}</div>
      <div class="card-meta"><span class="card-source">{n['source']}</span><span class="card-date">Today</span></div>
    </a>"""

    ticker_html = generate_ticker(news_list)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Cyber Security News | Shivaraj Patil</title>
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Inter:wght@300;400;600;700&family=Orbitron:wght@700;900&display=swap" rel="stylesheet"/>
<style>
:root{{--bg:#060a06;--bg2:#0c120c;--panel:#0f180f;--border:#1a2e1a;--green:#00ff41;--green-mute:#00601a;--cyan:#00e5ff;--amber:#ffb300;--red:#ff3b30;--text:#c8e6c9;--text-dim:#6a9b6a;--text-muted:#3a5c3a;--white:#f0fff0;--font-mono:'Share Tech Mono',monospace;--font-body:'Inter',sans-serif;--font-head:'Orbitron',monospace}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--text);font-family:var(--font-body);line-height:1.7;overflow-x:hidden}}
body::before{{content:'';position:fixed;inset:0;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,255,65,0.012) 2px,rgba(0,255,65,0.012) 4px);pointer-events:none;z-index:9999}}
nav{{position:fixed;top:0;left:0;right:0;z-index:1000;background:rgba(6,10,6,0.95);backdrop-filter:blur(12px);border-bottom:1px solid var(--border);padding:0 2rem;height:56px;display:flex;align-items:center;justify-content:space-between}}
.nav-logo{{font-family:var(--font-head);font-size:0.85rem;color:var(--green);letter-spacing:0.15em}}
.nav-links{{display:flex;gap:1.5rem;align-items:center}}
.nav-links a{{font-family:var(--font-mono);font-size:0.75rem;color:var(--text-dim);text-decoration:none;letter-spacing:0.1em;transition:color 0.2s}}
.nav-links a:hover{{color:var(--green)}}
.live-badge{{display:flex;align-items:center;gap:6px;font-family:var(--font-mono);font-size:0.65rem;color:var(--red);letter-spacing:0.15em}}
.live-dot{{width:7px;height:7px;background:var(--red);border-radius:50%;animation:pulse 1.5s ease-in-out infinite}}
@keyframes pulse{{0%,100%{{opacity:1;box-shadow:0 0 6px var(--red)}}50%{{opacity:0.4;box-shadow:none}}}}
.ticker-wrap{{background:var(--bg2);border-top:1px solid var(--border);border-bottom:1px solid var(--border);padding:0.5rem 0;overflow:hidden;margin-top:56px}}
.ticker{{display:flex;gap:3rem;animation:ticker 35s linear infinite;white-space:nowrap}}
.ticker:hover{{animation-play-state:paused}}
@keyframes ticker{{0%{{transform:translateX(0)}}100%{{transform:translateX(-50%)}}}}
.ticker-item{{font-family:var(--font-mono);font-size:0.72rem;color:var(--text-dim);display:flex;align-items:center;gap:0.5rem;flex-shrink:0}}
.ticker-item .t-label{{color:var(--green)}}
.ticker-item .t-sep{{color:var(--text-muted)}}
.hero{{padding:2rem 2rem 2rem;position:relative;overflow:hidden;border-bottom:1px solid var(--border)}}
.hero-grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(0,255,65,0.04) 1px,transparent 1px),linear-gradient(90deg,rgba(0,255,65,0.04) 1px,transparent 1px);background-size:40px 40px;pointer-events:none}}
.hero-inner{{max-width:960px;margin:0 auto;padding:1rem 0;position:relative}}
.section-label{{font-family:var(--font-mono);font-size:0.68rem;color:var(--green);letter-spacing:0.25em;margin-bottom:0.5rem}}
.hero-title{{font-family:var(--font-head);font-size:clamp(1.8rem,5vw,3rem);color:var(--white);margin-bottom:0.5rem;letter-spacing:0.05em}}
.hero-sub{{color:var(--text-dim);font-size:0.95rem}}
.hero-date{{font-family:var(--font-mono);font-size:0.72rem;color:var(--green);margin-top:0.5rem}}
.main{{max-width:960px;margin:0 auto;padding:2rem}}
.filters{{display:flex;flex-wrap:wrap;gap:0.5rem;margin-bottom:2rem}}
.filter-btn{{font-family:var(--font-mono);font-size:0.7rem;color:var(--text-dim);background:transparent;border:1px solid var(--border);padding:0.35rem 0.8rem;border-radius:2px;cursor:pointer;transition:all 0.2s;letter-spacing:0.08em}}
.filter-btn:hover,.filter-btn.active{{color:var(--green);border-color:var(--green);background:rgba(0,255,65,0.06)}}
.news-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1.2rem}}
.news-card{{background:var(--panel);border:1px solid var(--border);border-radius:4px;padding:1.2rem;transition:border-color 0.2s,transform 0.2s;position:relative;overflow:hidden;cursor:pointer;text-decoration:none;display:block;color:inherit}}
.news-card:hover{{border-color:var(--green-mute);transform:translateY(-2px)}}
.news-card::before{{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--green-mute),var(--green));opacity:0;transition:opacity 0.2s}}
.news-card:hover::before{{opacity:1}}
.card-cat{{font-family:var(--font-mono);font-size:0.62rem;letter-spacing:0.15em;margin-bottom:0.6rem;display:flex;align-items:center;gap:0.5rem}}
.cat-dot{{width:6px;height:6px;border-radius:50%;flex-shrink:0}}
.card-title{{font-size:0.9rem;color:var(--white);font-weight:600;line-height:1.4;margin-bottom:0.6rem}}
.card-desc{{font-size:0.78rem;color:var(--text-dim);line-height:1.6;margin-bottom:0.8rem}}
.card-meta{{display:flex;justify-content:space-between;align-items:center}}
.card-source{{font-family:var(--font-mono);font-size:0.62rem;color:var(--text-muted)}}
.card-date{{font-family:var(--font-mono);font-size:0.62rem;color:var(--text-muted)}}
.card-severity{{font-family:var(--font-mono);font-size:0.6rem;padding:0.15rem 0.5rem;border-radius:2px;border:1px solid;margin-left:auto}}
.sev-critical{{color:#ff3b30;border-color:rgba(255,59,48,0.3);background:rgba(255,59,48,0.08)}}
.sev-high{{color:#ff6b00;border-color:rgba(255,107,0,0.3);background:rgba(255,107,0,0.08)}}
.sev-medium{{color:#ffb300;border-color:rgba(255,179,0,0.3);background:rgba(255,179,0,0.08)}}
.sev-info{{color:#00e5ff;border-color:rgba(0,229,255,0.3);background:rgba(0,229,255,0.08)}}
.resources{{margin-top:3rem}}
.resources-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:0.8rem;margin-top:1.2rem}}
footer{{background:var(--bg);border-top:1px solid var(--border);padding:1.5rem 2rem;text-align:center;font-family:var(--font-mono);font-size:0.68rem;color:var(--text-muted);margin-top:3rem}}
@media(max-width:600px){{.main{{padding:1.2rem}}.nav-links a:not(:last-child):not(:first-child){{display:none}}}}
</style>
</head>
<body>
<nav>
  <div class="nav-logo">SP // SECURITY</div>
  <div class="nav-links">
    <a href="index.html">Portfolio</a>
    <a href="news.html" style="color:var(--green)">News</a>
    <a href="ctf.html">CTF</a>
    <a href="daily.html">Daily</a>
    <div class="live-badge"><span class="live-dot"></span>LIVE</div>
  </div>
</nav>
<div class="ticker-wrap">
  <div class="ticker">
    {ticker_html}
  </div>
</div>
<div class="hero">
  <div class="hero-grid"></div>
  <div class="hero-inner">
    <div class="section-label">// CYBER INTEL</div>
    <h1 class="hero-title">Security News Feed</h1>
    <p class="hero-sub">Latest cybersecurity threats, vulnerabilities, and updates — AI-generated daily.</p>
    <div class="hero-date">📅 Updated: {today}</div>
  </div>
</div>
<div class="main">
  <div class="filters">
    <button class="filter-btn active" onclick="filterNews('all',this)">All</button>
    <button class="filter-btn" onclick="filterNews('vulnerability',this)">Vulnerabilities</button>
    <button class="filter-btn" onclick="filterNews('ransomware',this)">Ransomware</button>
    <button class="filter-btn" onclick="filterNews('india',this)">India</button>
    <button class="filter-btn" onclick="filterNews('patch',this)">Patches</button>
    <button class="filter-btn" onclick="filterNews('apt',this)">APT Groups</button>
  </div>
  <div class="news-grid" id="newsGrid">
    {cards_html}
  </div>
  <div class="resources">
    <div class="section-label" style="margin-bottom:1.2rem">// LIVE SOURCES</div>
    <div class="resources-grid">
      <a href="https://thehackernews.com" target="_blank" class="news-card"><div style="font-family:var(--font-mono);font-size:0.72rem;color:var(--green)">🔴 The Hacker News</div><div style="font-size:0.75rem;color:var(--text-dim);margin-top:0.3rem">Latest cyber threats</div></a>
      <a href="https://bleepingcomputer.com" target="_blank" class="news-card"><div style="font-family:var(--font-mono);font-size:0.72rem;color:var(--green)">💻 BleepingComputer</div><div style="font-size:0.75rem;color:var(--text-dim);margin-top:0.3rem">Security & tech news</div></a>
      <a href="https://krebsonsecurity.com" target="_blank" class="news-card"><div style="font-family:var(--font-mono);font-size:0.72rem;color:var(--green)">🕵️ Krebs on Security</div><div style="font-size:0.75rem;color:var(--text-dim);margin-top:0.3rem">Investigative reporting</div></a>
      <a href="https://cert-in.org.in" target="_blank" class="news-card"><div style="font-family:var(--font-mono);font-size:0.72rem;color:var(--green)">🇮🇳 CERT-In</div><div style="font-size:0.75rem;color:var(--text-dim);margin-top:0.3rem">India advisories</div></a>
      <a href="https://nvd.nist.gov" target="_blank" class="news-card"><div style="font-family:var(--font-mono);font-size:0.72rem;color:var(--green)">📋 NVD / CVE</div><div style="font-size:0.75rem;color:var(--text-dim);margin-top:0.3rem">Vulnerability database</div></a>
      <a href="https://darkreading.com" target="_blank" class="news-card"><div style="font-family:var(--font-mono);font-size:0.72rem;color:var(--green)">🌑 Dark Reading</div><div style="font-size:0.75rem;color:var(--text-dim);margin-top:0.3rem">Enterprise security</div></a>
    </div>
  </div>
</div>
<footer>
  <span style="color:var(--green)">root@shivaraj:~$</span> Daily Cyber News · shivarajp24.github.io · Auto-updated by AI
</footer>
<script>
function filterNews(cat,btn){{
  document.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  document.querySelectorAll('.news-card[data-cat]').forEach(card=>{{
    card.style.display=(cat==='all'||card.dataset.cat===cat)?'block':'none';
  }});
}}
</script>
</body>
</html>"""

def build_daily_html(content):
    tips_html = "".join(f"<li>{tip}</li>\n" for tip in content["protection_tips"])
    threat_colors = {"LOW":"#00c032","MEDIUM":"#ffb300","HIGH":"#ff6b00","CRITICAL":"#ff3b30"}
    tc = threat_colors.get(content.get("threat_level","HIGH"), "#ff6b00")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{content['topic']} | Cyber Awareness</title>
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Inter:wght@400;600;700&family=Orbitron:wght@700;900&display=swap" rel="stylesheet"/>
<style>
:root{{--bg:#060a06;--panel:#0f180f;--border:#1a2e1a;--green:#00ff41;--green-mute:#00601a;--cyan:#00e5ff;--text:#c8e6c9;--text-dim:#6a9b6a;--text-muted:#3a5c3a;--white:#f0fff0;--font-mono:'Share Tech Mono',monospace;--font-body:'Inter',sans-serif;--font-head:'Orbitron',monospace}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--text);font-family:var(--font-body);line-height:1.7}}
body::before{{content:'';position:fixed;inset:0;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,255,65,0.012) 2px,rgba(0,255,65,0.012) 4px);pointer-events:none;z-index:9999}}
nav{{position:fixed;top:0;left:0;right:0;z-index:1000;background:rgba(6,10,6,0.92);backdrop-filter:blur(12px);border-bottom:1px solid var(--border);padding:0 2rem;height:56px;display:flex;align-items:center;justify-content:space-between}}
.nav-logo{{font-family:var(--font-head);font-size:0.85rem;color:var(--green);letter-spacing:0.15em}}
.nav-links{{display:flex;gap:1.5rem}}
.nav-links a{{font-family:var(--font-mono);font-size:0.75rem;color:var(--text-dim);text-decoration:none}}
.nav-links a:hover{{color:var(--green)}}
.hero{{min-height:55vh;display:flex;flex-direction:column;justify-content:center;padding:80px 2rem 3rem;position:relative;overflow:hidden}}
.hero-grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(0,255,65,0.04) 1px,transparent 1px),linear-gradient(90deg,rgba(0,255,65,0.04) 1px,transparent 1px);background-size:40px 40px;pointer-events:none}}
.hero-inner{{max-width:800px;margin:0 auto;width:100%;position:relative}}
.badge{{font-family:var(--font-mono);font-size:0.7rem;background:rgba(0,255,65,0.06);border:1px solid var(--green-mute);padding:0.3rem 0.8rem;border-radius:2px;display:inline-block;margin-bottom:1rem;letter-spacing:0.15em}}
h1{{font-family:var(--font-head);font-size:clamp(1.5rem,5vw,2.8rem);color:var(--white);margin-bottom:0.5rem;line-height:1.1}}
.topic-label{{font-family:var(--font-mono);font-size:0.8rem;color:var(--green);letter-spacing:0.1em;margin-bottom:1rem}}
.intro{{font-size:1rem;color:var(--text-dim);max-width:600px;border-left:2px solid var(--green-mute);padding-left:1rem;margin-top:1rem}}
.container{{max-width:800px;margin:0 auto;padding:3rem 2rem}}
.card{{background:var(--panel);border:1px solid var(--border);border-radius:4px;padding:1.6rem;margin-bottom:1.4rem;position:relative}}
.card::before{{content:'';position:absolute;left:0;top:0;bottom:0;width:2px;background:var(--green)}}
.card-title{{font-family:var(--font-head);font-size:0.75rem;color:var(--green);letter-spacing:0.15em;margin-bottom:0.8rem}}
.card p{{color:var(--text-dim);font-size:0.92rem;line-height:1.8}}
.tips-list{{list-style:none;padding:0}}
.tips-list li{{color:var(--text-dim);font-size:0.9rem;padding:0.5rem 0;border-bottom:1px solid var(--border);display:flex;gap:0.7rem}}
.tips-list li::before{{content:'→';color:var(--green);font-family:var(--font-mono);flex-shrink:0}}
.fact-card{{background:rgba(0,255,65,0.04);border:1px solid var(--green-mute);border-radius:4px;padding:1.4rem;margin-bottom:1.4rem}}
.fact-card .card-title{{color:var(--cyan)}}
.fact-card p{{color:var(--text);font-style:italic;font-size:0.92rem}}
.back-btn{{display:inline-flex;align-items:center;gap:0.5rem;font-family:var(--font-mono);font-size:0.78rem;color:var(--green);border:1px solid var(--green-mute);padding:0.6rem 1.2rem;border-radius:4px;text-decoration:none;margin-top:1rem}}
footer{{background:var(--bg);border-top:1px solid var(--border);padding:1.5rem 2rem;text-align:center;font-family:var(--font-mono);font-size:0.68rem;color:var(--text-muted)}}
</style>
</head>
<body>
<nav>
  <div class="nav-logo">SP // SECURITY</div>
  <div class="nav-links">
    <a href="index.html">Portfolio</a>
    <a href="news.html">News</a>
    <a href="ctf.html">CTF</a>
    <a href="daily.html" style="color:var(--green)">Daily</a>
  </div>
</nav>
<div class="hero">
  <div class="hero-grid"></div>
  <div class="hero-inner">
    <span class="badge" style="color:var(--green)">📅 {today}</span>
    <span class="badge" style="color:{tc};background:rgba(0,0,0,0.3);border-color:{tc}44;margin-left:0.5rem">⚠️ {content.get('threat_level','HIGH')}</span>
    <div class="topic-label">// DAILY CYBER AWARENESS</div>
    <h1>{content['headline']}</h1>
    <p class="intro">{content['intro']}</p>
  </div>
</div>
<div class="container">
  <div class="card"><div class="card-title">// WHAT IS IT?</div><p>{content['what_is_it']}</p></div>
  <div class="card"><div class="card-title">// HOW IT WORKS</div><p>{content['how_it_works']}</p></div>
  <div class="card"><div class="card-title">// REAL WORLD EXAMPLE</div><p>{content['real_world_example']}</p></div>
  <div class="card"><div class="card-title">// PROTECTION TIPS</div><ul class="tips-list">{tips_html}</ul></div>
  <div class="fact-card"><div class="card-title">// DID YOU KNOW?</div><p>{content['did_you_know']}</p></div>
  <a href="index.html" class="back-btn">← Back to Portfolio</a>
</div>
<footer><span style="color:var(--green)">root@shivaraj:~$</span> Daily Cyber Awareness · shivarajp24.github.io</footer>
</body>
</html>"""

def update_index(content, news_list):
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()
        banner = f"""<!-- DAILY AWARENESS BANNER -->
<div style="position:fixed;bottom:0;left:0;right:0;z-index:999;background:#0c120c;border-top:1px solid #1a2e1a;padding:0.6rem 1.5rem;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:0.5rem">
  <span style="font-family:'Share Tech Mono',monospace;font-size:0.72rem;color:#6a9b6a">📡 TODAY:</span>
  <a href="daily.html" style="font-family:'Share Tech Mono',monospace;font-size:0.75rem;color:#00ff41;text-decoration:none">{content['topic']} — {content['headline']} →</a>
  <span style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:#3a5c3a">{today}</span>
</div>"""
        if "<!-- DAILY AWARENESS BANNER -->" in html:
            start = html.index("<!-- DAILY AWARENESS BANNER -->")
            end = html.index("</div>", start) + 6
            html = html[:start] + banner + html[end:]
        else:
            html = html.replace("</body>", banner + "\n</body>")
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("✅ index.html updated")
    except Exception as e:
        print(f"⚠️ index update error: {e}")

def send_telegram(content, news_list):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Telegram credentials missing")
        return
    top_news = news_list[0] if news_list else {"title":"Check the site!","severity":"HIGH"}
    message = f"""🔐 *Daily Cyber Update — {today}*

📖 *Awareness Topic:* {content['topic']}
*{content['headline']}*
{content['intro']}

📰 *Top News:* {top_news['title']}
⚠️ Severity: {top_news.get('severity','HIGH')}

🌐 Daily: https://shivarajp24.github.io/daily.html
📡 News: https://shivarajp24.github.io/news.html

_By Shivaraj Patil | Cybersecurity Portfolio_"""

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        r = requests.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }, timeout=10)
        print(f"✅ Telegram: {r.status_code}")
    except Exception as e:
        print(f"❌ Telegram error: {e}")

def main():
    if not GROQ_API_KEY:
        raise Exception("GROQ_API_KEY is missing!")

    print(f"🚀 Generating daily content: {topic}")
    daily_content = generate_daily_content()
    print(f"✅ Daily: {daily_content['headline']}")

    print("📰 Generating news...")
    news_list = generate_news()
    print(f"✅ News: {len(news_list)} articles generated")

    with open("daily.html", "w", encoding="utf-8") as f:
        f.write(build_daily_html(daily_content))
    print("✅ daily.html saved")

    with open("news.html", "w", encoding="utf-8") as f:
        f.write(build_news_html(news_list))
    print("✅ news.html saved")

    update_index(daily_content, news_list)
    send_telegram(daily_content, news_list)
    print("🎉 All done!")

if __name__ == "__main__":
    main()
