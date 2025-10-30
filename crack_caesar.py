#!/usr/bin/env python3
import sys, string
from pathlib import Path
from importlib.machinery import SourceFileLoader

# ===== ARQUIVOS PADRÃO (sem extensão) =====
DEFAULT_MSG_FILE = "Mensagem-Codificada"
DEFAULT_QUADGRAMS_FILE = "quadgrams"

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

def main(msg_path: str, quadgram_path: str):
    qpath = load_quadgrams(quadgram_path)
    ngram = SourceFileLoader("ngram_score", "ngram_score.py").load_module().ngram_score(qpath, sep=" ")

    raw = Path(msg_path).read_text(encoding="utf-8", errors="ignore")
    decoded = binary_to_text(raw).upper()

    alphabet = string.ascii_uppercase
    def caesar(s: str, k: int) -> str:
        table = str.maketrans(alphabet, alphabet[-k:] + alphabet[:-k])
        return s.translate(table)

    best = None
    for k in range(26):
        pt = caesar(decoded, k)
        score = ngram.score(pt.replace(" ", ""))
        if best is None or score > best[0]:
            best = (score, k, pt)

    _, k, pt = best
    print(f"[+] Best Caesar key (shift): {k}")
    print(pt)

if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    msg = str((here / DEFAULT_MSG_FILE).resolve())
    grams = str((here / DEFAULT_QUADGRAMS_FILE).resolve())

    # Opcional: permitir sobrescrever via argumentos
    if len(sys.argv) == 3:
        msg, grams = sys.argv[1], sys.argv[2]
    elif len(sys.argv) not in (1, 3):
        print("Uso: py crack_caesar.py  (usa 'mensagem' e 'quadgramas')  OU  py crack_caesar.py <mensagem> <quadgramas>")
        sys.exit(1)

    for p in [msg, grams]:
        if not Path(p).exists():
            print(f"Erro: arquivo não encontrado: {p}")
            sys.exit(1)

    main(msg, grams)
