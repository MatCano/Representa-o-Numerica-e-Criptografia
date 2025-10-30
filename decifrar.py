import random
import math
import string
import os

POPULATION_SIZE = 10
NUM_GENERATIONS = 30000
ELITISM_COUNT = 4
MUTATION_RATE = 0.1
TOURNAMENT_SIZE = 5

ALPHABET = string.ascii_uppercase

def decodificar_binario(bin_string):
    blocos_binarios = bin_string.strip().split(' ')
    texto_cifrado = ""
    for bloco in blocos_binarios:
        if bloco:
            try:
                valor_decimal = int(bloco, 2)
                texto_cifrado += chr(valor_decimal)
            except ValueError:
                continue 
    return texto_cifrado

def carregar_metricas(arquivo="quadgrams"):
    if not os.path.exists(arquivo):
        print(f"Erro: Arquivo '{arquivo}' não encontrado.")
        exit()
    print(f"Carregando métricas de {arquivo}...")
    log_probs = {}
    total_count = 0
    temp_counts = {}
    try:
        with open(arquivo, 'r') as f:
            for linha in f:
                try:
                    partes = linha.strip().split()
                    if len(partes) != 2:
                        continue
                    gram = partes[0]
                    count_str = partes[1]
                    if len(gram) == 4 and count_str.isdigit():
                        count = int(count_str)
                        temp_counts[gram] = count
                        total_count += count
                except Exception:
                    continue
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        exit()
    if total_count == 0:
        print("Erro: Nenhuma métrica válida encontrada no arquivo.")
        exit()
    for gram, count in temp_counts.items():
        log_probs[gram] = math.log10(count / total_count)
    floor_prob = math.log10(0.01 / total_count)
    log_probs["_min_"] = floor_prob
    print("Métricas carregadas com sucesso.")
    return log_probs

def decifrar(texto_cifrado, chave_str):
    mapa_chave = {cifrada: plana for plana, cifrada in zip(ALPHABET, chave_str)}
    texto_plano = ""
    for char_cifrado in texto_cifrado:
        texto_plano += mapa_chave.get(char_cifrado, char_cifrado)
    return texto_plano

def calcular_fitness(texto_plano, log_probs):
    score = 0
    texto_limpo = "".join(filter(str.isalpha, texto_plano.upper()))
    for i in range(len(texto_limpo) - 3):
        tetragrama = texto_limpo[i:i+4]
        score += log_probs.get(tetragrama, log_probs["_min_"])
    return score

def gerar_chave_aleatoria():
    alfabeto_lista = list(ALPHABET)
    random.shuffle(alfabeto_lista)
    return "".join(alfabeto_lista)

def inicializar_populacao(tamanho):
    return [gerar_chave_aleatoria() for _ in range(tamanho)]

def selection_torneio(populacao_com_scores):
    competidores = random.sample(populacao_com_scores, TOURNAMENT_SIZE)
    competidores.sort(key=lambda x: x[1], reverse=True)
    return competidores[0][0]

def order_crossover(pai1, pai2):
    tamanho = len(pai1)
    filho1, filho2 = [""] * tamanho, [""] * tamanho
    c1, c2 = sorted(random.sample(range(tamanho), 2))
    filho1[c1:c2+1] = pai1[c1:c2+1]
    filho2[c1:c2+1] = pai2[c1:c2+1]
    segmento_f1 = set(filho1[c1:c2+1])
    material_p2 = [letra for letra in pai2 if letra not in segmento_f1]
    idx_p2 = 0
    for i in list(range(c2 + 1, tamanho)) + list(range(c1)):
        filho1[i] = material_p2[idx_p2]
        idx_p2 += 1
    segmento_f2 = set(filho2[c1:c2+1])
    material_p1 = [letra for letra in pai1 if letra not in segmento_f2]
    idx_p1 = 0
    for i in list(range(c2 + 1, tamanho)) + list(range(c1)):
        filho2[i] = material_p1[idx_p1]
        idx_p1 += 1
    return "".join(filho1), "".join(filho2)

