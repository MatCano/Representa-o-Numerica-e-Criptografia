#!/usr/bin/env python3
import sys, random, math, string
from pathlib import Path
from importlib.machinery import SourceFileLoader

# ===== ARQUIVOS PADRÃO (sem extensão) =====
DEFAULT_MSG_FILE = "Mensagem-Codificada"
DEFAULT_QUADGRAMS_FILE = "quadgrams"
alphabet = string.ascii_uppercase

def load_quadgrams(path: str) -> str:
    """Limpa o arquivo de quadrigramas para 'TOKEN COUNT' e salva em <path>.clean."""
    clean_lines = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2 and parts[0].isalpha() and parts[1].isdigit():
                clean_lines.append(f"{parts[0]} {parts[1]}")
    tmp = path + ".clean"
    with open(tmp, "w", encoding="utf-8") as g:
        g.write("\n".join(clean_lines))
    return tmp

def binary_to_text(s: str) -> str:
    """Converte '01001000 01100101 ...' -> 'He...' (ignora tokens não binários)."""
    out = []
    for tok in s.split():
        if set(tok) <= {"0","1"}:
            try:
                out.append(chr(int(tok, 2)))
            except ValueError:
                pass
    return "".join(out)

def decrypt_subst(ctext: str, key: str) -> str:
    return ctext.translate(str.maketrans(alphabet, key))

def random_swap(key: str) -> str:
    a, b = random.sample(range(26), 2)
    k = list(key); k[a], k[b] = k[b], k[a]
    return "".join(k)

def freq_init_key(ct: str) -> str:
    from collections import Counter
    ETAOIN = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
    freq = [p for p,_ in Counter(ct).most_common()]
    key_map = {}
    for i, ch in enumerate(freq):
        if i < len(ETAOIN):
            key_map[ch] = ETAOIN[i]
    remaining = [ch for ch in alphabet if ch not in key_map.values()]
    for ch in alphabet:
        if ch not in key_map:
            key_map[ch] = remaining.pop(0)
    return "".join(key_map[ch] for ch in alphabet)

def anneal(ctext: str, scorer, iters=15000, temp_start=8.0, temp_end=0.01):
    key = freq_init_key(ctext)
    pt = decrypt_subst(ctext, key)
    best_key, best_score = key, scorer.score(pt)
    key_score = best_score
    for i in range(1, iters+1):
        T = temp_start * ((temp_end / temp_start) ** (i/iters))
        k2 = random_swap(key)
        pt2 = decrypt_subst(ctext, k2)
        s2 = scorer.score(pt2)
        delta = s2 - key_score
        if delta > 0 or math.exp(delta/max(T,1e-9)) > random.random():
            key, key_score = k2, s2
            if s2 > best_score:
                best_key, best_score = k2, s2
    return best_key, best_score

def main(msg_path: str, quadgram_path: str):
    qpath = load_quadgrams(quadgram_path)
    ngram_score = SourceFileLoader("ngram_score", "ngram_score.py").load_module().ngram_score(qpath, sep=" ")

    raw = Path(msg_path).read_text(encoding="utf-8", errors="ignore")
    decoded = binary_to_text(raw).upper()

    # Só letras para buscar a chave
    ctext = "".join(ch for ch in decoded if ch.isalpha())

    best_key, best_score = None, -1e9
    for _ in range(6):
        k, s = anneal(ctext, ngram_score, iters=15000, temp_start=8.0, temp_end=0.01)
        if s > best_score:
            best_key, best_score = k, s

    # Aplica sobre o texto completo preservando não-letras
    table = str.maketrans(alphabet, best_key)
    full_plain = decoded.translate(table)

    print(f"[+] Best substitution key (cipher A..Z -> plain): {best_key}")
    print(full_plain)

if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    msg = str((here / DEFAULT_MSG_FILE).resolve())
    grams = str((here / DEFAULT_QUADGRAMS_FILE).resolve())

    # Opcional: permitir sobrescrever via argumentos
    if len(sys.argv) == 3:
        msg, grams = sys.argv[1], sys.argv[2]
    elif len(sys.argv) not in (1, 3):
        print("Uso: py crack_substitution.py  (usa 'mensagem' e 'quadgramas')  OU  py crack_substitution.py <mensagem> <quadgramas>")
        sys.exit(1)

    for p in [msg, grams]:
        if not Path(p).exists():
            print(f"Erro: arquivo não encontrado: {p}")
            sys.exit(1)

    main(msg, grams)
