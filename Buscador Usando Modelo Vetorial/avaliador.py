import math
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import f1_score
def ler_arquivo_esperado(caminho_arquivo):
    dic_esperados = {}
    with open(caminho_arquivo, 'r') as arquivo_esperado:
        for linha in arquivo_esperado:
            linha = linha.replace("\n", "").replace(" ", "")
            consulta, doc, votos = linha.split(";")
            if not consulta.isdecimal():
                continue
            consulta = str(consulta)
            votos = int(votos)
            if consulta not in dic_esperados:
                dic_esperados[consulta] = {doc: votos}
            else:
                if doc not in dic_esperados[consulta]:
                    dic_esperados[consulta][doc] = votos
                else:
                    dic_esperados[consulta][doc] += votos
    return dic_esperados

def ler_arquivo_resultados(caminho_arquivo):
    dic_resultados = {}
    with open(caminho_arquivo, 'r') as arquivo_resultados:
        for i, linha in enumerate(arquivo_resultados):
            if i == 0:  # Ignorar a primeira linha
                continue
            linha = linha.replace("\n", "").replace(" ", "")
            consulta, lista_resultados = linha.split(";")
            lista_resultados = lista_resultados[1:-1].split('[')
            for lista_rank in lista_resultados:
                doc_info = lista_rank.strip("],").split(",")
                if len(doc_info) < 3:
                    continue
                doc_number = str(int(doc_info[1]))
                if consulta not in dic_resultados:
                    dic_resultados[consulta] = {doc_number: 1}
                else:
                    if doc_number not in dic_resultados[consulta]:
                        dic_resultados[consulta][doc_number] = 1
                    else:
                        dic_resultados[consulta][doc_number] += 1
    return dic_resultados

def calcular_precisao_recall(dic_esperados, dic_resultados):
    r_precisao = []
    tabela_precisoes = pd.DataFrame(0.0, index=range(1, 101), columns=["precisao@5", "precisao@10"])
    media_precisao = 0
    media_media_precisao = 0
    dcg = [0] * 10
    media_dcg = [0] * 10
    rr = 0
    media_rr = 0
    onze_recall_total = [0] * 11
    onze_recall_consulta = [0] * 11
    for chave, valor in dic_resultados.items():
        media_precisao = 0
        dic_consulta = dic_esperados.get(chave)
        if dic_consulta is None:
            continue
        num_recuperados = 0.0
        num_recuperados_relevantes = 0.0
        num_relevantes = len(dic_consulta)
        for doc in valor:
            num_recuperados += 1
            if doc in dic_consulta.keys():
                num_recuperados_relevantes += 1
            precisao = 100 * (num_recuperados_relevantes / num_recuperados)
            recall = math.floor(100 * (num_recuperados_relevantes / num_relevantes)) / 10
            recall = int(recall)
            onze_recall_consulta[recall] = max(onze_recall_consulta[recall], precisao)
            if num_recuperados == 5:
                chave = int(chave)
                tabela_precisoes.loc[chave]['precisao@5'] = precisao / 100
            if num_recuperados == 10:
                chave = int(chave)
                tabela_precisoes.loc[chave]['precisao@10'] = precisao / 100
            if num_recuperados == num_relevantes:
                r_precisao.append(num_recuperados_relevantes / num_relevantes)
            if num_recuperados <= num_relevantes:
                media_precisao += (num_recuperados_relevantes / num_recuperados) / num_relevantes
            if num_recuperados_relevantes == 1:
                rr = 1 / num_recuperados
            if int(num_recuperados) <= 10:
                if int(num_recuperados) == 1:
                    dcg[int(num_recuperados) - 1] = (2 ** num_recuperados_relevantes - 1) / (math.log(1 + num_recuperados))
                    continue
                dcg[int(num_recuperados - 1)] = dcg[int(num_recuperados - 2)] + (
                            2 ** num_recuperados_relevantes - 1) / (math.log(1 + num_recuperados))
        media_media_precisao += media_precisao / 100
        media_rr += rr / 100
        for i in range(len(dcg)):
            media_dcg[i] += dcg[i] / 100
        for i in range(len(onze_recall_total)):
            onze_recall_total[i] = max(onze_recall_consulta[i], onze_recall_total[i])
    return tabela_precisoes, media_media_precisao, media_rr, media_dcg, onze_recall_total, r_precisao

