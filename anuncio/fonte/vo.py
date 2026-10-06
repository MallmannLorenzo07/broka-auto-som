import re, json, sys, subprocess, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
OUT=sys.argv[1]
k=Kokoro('/tmp/claude-0/kokoro-v1.0.onnx','/tmp/claude-0/voices-v1.0.bin')
tk=k.tokenizer
LINES=[
 ("c1a",0.70,"Broka Auto Som."),
 ("c1b",1.55,"Agora com site novo!"),
 ("c2a",3.35,"Mais som."),
 ("c2b",4.10,"Mais estilo."),
 ("c2c",4.85,"Mais conforto."),
 ("c3a",6.50,"Conheça o nosso site."),
 ("c3b",8.45,"Todos os serviços, em um só lugar."),
 ("c3c",9.95,"Orçamento em um toque."),
 ("c3d",11.45,"E respostas pras suas dúvidas."),
 ("c4a",12.40,"Escolha os serviços,"),
 ("c4b",14.55,"e receba o orçamento direto no WhatsApp."),
 ("c5a",16.95,"Insulfilm nano cerâmica, ou carbono?"),
 ("c5b",18.55,"A gente te ajuda a escolher."),
 ("c6a",20.30,"Broka Auto Som."),
 ("c6b",21.00,"Agende pelo WhatsApp!"),
 ("c6c",22.10,"Acesse o site: link na bio."),
]
def ph(s):
    p=tk.phonemize(s,'pt-br')
    p=re.sub(r'ɾə(?=[^\sˈˌ,.!?aeiouæɐɛɔ])','ɾ',p)   # tira o "e" extra de orçamento/carbono
    p=p.replace('brˈokæ','bɾˈɔkæ')                   # Broka = "Bróca"
    return p
CHAIN=('aresample=48000,rubberband=pitch=0.8409:formant=preserved:pitchq=quality:transients=smooth:detector=soft,'
       'highpass=f=70,equalizer=f=130:t=q:w=0.9:g=4.5,equalizer=f=380:t=q:w=1.2:g=-2.5,'
       'equalizer=f=3200:t=q:w=1.4:g=2,deesser=i=0.4,acompressor=threshold=-22dB:ratio=3:attack=6:release=150:makeup=3')
meta=[]
for key,cue,text in LINES:
    p=ph(text)
    a,sr=k.create(p,voice='pm_alex',speed=1.0,is_phonemes=True)
    # apara silêncio das pontas
    idx=np.where(np.abs(a)>0.01)[0]; a=a[max(0,idx[0]-200):idx[-1]+800]
    sf.write(f'{OUT}/{key}_raw.wav',a,sr)
    # tratamento de locutor: 3 semitons mais grave (timbre preservado), graves, compressão
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'{OUT}/{key}_raw.wav','-af',CHAIN,'-ar','44100',f'{OUT}/{key}.wav'],check=True)
    a,sr=sf.read(f'{OUT}/{key}.wav')
    meta.append(dict(key=key,cue=cue,text=text,dur=round(len(a)/sr,3),ph=p))
json.dump(meta,open(f'{OUT}/meta.json','w'),ensure_ascii=False,indent=1)
for m in meta: print(m['key'],m['cue'],m['dur'],m['ph'])
