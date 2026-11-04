"""Stamp ?v=<content hash> on every local CSS/JS reference so browsers fetch updates right away.
Run from the repo root after editing any file in assets/:  python3 _build/version.py"""
import glob,hashlib,re
files=['andrew.css','chrome.css','footer.css','article.css','nav.js','andrew.js','article.js','posts-data.js']
v={f:hashlib.md5(open('assets/'+f,'rb').read()).hexdigest()[:8] for f in files}
for p in ['index.html']+glob.glob('posts/*.html'):
    h=open(p).read()
    for f in files: h=re.sub(r'(assets/'+re.escape(f)+r')(\?v=[0-9a-f]+)?"',r'\1?v='+v[f]+'"',h)
    open(p,'w').write(h)
print(v)
