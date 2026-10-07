import sys, os, json, torch, torchaudio as ta
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
cfg = json.load(open(sys.argv[1])); out = cfg['out']; os.makedirs(out, exist_ok=True)
torch.set_num_threads(os.cpu_count()); m = ChatterboxMultilingualTTS.from_pretrained(device='cpu')
for v in cfg['vozes']:
    for i, txt in enumerate(cfg['falas']):
        for s in range(cfg['seeds']):
            f = f'{out}/{v}_{i}_{s}.wav'
            if os.path.exists(f): continue
            torch.manual_seed(100 * s + i)
            w = m.generate(txt, language_id='pt', audio_prompt_path=f"{cfg['refs']}/{v}.wav", exaggeration=cfg['exag'], cfg_weight=cfg['cfg'])
            ta.save(f, w, m.sr); print(f.split('/')[-1], round(w.shape[-1] / m.sr, 2), flush=True)