def mutacao(chave_str):
    chave_lista = list(chave_str)
    i1, i2 = random.sample(range(len(chave_lista)), 2)
    chave_lista[i1], chave_lista[i2] = chave_lista[i2], chave_lista[i1]
    return "".join(chave_lista)

def main():
    mensagem_binaria = (
        "1010110 1000011 1001111 100000 1000001 1010100 1000100 100000 1001000 1001111 100000 1010011 1001111 1010100 1001101 1001111 100000 1010110 1000011 1001111 100000 1001111 1010000 1001010 1001011 1010111 1001001 1010100 1010110 1001110 1010111 1011010 100000 1010111 1000111 100000 1010110 1000011 1001111 100000 1010011 1010111 1001101 1010001 1010111 1001101 100000 1001110 1001101 100000 1010110 1000011 1001111 100000 1000001 1010100 1000100 100000 1001000 1001111 100000 1010110 1000011 1001001 1001111 1010100 1010110 1001111 1011010 100000 1010110 1000011 1001111 100000 1010011 1010111 1011010 1010110 1001110 1011010 1010101 1001110 1011010 1010010 100000 1010111 1000111 100000 1010111 1010101 1001001 100000 1001101 1001010 1001111 1010011 1001110 1001111 1001101 100000 1001110 1011010 100000 1010110 1000011 1010100 1010110 100000 1011000 1001011 1001111 1010100 1011001 100000 1001000 1010111 1001001 1001011 1000001 100000 1010100 1001001 1010001 1001101 100000 1011000 1001111 1010100 1001001 1001110 1011010 1010010 100000 1001001 1001111 1001101 1010111 1010101 1001001 1010011 1001111 100000 1000011 1010101 1011010 1010010 1001001 1000100 100000 1001010 1001111 1010111 1001010 1001011 1001111 100000 1010100 1011010 1000001 100000 1011010 1010100 1010110 1001110 1010111 1011010 1001101 100000 1001000 1010111 1010101 1001011 1000001 100000 1011000 1001111 100000 1001010 1001001 1010111 1011010 1001111 100000 1010110 1010111 100000 1010100 1010011 1010110 100000 1010111 1011010 100000 1010110 1000011 1001111 1001110 1001001 100000 1001011 1010111 1001000 100000 1010011 1010111 1011010 1010110 1001001 1010100 1010011 1010110 1001111 1000001 100000 1001010 1001001 1001111 1001100 1010101 1000001 1001110 1010011 1001111 1001101 100000 1010100 1011010 1000001 100000 1001000 1010111 1010101 1001011 1000001 100000 1000011 1010100 1000010 1001111 100000 1001101 1001111 1001111 1011010 100000 1010110 1000011 1001111 100000 1001011 1010100 1001101 1010110 100000 1010010 1010100 1001101 1001010 100000 1010111 1000111 100000 1000011 1010101 1010001 1010100 1011010 100000 1001111 1011010 1001011 1001110 1010010 1000011 1010110 1001111 1011010 1010001 1001111 1011010 1010110 100000 1010101 1011010 1010110 1001110 1001011 100000 1010110 1000011 1001111 100000 1001001 1001110 1001101 1001111 100000 1010111 1000111 100000 1010100 100000 1000010 1001110 1001101 1001110 1010111 1011010 1010100 1001001 1000100 100000 1011010 1001111 1001000 100000 1010011 1010101 1001011 1010110 1010101 1001001 1001111 100000 1010110 1000011 1010100 1010110 100000 1010111 1011010 1010011 1001111 100000 1010100 1010010 1010100 1001110 1011010 100000 1001111 1010001 1011000 1001001 1010100 1010011 1001111 1001101 100000 1010110 1000011 1001111 100000 1010011 1010111 1001101 1010001 1001110 1010011 100000 1001010 1001111 1001001 1001101 1001010 1001111 1010011 1010110 1001110 1000010 1001111 100000 1010100 100000 1001010 1001111 1001001 1001101 1001010 1001111 1010011 1010110 1001110 1000010 1001111 100000 1001110 1011010 100000 1001000 1000011 1001110 1010011 1000011 100000 1001000 1001111 100000 1010100 1001001 1001111 100000 1010111 1011010 1001111 100000 1000111 1001110 1010110 1010110 1001110 1011010 1010010 100000 1011010 1001111 1001110 1010110 1000011 1001111 1001001 100000 1010100 1011000 1010111 1000010 1001111 100000 1011010 1010111 1001001 100000 1011000 1001111 1001011 1010111 1001000 100000 1011000 1010101 1010110 100000 1001000 1001110 1010110 1000011 1001110 1011010"
    )
    texto_cifrado = decodificar_binario(mensagem_binaria.replace("H", "0"))
    log_probs = carregar_metricas("quadgrams")
    print(f"Iniciando evolução com {POPULATION_SIZE} indivíduos...")
    populacao = inicializar_populacao(POPULATION_SIZE)
    pop_com_scores = []
    for chave in populacao:
        texto_plano = decifrar(texto_cifrado, chave)
        score = calcular_fitness(texto_plano, log_probs)
        pop_com_scores.append((chave, score))
    for geracao in range(NUM_GENERATIONS):
        pop_com_scores.sort(key=lambda x: x[1], reverse=True)
        if geracao % 50 == 0 or geracao == NUM_GENERATIONS - 1:
            print(f"Geração {geracao:4d} | Melhor Score: {pop_com_scores[0][1]:.2f}")
            print(f"  Amostra: {decifrar(texto_cifrado, pop_com_scores[0][0])[:90]}")
        nova_populacao_com_scores = []
        elite = pop_com_scores[:ELITISM_COUNT]
        nova_populacao_com_scores.extend(elite)
        while len(nova_populacao_com_scores) < POPULATION_SIZE:
            pai1 = selection_torneio(pop_com_scores)
            pai2 = selection_torneio(pop_com_scores)
            filho1_chave, filho2_chave = order_crossover(pai1, pai2)
            if random.random() < MUTATION_RATE:
                filho1_chave = mutacao(filho1_chave)
            if random.random() < MUTATION_RATE:
                filho2_chave = mutacao(filho2_chave)
            score_f1 = calcular_fitness(decifrar(texto_cifrado, filho1_chave), log_probs)
            nova_populacao_com_scores.append((filho1_chave, score_f1))
            if len(nova_populacao_com_scores) < POPULATION_SIZE:
                score_f2 = calcular_fitness(decifrar(texto_cifrado, filho2_chave), log_probs)
                nova_populacao_com_scores.append((filho2_chave, score_f2))
        pop_com_scores = nova_populacao_com_scores
    print("\n--- Evolução Concluída ---")
    pop_com_scores.sort(key=lambda x: x[1], reverse=True)
    melhor_chave = pop_com_scores[0][0]
    melhor_score = pop_com_scores[0][1]
    print(f"Melhor Score Final: {melhor_score:.2f}")
    print("\nChave de Substituição Encontrada (Cifra -> Plano):")
    mapa_final_cifra_para_plano = {cifrada: plana for plana, cifrada in zip(ALPHABET, melhor_chave)}
    print(f"Cifra (Alfabeto): {ALPHABET}")
    print(f"Plano (Chave):   {''.join(mapa_final_cifra_para_plano.get(c, '?') for c in ALPHABET)}")
    print("\n--- Mensagem Decifrada (Criptografia 2) ---")
    mensagem_final = decifrar(texto_cifrado, melhor_chave)
    print(mensagem_final)

if __name__ == "__main__":
    main()
