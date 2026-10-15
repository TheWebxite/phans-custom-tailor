import re,glob,os,json,html
from html.parser import HTMLParser
EMO=re.compile('[\U0001F000-\U0001FAFF☀-➿⬀-⯿️‍←-⇿✀-➿]')
KEEP={'h2':'h2','h3':'h3','h4':'h3','p':'p','ul':'ul','ol':'ol','li':'li','strong':'strong','b':'strong','em':'em','i':'em','a':'a','blockquote':'blockquote','table':'table','tr':'tr','td':'td','th':'th','thead':'thead','tbody':'tbody','br':'br','img':'img'}
class San(HTMLParser):
  def __init__(s): super().__init__(convert_charrefs=True); s.out=[]; s.skip=0; s.imgs=[]; s.yt=[]
  def handle_starttag(s,t,a):
    a=dict(a)
    if t in('script','style','button','iframe','svg'):
      if t=='iframe' and 'youtube' in (a.get('src') or ''): s.yt.append(a['src'])
      if t!='iframe': s.skip+=1
      return
    if s.skip: return
    k=KEEP.get(t)
    if not k: return
    if k=='a':
      h=a.get('href','')
      s.out.append(f'<a href="{html.escape(h)}">' if h and not h.startswith('javascript') else '<a>')
    elif k=='img':
      src=a.get('src','');
      if src.startswith('//'): src='https:'+src
      s.imgs.append(src); s.out.append(f'<img src="{html.escape(src)}" alt="{html.escape(a.get("alt",""))}">')
    elif k=='br': s.out.append('<br>')
    else: s.out.append(f'<{k}>')
  def handle_endtag(s,t):
    if t in('script','style','button','svg'): s.skip=max(0,s.skip-1); return
    if s.skip: return
    k=KEEP.get(t)
    if k and k not in('img','br'): s.out.append(f'</{k}>')
  def handle_data(s,d):
    if s.skip: return
    s.out.append(html.escape(EMO.sub('',d.replace('\xa0',' ')),quote=False))
def clean(h):
  p=San(); p.feed(h); x=''.join(p.out)
  x=re.sub(r'<(p|h2|h3|li|strong|em)>\s*</\1>','',x)
  x=re.sub(r'<(p|h2|h3|li|strong|em)>\s*</\1>','',x)
  x=re.sub(r'\s+',' ',x).strip()
  return x,p.imgs,p.yt
def block(s,id_):
  i=s.find(f'id="{id_}"')
  if i<0: return None
  i=s.find('>',i)+1; depth=1; j=i
  for m in re.finditer(r'(?i)<(/?)div\b[^>]*>',s[i:]):
    depth+= -1 if m.group(1) else 1
    if depth==0: j=i+m.start(); break
  return s[i:j]
out={}
for f in sorted(glob.glob('blog/*.html')):
  slug=os.path.basename(f)[:-5]; s=open(f,encoding='utf-8').read()
  title=html.unescape(re.search(r'(?is)<div class="article-head">\s*<h1>(.*?)</h1>',s).group(1)).strip()
  date=re.search(r'fa-calendar[^>]*></i>\s*([\d/]+)',s).group(1)
  author=re.search(r'fa-user[^>]*></i>\s*([^<]+)',s).group(1).strip()
  i=s.find('class="article-body"'); i=s.find('>',i)+1
  # end of body: fb-send
  j=s.find('class="fb-send"',i); body=s[i:j]
  langs={}
  for code,id_ in (('vi','content-vi'),('en','content-en'),('zh','content-zh-CN')):
    b=block(body,id_)
    if b: langs[code]=b
  if not langs: langs={'en':body}
  res={'slug':slug,'title':EMO.sub('',title),'date':date,'author':author,'langs':{},'images':[],'youtube':[]}
  for k,v in langs.items():
    c,im,yt=clean(v); res['langs'][k]=c; res['images']+=im
  _,_,yt=clean(body); res['youtube']=yt
  og=re.search(r'property="og:image" content="([^"]+)"',s); res['og']=og.group(1) if og else None
  json.dump(res,open(f'/Users/hengzhexin/Desktop/Client/PhanCustom/_source/blog/{slug}.json','w'),ensure_ascii=False,indent=1)
  print(slug,'|',res['title'],'|',date,author,'| langs',{k:len(v) for k,v in res['langs'].items()},'| imgs',len(res['images']),'| yt',yt,'| og',res['og'])