def calcular_f1_score(dic_esperados, dic_resultados):
    f1_scores = []
    for chave, valor in dic_resultados.items():
        dic_consulta = dic_esperados.get(chave)
        if dic_consulta is None:
            continue
        num_recuperados = 0.0
        num_recuperados_relevantes = 0.0
        num_relevantes = len(dic_consulta)
        y_true = []
        y_pred = []
        for doc in valor:
            num_recuperados += 1
            if doc in dic_consulta.keys():
                num_recuperados_relevantes += 1
                y_true.append(1)
            else:
                y_true.append(0)
            y_pred.append(1)
            if num_recuperados == num_relevantes:
                f1 = f1_score(y_true, y_pred)
                f1_scores.append(f1)
    return f1_scores

def gerar_graficos(tabela_precisoes1, tabela_precisoes2, media_dcg1, media_dcg2, onze_recall_total1, onze_recall_total2, r_precisao1, r_precisao2, f1_scores1, f1_scores2):
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 11), [dcg / 100 for dcg in media_dcg1], color='blue', linestyle='solid', linewidth=3, marker='o', markerfacecolor='black', markersize=6, label='stemmer')
    plt.plot(range(1, 11), [dcg / 100 for dcg in media_dcg2], color='red', linestyle='solid', linewidth=3, marker='o', markerfacecolor='black', markersize=6, label='nostemmer')
    plt.yscale('log')
    plt.ylim(0.01, 1)
    plt.xlim(1, 10)
    plt.xlabel('Ranking n', fontsize=14)
    plt.ylabel('DCG Médio', fontsize=14)
    plt.title('Gráfico Média DCG', fontsize=16)
    plt.legend()
    plt.grid(True)
    plt.savefig("./avaliacao/media_dcg.png", dpi=300)
    plt.figure(figsize=(10, 6))
    plt.plot(range(0, 101, 10), onze_recall_total1, marker='o', label='stemmer')
    plt.plot(range(0, 101, 10), onze_recall_total2, marker='o', label='nostemmer')
    plt.xlabel('Recall (%)')
    plt.ylabel('Precisão (%)')
    plt.title('Gráfico de 11 pontos de Precisão e Recall')
    plt.legend()
    plt.grid(True)
    plt.savefig("./avaliacao/11_pontos.png", dpi=300)
    bar_width = 0.35
    bar1 = np.arange(len(tabela_precisoes1.index))
    bar2 = [x + bar_width for x in bar1]
    plt.figure(figsize=(10, 6))
    plt.bar(bar1, tabela_precisoes1["precisao@5"], width=bar_width, alpha=0.7, label='Precision@5 stemmer')
    plt.bar(bar2, tabela_precisoes2["precisao@5"], width=bar_width, alpha=0.7, label='Precision@5 nostemmer')
    plt.bar(bar1, tabela_precisoes1["precisao@10"], width=bar_width, alpha=0.7, label='Precision@10 stemmer')
    plt.bar(bar2, tabela_precisoes2["precisao@10"], width=bar_width, alpha=0.7, label='Precision@10 nostemmer')
    plt.xlabel('Consultas')
    plt.ylabel('Precisão')
    plt.title('Precision@5 e Precision@10')
    plt.legend()
    plt.grid(True)
    plt.savefig("./avaliacao/precision5_precision10.png", dpi=300)
    plt.figure(figsize=(10, 6))
    plt.hist(r_precisao1, bins=10, alpha=0.7, label='R-Precision stemmer')
    plt.hist(r_precisao2, bins=10, alpha=0.7, label='R-Precision nostemmer')
    plt.xlabel('R-Precision')
    plt.ylabel('Frequência')
    plt.title('Histograma de R-Precision')
    plt.legend()
    plt.savefig("./avaliacao/r_precision.png", dpi=300)
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 11), [dcg / 100 for dcg in media_dcg1], marker='o', label='stemmer')
    plt.plot(range(1, 11), [dcg / 100 for dcg in media_dcg2], marker='o', label='nostemmer')
    plt.xlabel('Ranking')
    plt.ylabel('DCG Médio')
    plt.title('Discounted Cumulative Gain (médio)')
    plt.legend()
    plt.grid(True)
    plt.savefig("./avaliacao/discounted_cumulative.png", dpi=300)
    idcg = [1.0 / math.log(i + 2, 2) for i in range(10)]
    idcg = sum(idcg)
    ndcg1 = [dcg / idcg for dcg in media_dcg1]
    ndcg2 = [dcg / idcg for dcg in media_dcg2]
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 11), ndcg1, marker='o', label='stemmer')
    plt.plot(range(1, 11), ndcg2, marker='o', label='nostemmer')
    plt.xlabel('Ranking')
    plt.ylabel('NDCG')
    plt.title('Normalized Discounted Cumulative Gain')
    plt.legend()
    plt.grid(True)
    plt.savefig("./avaliacao/normalized_discounted_cumulative_gain.png", dpi=300)
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, len(f1_scores1) + 1), f1_scores1, marker='o', linestyle='-', label='stemmer')
    plt.plot(range(1, len(f1_scores2) + 1), f1_scores2, marker='o', linestyle='-', label='nostemmer')
    plt.title('F1 Score for each Query')
    plt.xlabel('Query Number')
    plt.ylabel('F1 Score')
    plt.legend()
    plt.savefig("./avaliacao/f_1_score.png", dpi=300)

