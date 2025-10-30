# Representação Numérica e Criptografia

Ferramentas em Python para **quebrar cifra de substituição monoalfabética** usando **pontuação por n‑gramas (quadgrams)** e decifrar mensagens, desenvolvidas como parte de um trabalho prático de criptografia clássica.

---

## ✨ Visão geral

- **Quebra de cifra de substituição**: busca automática de chaves (heurística) com pontuação estatística de linguagem.
- **Pontuação por n‑gramas**: utilitário para calcular log‑probabilidade de textos via frequências de **quadgramas**.
- **Scripts de decifra**: pipeline para ler mensagem codificada, aplicar a chave e gravar a mensagem decifrada.

---

## 📁 Estrutura do projeto

```
.
├── crack_substitution.py     # Quebra cifra de substituição com score por quadgrams
├── decifrar.py               # Aplica chave/substituição e grava a saída decifrada
├── ngram_score.py            # Classe/funções de pontuação por quadgramas
├── quadgrams                 # Corpus de frequências (quadgramas) usado no score
├── Mensagem-Codificada       # (opcional) exemplo de texto cifrado
├── Mensagem descripitada     # (opcional) exemplo de saída decifrada
└── Trabalho Prático 1.pdf    # Enunciado/relatório acadêmico
```

> Observação: os nomes dos arquivos podem variar; ajuste caminhos/variáveis dentro dos scripts conforme necessário.

---

## 🧰 Pré‑requisitos

- **Python 3.8+** (recomendado 3.10+).
- Sem dependências externas obrigatórias (scripts puros em Python).

---

## 🚀 Como usar

Para baixar este repositório localmente via Git:

```bash
git clone https://github.com/MatCano/Representa-o-Numerica-e-Criptografia.git
cd Representa-o-Numerica-e-Criptografia
```

Execute os comandos a partir da **raiz do repositório**. Garanta que o arquivo `quadgrams` esteja presente.

### 1) Quebrar a cifra de substituição

```bash
python crack_substitution.py
```

Comportamento típico:
- O script tenta **descobrir uma chave de substituição** que maximize o score por quadgramas.
- Exibe/grava a **melhor hipótese de texto claro** e/ou a **permutação de chave** encontrada.

### 2) Usar o módulo de pontuação (quadgramas)

```python
from ngram_score import NgramScore

score = NgramScore("quadgrams")
print(score.scoring("EXEMPLO DE TEXTO EM CAPS"))
```

- Quanto **maior** o score, mais “plausível” o texto na língua alvo (segundo o corpus).

### 3) Decifrar mensagem com uma chave

```bash
python decifrar.py
```

- O script normalmente lê um arquivo de entrada (ex.: `Mensagem-Codificada`) e aplica a **substituição** definida no código (ou a encontrada no passo anterior), gerando a saída (ex.: `Mensagem descripitada`).
- Caso necessário, **edite o script** para apontar para seus próprios arquivos/chave.

---

## 🧪 Dicas e reprodutibilidade

- Garanta que o texto esteja **em caixa alta e sem acentos/pontuação** se o script assim exigir (comum em cifras clássicas).
- Para heurísticas como **hill‑climbing** (troca de letras), rode múltiplas tentativas e/ou varie a semente aleatória (se exposta).
- Verifique permissões/leitura do arquivo `quadgrams` e caminhos dos arquivos de entrada/saída.

---

## 📖 Base teórica (resumo)

- **Cifra de substituição monoalfabética**: cada letra do alfabeto é mapeada para outra (permutação).
- **Quebra por estatística**: textos naturais exibem padrões (frequências de letras e n‑gramas). A chave que **maximiza o score** de quadgramas tende a revelar o texto claro.

---

## 🔧 Personalização

- Ajuste **pré‑processamento** (remoção de acentos/pontuação) e **alfabeto** conforme a língua alvo.
- Substitua `quadgrams` por um corpus do idioma desejado para melhorar a qualidade do score.

---

## 🤝 Contribuindo

1. Faça um fork.
2. Crie uma branch: `git checkout -b feature/minha-melhoria`
3. Commit: `git commit -m "feat: descreva sua melhoria"`
4. Push: `git push origin feature/minha-melhoria`
5. Abra um Pull Request.

---


## 👤 Autores / Créditos
