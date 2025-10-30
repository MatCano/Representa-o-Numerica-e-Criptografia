# Representação Numérica e Criptografia

Ferramentas em Python para **cifras clássicas**, com foco em:
- **Quebra de cifra de substituição monoalfabética** via **pontuação por n-gramas (quadgrams)**;
- **Quebra de cifra de César** (força bruta) via **pontuação por n-gramas (quadgrams)**;
- **Decifra** de mensagens com chave/substituição definida.

---

## ⬇️ Como obter o código (git clone)

Para baixar este repositório localmente via Git:

```bash
git clone https://github.com/MatCano/Representa-o-Numerica-e-Criptografia.git
cd Representa-o-Numerica-e-Criptografia
```

---

## ✨ Visão geral

- **Quebra de Substituição**: busca heurística (p.ex., trocas de letras) guiada por **score de quadgramas**.
- **Pontuação por n-gramas**: utilitário para avaliar “plausibilidade” de um texto.
- **Quebra de César**: teste sistemático dos deslocamentos possíveis (força bruta).
- **Decifra**: aplica uma chave/permutação para obter o texto claro.

---

## 📁 Estrutura do projeto

```
.
├── crack_substitution.py     # Quebra cifra de substituição com score por quadgrams
├── crack_caesar.py           # Quebra cifra de César (força bruta dos deslocamentos)
├── decifrar.py               # Aplica chave/substituição e grava a saída decifrada
├── ngram_score.py            # Classe/funções de pontuação por quadgramas
├── quadgrams                 # Corpus de frequências (quadgramas) usado no score
├── Mensagem-Codificada       # (opcional) exemplo de texto cifrado
├── Mensagem descripitada     # (opcional) exemplo de saída decifrada
└── Trabalho Prático 1.pdf    # Enunciado/relatório acadêmico
```

> Observação: os nomes dos arquivos de entrada/saída podem variar; ajuste caminhos/variáveis dentro dos scripts conforme necessário.

---

## 🧰 Pré-requisitos

- **Python 3.8+** (recomendado 3.10+)
- Sem dependências externas obrigatórias (scripts puros em Python).

---

## 🚀 Como usar

Execute os comandos a partir da **raiz do repositório**. Garanta que `quadgrams` esteja presente para os recursos de substituição.

### 1) Quebrar **cifra de substituição** (monoalfabética)

```bash
python crack_substitution.py
```

Comportamento típico:
- O script busca **uma chave/permutação** que **maximize o score** por quadgramas.
- Exibe/grava a **melhor hipótese de texto claro** e/ou a **chave** encontrada.

> Se precisar mudar arquivo de entrada/saída ou parâmetros, edite as variáveis no próprio script.

### 2) Quebrar **cifra de César** (força bruta)

```bash
python crack_caesar.py
```

Comportamento típico:
- Testa sistematicamente os **deslocamentos k = 1..25**.
- Exibe as melhores hipóteses (e, quando aplicável, o deslocamento mais provável).

> Se o script aceitar parâmetros (ex.: caminho de arquivo, k fixo, etc.), eles estarão documentados no cabeçalho/comentários do arquivo. Na ausência, ajuste as variáveis internas (nome do arquivo cifrado, etc.).

### 3) Pontuar textos com **quadgramas**

```python
from ngram_score import NgramScore

score = NgramScore("quadgrams")
print(score.scoring("EXEMPLO DE TEXTO EM CAPS"))
```

- Quanto **maior** o score, mais “plausível” o texto segundo o corpus de quadgramas.

### 4) **Decifrar** mensagem com chave conhecida

```bash
python decifrar.py
```

- Lê um arquivo de entrada (ex.: `Mensagem-Codificada`) e aplica a **substituição** definida no código (ou encontrada anteriormente), gerando a saída (ex.: `Mensagem descripitada`).

---

## 🧪 Dicas e reprodutibilidade

- Normalização comum em cifras clássicas: **maiúsculas, sem acentos/pontuação** (conforme o script).
- Para heurísticas (substituição), rode múltiplas tentativas e/ou varie a semente aleatória (se existir).
- Verifique permissões/leitura de arquivos e caminhos (entrada/saída, `quadgrams`).

---

## 📖 Base teórica (resumo)

- **Cifra de Substituição Monoalfabética**: mapeia cada letra para outra (permutação). A quebra explora padrões estatísticos (frequências, n-gramas).
- **Pontuação por n-gramas (quadgramas)**: mede a “naturalidade” de um texto; chaves melhores produzem textos com score maior.

- **Cifra de César**: é um caso particular de substituição, em que cada letra é deslocada por um k fixo no alfabeto. 

---

## 🔧 Personalização

- Ajuste **pré-processamento** (remoção de acentos/pontuação) e **alfabeto** conforme a língua alvo.
- Troque `quadgrams` por um corpus do idioma desejado para otimizar a pontuação.
- Para **César**, é simples incluir suporte a **k negativo** e/ou **modo dec** via argumentos.

---

## 🤝 Contribuindo

1. Faça um fork.
2. Crie uma branch: `git checkout -b feature/minha-melhoria`
3. Commit: `git commit -m "feat: descreva sua melhoria"`
4. Push: `git push origin feature/minha-melhoria`
5. Abra um Pull Request.