def main():
    dic_esperados1 = ler_arquivo_esperado(r'./results/esperados.csv')
    dic_resultados1 = ler_arquivo_resultados(r'./results/resultados-stemmer.csv')
    dic_resultados2 = ler_arquivo_resultados(r'./results/resultados-nostemmer.csv')
    tabela_precisoes1, media_media_precisao1, media_rr1, media_dcg1, onze_recall_total1, r_precisao1 = calcular_precisao_recall(dic_esperados1, dic_resultados1)
    tabela_precisoes2, media_media_precisao2, media_rr2, media_dcg2, onze_recall_total2, r_precisao2 = calcular_precisao_recall(dic_esperados1, dic_resultados2)
    f1_scores1 = calcular_f1_score(dic_esperados1, dic_resultados1)
    f1_scores2 = calcular_f1_score(dic_esperados1, dic_resultados2)
    gerar_graficos(tabela_precisoes1, tabela_precisoes2, media_dcg1, media_dcg2, onze_recall_total1, onze_recall_total2, r_precisao1, r_precisao2, f1_scores1, f1_scores2)
    tabela_map_mrr1 = pd.DataFrame(data=[[media_media_precisao1, media_rr1]], index=["valores"], columns=["map", "mrr"])
    tabela_map_mrr2 = pd.DataFrame(data=[[media_media_precisao2, media_rr2]], index=["valores"], columns=["map", "mrr"])
    tabela_precisoes1.to_csv("./avaliacao/precisoes-stemmer.csv", sep=';', encoding='utf-8')
    tabela_precisoes2.to_csv("./avaliacao/precisoes-nostemmer.csv", sep=';', encoding='utf-8')
    tabela_map_mrr1.to_csv("./avaliacao/map_mrr-stemmer.csv", sep=';', encoding='utf-8')
    tabela_map_mrr2.to_csv("./avaliacao/map_mrr-nostemmer.csv", sep=';', encoding='utf-8')

if __name__ == '__main__':
    main()