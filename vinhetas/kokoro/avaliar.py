import glob, re, unicodedata, sys
import numpy as np, soundfile as sf
from faster_whisper import WhisperModel
REF=open(sys.argv[2]).read().strip() if len(sys.argv)>2 else "Pê e Dê Bebidas. Trinta e nove dias de anúncios, no Google e no Meta. Duzentos e dez contatos. Novecentas e dez visitas ao Instagram. E agora, a pergunta que importa: o que esses contatos viraram?"
def norm(s):
    s=unicodedata.normalize('NFKD',s.lower()).encode('ascii','ignore').decode()
    for a,b in [('39','trinta e nove'),('210','duzentos e dez'),('910','novecentas e dez'),('ped ','pe e de '),('p&d','pe e de'),('pd ','pe e de ')]: s=s.replace(a,b)
    return re.findall(r"[a-z]+",s)
def wer(r,h):
    d=[[0]*(len(h)+1) for _ in range(len(r)+1)]
    for i in range(len(r)+1): d[i][0]=i
    for j in range(len(h)+1): d[0][j]=j
    for i in range(1,len(r)+1):
        for j in range(1,len(h)+1): d[i][j]=min(d[i-1][j]+1,d[i][j-1]+1,d[i-1][j-1]+(r[i-1]!=h[j-1]))
    return d[-1][-1]/len(r)
def load(f):
    x,sr=sf.read(f,dtype='float32')
    if x.ndim>1: x=x.mean(1)
    return np.interp(np.linspace(0,len(x)-1,int(len(x)*16000/sr)),np.arange(len(x)),x).astype(np.float32)
m=WhisperModel('small',device='cpu',compute_type='int8'); R=norm(REF); res=[]
for f in sorted(glob.glob(sys.argv[1])):
    segs,_=m.transcribe(load(f),language='pt',beam_size=5,condition_on_previous_text=False)
    segs=list(segs); txt=' '.join(s.text.strip() for s in segs); lp=sum(s.avg_logprob for s in segs)/max(1,len(segs))
    res.append((wer(R,norm(txt)),-lp,f.split('/')[-1],txt))
for w,lp,f,t in sorted(res): print(f"WER {w:5.1%}  incerteza {lp:5.3f}  {f:26} → {t}")
