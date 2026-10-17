#!/usr/bin/env python3
"""Public RSS aggregator. No external Python packages."""
import json, re, time, html, hashlib, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
OUT=Path(__file__).resolve().parents[1]/"data"/"news.json"
FEEDS={"ai":["artificial intelligence AI LLM","trí tuệ nhân tạo Việt Nam"],"gis":["GIS GeoAI remote sensing satellite","viễn thám GIS Việt Nam"],"robot":["robotics autonomous robot IoT","robot môi trường drone"],"security":["cybersecurity privacy technology","an ninh mạng AI"],"blockchain":["blockchain technology Algorand Stellar"],"science":["science technology innovation research","khoa học công nghệ Việt Nam"]}
def clean(s): return re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",html.unescape(s or ""))).strip()
def date(s):
    try: return parsedate_to_datetime(s).astimezone(timezone.utc).isoformat()
    except Exception: return datetime.now(timezone.utc).isoformat()
def main():
    try: old=json.loads(OUT.read_text(encoding="utf-8")).get("articles",[])
    except (FileNotFoundError,ValueError): old=[]
    new=[]; errors=[]
    for topic,queries in FEEDS.items():
        for query in queries:
            url="https://news.google.com/rss/search?"+urllib.parse.urlencode({"q":query+" when:7d","hl":"vi","gl":"VN","ceid":"VN:vi"})
            try:
                req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 RADAR247 RSS Reader"})
                with urllib.request.urlopen(req,timeout=25) as r: raw=r.read(2_000_000)
                for entry in ET.fromstring(raw).findall("./channel/item"):
                    title=clean(entry.findtext("title")); link=(entry.findtext("link") or "").strip()
                    if not title or not link.startswith("https://"): continue
                    source=entry.find("source")
                    publisher=clean(source.text if source is not None else "Google News")
                    new.append({"id":hashlib.sha256(link.encode()).hexdigest()[:20],"title":title[:280],"link":link,"source":publisher,"published":date(entry.findtext("pubDate","")),"summary":clean(entry.findtext("description"))[:450],"topic":topic})
            except Exception as err: errors.append(str(err))
            time.sleep(.3)
    data={}
    for item in old+new: data[item.get("id",item.get("link",""))]=item
    articles=sorted(data.values(),key=lambda x:x.get("published",""),reverse=True)[:500]
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps({"updated_at":datetime.now(timezone.utc).isoformat(),"status":"ok" if new else "cached","collected_count":len(new),"feed_failures":errors,"articles":articles},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Collected",len(new),"stored",len(articles),"errors",len(errors))
    if not articles: raise SystemExit("No RSS articles available; check RSS connectivity.")
if __name__=="__main__": main()
