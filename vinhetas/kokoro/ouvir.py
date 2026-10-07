import glob, sys, numpy as np, soundfile as sf
from faster_whisper import WhisperModel
m=WhisperModel('small',device='cpu',compute_type='int8')
for f in sorted(glob.glob(sys.argv[1])):
    x,sr=sf.read(f,dtype='float32')
    if x.ndim>1: x=x.mean(1)
    x=np.interp(np.linspace(0,len(x)-1,int(len(x)*16000/sr)),np.arange(len(x)),x).astype(np.float32)
    segs,info=m.transcribe(x,beam_size=5); segs=list(segs)
    lp=sum(s.avg_logprob for s in segs)/max(1,len(segs))
    print(f"{f.split('/')[-1]:22} {info.language} {info.language_probability:.2f} incerteza {-lp:.3f} | "+' '.join(s.text.strip() for s in segs)[:160])
