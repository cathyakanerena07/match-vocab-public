import json, sys, os
HERE=os.path.dirname(os.path.abspath(__file__))
OUT=os.path.dirname(HERE)  # ~/dev/vocabmatch-public
sys.path.insert(0, HERE)
import en_words, ja_front, ja_ex

tpl=open(f"{HERE}/template_v2.html",encoding="utf-8").read()
def gen(title,key,lang,decks,out):
    h=(tpl.replace("/*__TITLE__*/",title).replace("/*__KEY__*/",key)
         .replace("/*__LANG__*/",lang).replace("/*__DATA__*/",json.dumps(decks,ensure_ascii=False)))
    open(out,"w",encoding="utf-8").write(h)
    print("wrote",out.split('/')[-1],"|",sum(len(d['cards']) for d in decks),"cards |",[(d['title'],len(d['cards'])) for d in decks])

# ---- English: 英検帯 leveled, front=日本語 ----
BANDS=[("5","英検5級 · 基礎",["#22c55e","#4ade80"],"中学入門レベルの基本語"),
 ("4","英検4級 · 初級",["#10b981","#14b8a6"],"中学レベルの日常語"),
 ("3","英検3級 · 中級",["#0ea5e9","#38bdf8"],"中学卒業レベル"),
 ("p2","英検準2級 · 中上級",["#6366f1","#818cf8"],"高校中級レベル"),
 ("2","英検2級 · 上級",["#9333ea","#a855f7"],"高校卒業・大学入試レベル"),
 ("p1","英検準1級 · 難関",["#e11d48","#f43f5e"],"大学中級・難関レベル")]
seen=set(); en_decks=[]; nid=0
for b,ttl,color,desc in BANDS:
    cards=[]
    for en,ja in en_words.WORDS[b]:
        if en.lower() in seen: continue
        seen.add(en.lower())
        cards.append({"id":600000+(nid:=nid+1),"front":ja,"back":en,"level":0,"next":0})
    en_decks.append({"id":f"en-{b}","title":ttl,"desc":desc+"（表=日本語）","color":color,"type":"word","cards":cards})
gen("Vocab Match","vmp-en","en-US",en_decks,f"{OUT}/VocabMatch.html")

# ---- Chinese / Korean / German: front→日本語, exEn→日本語 ----
JA=ja_front.JA; JAEX=ja_ex.JAEX
def localize(src_file,title,key,lang,out):
    decks=json.load(open(f"{HERE}/{src_file}"))
    for d in decks:
        d["desc"]=d.get("desc","").replace("（表=英語）","（表=日本語）")
        if "（表=" not in d["desc"]: d["desc"]=d["desc"]+"（表=日本語）"
        for c in d["cards"]:
            c["front"]=JA.get(c["front"],c["front"])
            if c.get("exEn"): c["exEn"]=JAEX.get(c["exEn"],c["exEn"])
    gen(title,key,lang,decks,out)
localize("cn_decks_src.json","Chinese Match","vmp-cn","zh-CN",f"{OUT}/ChineseMatch.html")
localize("ko_decks_src.json","Korean Match","vmp-ko","ko-KR",f"{OUT}/KoreanMatch.html")
localize("de_decks_src.json","German Match","vmp-de","de-DE",f"{OUT}/GermanMatch.html")
print("=== all generated ===")
