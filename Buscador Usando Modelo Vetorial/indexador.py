import math, os, csv, ast
import logging

# Configurações do indexador
tf_norm = True  # Normalizar o tf
idf_smooth = 1.0  # Valor do smoothing do idf



def configurar_registro() -> logging.Logger:
    """
    Cria uma instância de registrador (logger) para registrar mensagens em um arquivo.

    Retorna:
        logging.Logger: A instância do registrador (logger).
    """
    # Garante que os diretórios de logs e resultados existam
    os.makedirs("logs", exist_ok=True)
    os.makedirs("results", exist_ok=True)

    # Cria e configura o registrador (logger)
    registrador = logging.getLogger('indexador')

    # Configura o registrador para nível de informação
    registrador.setLevel(logging.INFO)

    # Formata a mensagem de log
    formatador = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Cria um arquivo de log
    manipulador = logging.FileHandler("logs/indexador.log", encoding="utf-8")

    # Configura o manipulador
    manipulador.setFormatter(formatador)
    registrador.addHandler(manipulador)

    return registrador


def read_config_file(filename):
    with open(filename, 'r') as f:
        leia = ''
        escreva = ''
        for line in f:
            if line.startswith('LEIA='):
                leia = line.strip()[5:]
            elif line.startswith('ESCREVA='):
                escreva = line.strip()[8:]
    return leia, escreva

def process_csv_file(filename):
    num_words_list = []
    lista_final = []
    vocab = 0
    with open(filename, newline='\n') as arquivo_csv:
        leitor = csv.reader(arquivo_csv, delimiter=";")
        next(leitor)
        for linha in leitor:
            lista = ast.literal_eval(linha[1])
            vocab += 1
            for elemento in lista:
                while int(elemento) > len(lista_final):
                    lista_final.append(0)
                lista_final[int(elemento) - 1] += 1
    return lista_final

def read_inverted_list(filename):
    lista_invertida = {}
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)
        for row in reader:
            palavra = row[0]
            documentos = eval(row[1].replace(' ', ''))
            lista_invertida[palavra] = documentos
    return lista_invertida

def calculate_tfidf(lista_invertida):
    tf_max = {}
    for palavra, documentos in lista_invertida.items():
        tf_max[palavra] = max([documentos.count(doc) for doc in set(documentos)])

    N = len(set([doc.strip() for documentos in lista_invertida.values() for doc in documentos])) # número de documentos na coleção
    idf = {}
    for palavra, documentos in lista_invertida.items():
        n = len(set(documentos)) # número de documentos em que a palavra aparece
        idf[palavra] = math.log(N / n)

    tfidf = {}
    for palavra, documentos in lista_invertida.items():
        tfidf[palavra] = []
        for doc in set(documentos):
            tf = documentos.count(doc) / tf_max[palavra]
            tfidf[palavra].append((doc, tf * idf[palavra]))
    return tfidf

def write_model_file(filename, tfidf):
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Word', 'DocNumber', 'Weight'])
        for word, doc_info_list in tfidf.items():
            for doc_info in doc_info_list:
                doc_number = doc_info[0]
                weight = doc_info[1]
                writer.writerow([word, doc_number, weight])

def main():
    logger = configurar_registro()
    logger.info('Iniciando indexador...')

    leia, escreva = read_config_file('config/index.cfg')
    logger.info('Arquivo de configuração config/index.cfg carregado com sucesso!')
        
    lista_final = process_csv_file(leia)
    logger.info(f'{leia} processado com sucesso')
    lista_invertida = read_inverted_list('results/inverted_list.csv')
    logger.info('Lista invertida carregada com sucesso')
    tfidf = calculate_tfidf(lista_invertida)
    write_model_file(r'results/modelo.csv', tfidf)
    logger.info(f'Modelo escrito com sucesso no arquivo {escreva}')

if __name__ == "__main__":
    main()
