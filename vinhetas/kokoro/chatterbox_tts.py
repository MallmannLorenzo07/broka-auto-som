"""Narração gratuita e sem conta: Chatterbox Multilingual (Resemble AI, licença MIT), clonando o timbre de uma referência.
Uso: python chatterbox_tts.py REF.wav saida_dir [--exag 0.45 --cfg 0.5 --seed 1] "fala 1" "fala 2" ...  → saida_dir/0.wav ..."""
import sys, os, argparse, torch, torchaudio as ta
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
p = argparse.ArgumentParser(); p.add_argument('ref'); p.add_argument('out'); p.add_argument('falas', nargs='+')
p.add_argument('--exag', type=float, default=.45); p.add_argument('--cfg', type=float, default=.5); p.add_argument('--seed', type=int, default=1)
p.add_argument('--prefixo', default='')
a = p.parse_args(); torch.set_num_threads(os.cpu_count()); os.makedirs(a.out, exist_ok=True)
m = ChatterboxMultilingualTTS.from_pretrained(device='cpu')
for i, txt in enumerate(a.falas):
    torch.manual_seed(a.seed + i)
    w = m.generate(txt, language_id='pt', audio_prompt_path=a.ref, exaggeration=a.exag, cfg_weight=a.cfg)
    ta.save(f'{a.out}/{a.prefixo}{i}.wav', w, m.sr); print(i, round(w.shape[-1] / m.sr, 2), txt, flush=True)
