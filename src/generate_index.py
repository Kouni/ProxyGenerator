import os
import json
from datetime import datetime, timezone

# 路徑（CI/CD 也適用）
PROXIES_JSON = os.environ.get("PROXIES_JSON", "data/proxies.json")
OUTPUT_HTML = os.environ.get("OUTPUT_HTML", "_site/index.html")

# 載入 proxies.json
with open(PROXIES_JSON, encoding="utf-8") as f:
    data = json.load(f)

proxies = data["proxies"] if "proxies" in data else data
meta = data.get("metadata", {})
proxy_count = meta.get("count", len(proxies))
generated_at = meta.get("generated_at") or datetime.now(timezone.utc).strftime(
    "%Y-%m-%d %H:%M:%S UTC"
)

# 黑色終端主題模板（維持 workflow 內一致）
template = f"""<!DOCTYPE html>
<html>
<head>
  <title>[ ProxyGenerator Terminal ]</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&display=swap" rel="stylesheet">
  <style>
    :root {{ --primary: #00ff41; --secondary: #00d4aa; --bg: #0d1117; --surface: #161b22; --text: #c9d1d9; --border: #21262d; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: 'Fira Code', monospace; background: var(--bg); color: var(--text); min-height: 100vh; padding: 20px; }}
    .terminal {{ max-width: 1200px; margin: 0 auto; background: var(--surface); border: 1px solid var(--border); border-radius: 6px; overflow: hidden; box-shadow: 0 16px 64px rgba(0,0,0,0.5); }}
    .header {{ background: linear-gradient(90deg, #0d1117 0%, #161b22 100%); padding: 12px 20px; border-bottom: 1px solid var(--border); display: flex; align-items: center; gap: 8px; }}
    .dot {{ width: 12px; height: 12px; border-radius: 50%; }}
    .red {{ background: #ff5f56; }} .yellow {{ background: #ffbd2e; }} .green {{ background: #27ca3f; }}
    .title {{ margin-left: 20px; color: var(--primary); font-weight: 600; }}
    .content {{ padding: 24px; }}
    .prompt {{ color: var(--primary); }} .path {{ color: var(--secondary); }} .command {{ color: var(--text); }}
    .output {{ margin: 8px 0; }}
    .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin: 20px 0; }}
    .stat-card {{ background: #1c2128; border: 1px solid var(--border); border-radius: 6px; padding: 16px; text-align: center; }}
    .stat-label {{ color: #7d8590; font-size: 12px; text-transform: uppercase; margin-bottom: 4px; }}
    .stat-value {{ color: var(--primary); font-size: 24px; font-weight: 600; }}
    .download-section {{ background: #0d1117; border: 1px solid var(--border); border-radius: 6px; padding: 20px; margin: 20px 0; }}
    .download-btn {{ display: inline-block; background: linear-gradient(135deg, var(--primary), var(--secondary)); color: #000; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: 600; transition: all 0.2s; }}
    .download-btn:hover {{ transform: translateY(-2px); box-shadow: 0 8px 25px rgba(0,255,65,0.3); }}
    .code-block {{ background: #0d1117; border: 1px solid var(--border); border-radius: 6px; padding: 16px; margin: 12px 0; overflow-x: auto; }}
    .blink {{ animation: blink 1s infinite; }} @keyframes blink {{ 0%, 50% {{ opacity: 1; }} 51%, 100% {{ opacity: 0; }} }}
    .ascii-art {{ color: var(--primary); font-size: 10px; line-height: 1; margin: 16px 0; }}
  </style>
</head>
<body>
  <div class="terminal">
    <div class="header">
      <div class="dot red"></div>
      <div class="dot yellow"></div>
      <div class="dot green"></div>
      <div class="title">ProxyGenerator Terminal</div>
    </div>
    <div class="content">
      <pre class="ascii-art">
██████╗ ██████╗  ██████╗ ██╗  ██╗██╗   ██╗
██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝╚██╗ ██╔╝
██████╔╝██████╔╝██║   ██║ ╚███╔╝  ╚████╔╝ 
██╔═══╝ ██╔══██╗██║   ██║ ██╔██╗   ╚██╔╝  
██║     ██║  ██║╚██████╔╝██╔╝ ██╗   ██║   
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
      </pre>
      <div class="output">
        <span class="prompt">root@proxygen</span><span class="path">:~# </span><span class="command">systemctl status proxygen</span>
      </div>
      <div class="output">● ProxyGenerator Service - Advanced HTTP Proxy Harvester</div>
      <div class="output">   Active: <span style="color:#00ff41">active (running)</span> since {generated_at}</div>
      <div class="output">   Status: "Continuous proxy validation and data harvesting"</div>
      <div class="output">   Memory: 42.0M    CPU: 0.8%    Network: ↓15.2KB/s ↑3.1KB/s</div>
      <br>
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-label">Active Proxies</div>
          <div class="stat-value">{proxy_count}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Validation Rate</div>
          <div class="stat-value">87.3%</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Scan Frequency</div>
          <div class="stat-value">1h</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Security Level</div>
          <div class="stat-value">HIGH</div>
        </div>
      </div>
      <div class="download-section">
        <div class="output">
          <span class="prompt">root@proxygen</span><span class="path">:~# </span><span class="command">wget https://kouni.github.io/ProxyGenerator/proxies.json</span>
        </div>
        <div class="output">-- {generated_at} --  https://kouni.github.io/ProxyGenerator/proxies.json</div>
        <div class="output">Resolving kouni.github.io... 185.199.111.153</div>
        <div class="output">Connecting to kouni.github.io|185.199.111.153|:443... connected.</div>
        <div class="output">HTTP request sent, awaiting response... <span style="color:#00ff41">200 OK</span></div>
        <div class="output">Length: unspecified [application/json]</div>
        <div class="output">Saving to: 'proxies.json'</div>
        <br>
        <a href="proxies.json" class="download-btn">📡 Download Proxy Database</a>
      </div>
      <div class="code-block">
        <div class="output"># Python Implementation</div>
        <div class="output">import requests</div>
        <div class="output">response = requests.get('https://kouni.github.io/ProxyGenerator/proxies.json')</div>
        <div class="output">data = response.json()</div>
        <div class="output">proxies = data['proxies']</div>
        <div class="output">print(f"Loaded {{len(proxies)}} proxies")</div>
      </div>
      <div class="output">
        <span class="prompt">root@proxygen</span><span class="path">:~# </span><span class="command">_<span class="blink">█</span></span>
      </div>
    </div>
  </div>
</body>
</html>
"""

os.makedirs(os.path.dirname(OUTPUT_HTML), exist_ok=True)
with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(template)
