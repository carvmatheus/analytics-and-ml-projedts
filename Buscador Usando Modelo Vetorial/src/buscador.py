from collections import Counter
import nltk
import logging, os

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
    registrador = logging.getLogger('buscador')

    # Configura o registrador para nível de informação
    registrador.setLevel(logging.INFO)

    # Formata a mensagem de log
    formatador = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Cria um arquivo de log
    manipulador = logging.FileHandler("logs/buscador.log", encoding="utf-8")

    # Configura o manipulador
    manipulador.setFormatter(formatador)
    registrador.addHandler(manipulador)

    return registrador


def magnitude(vector):
    return sum(value**2 for value in vector.values())**0.5

# Função para calcular o produto escalar de dois vetores
def dot_product(vector1, vector2):
    return sum(vector1.get(key, 0) * vector2.get(key, 0) for key in set(vector1) | set(vector2))

# Função para calcular a similaridade de cosseno de dois vetores
def cosine_similarity(vector1, vector2):
    magnitude_product = magnitude(vector1) * magnitude(vector2)
    if magnitude_product == 0:
        return 0
    else:
        return dot_product(vector1, vector2) / (magnitude(vector1) * magnitude(vector2))


def main():
    import csv

    logger = configurar_registro()
    logger.info('Iniciando o buscador...')
    nltk.download('stopwords')
    stop_words = [word.upper() for word in nltk.corpus.stopwords.words('english')]

    conf_file = 'busca.cfg'
    min_length = 3

    with open(f"config/{conf_file}") as config_file:
        for line in config_file:
            line = line.rstrip()

            instruct, filename = line.split('=')

            if instruct == "MODELO":
                modelo = filename
            elif instruct == "CONSULTAS":
                consultas = filename
            elif instruct == "RESULTADOS":
                oldname, extension = filename.split('.')
    matrix_dict = {}
    logger.info(f'arquivo de configuracao {conf_file} lido com sucesso')

    with open(modelo) as model_file:
            model_reader = csv.reader(model_file, delimiter=";")
            next(model_reader)
            
            for line in model_reader:
                if line[0] not in matrix_dict.keys():
                    matrix_dict[line[0]] = {int(line[1]): float(line[2])}
                else:
                    matrix_dict[line[0]][int(line[1])] = float(line[2])
    logger.info(f'Arquivo {modelo} lido com sucesso...')

    with open(consultas) as query_file:
        query_reader = csv.reader(query_file, delimiter=";")
        next(query_reader)
        q_number = 0
        line=0
        query_dict = {}
        for query in query_reader:
            query_words = query[1].split()
            words = [word for word in query_words if (len(word) >= min_length and word not in stop_words)]
            query_dict[q_number] = {word: 1 for word in words}
            q_number += 1
    logger.info(f'Foram lidos {q_number} queries com sucesso...')
    logger.info(f'Arquivo {consultas} lido com sucesso...')



    cols = sorted(set(matrix_dict.keys()))
    rows = sorted(set(row for col, rows in matrix_dict.items() for row in rows))

    # Cria a matriz como um dicionário de dicionários
    matrix = {row: {col: matrix_dict[col].get(row, 0) for col in cols} for row in rows}

    # Converte as colunas em maiúsculas
    new_matrix = {}
    for row, row_dict in matrix.items():
        new_row_dict = {}
        for col, value in row_dict.items():
            new_col = col.upper()
            new_row_dict[new_col] = value
        new_matrix[row] = new_row_dict
    matrix = new_matrix       

    # Obtém todos os documentos (chaves do dicionário)
    documents = matrix.keys()

    # Cria um novo dicionário para armazenar a matriz filtrada
    filtered_matrix = {}

    # Itera sobre cada documento na matriz
    for doc in documents:
        # Cria um novo dicionário para armazenar as colunas (palavras) filtradas para este documento
        filtered_columns = {}
        
        # Itera sobre cada coluna (palavra) da matriz original
        for word in matrix[doc]:
            # Se a palavra estiver na lista de palavras, adiciona ela e o peso para o novo dicionário
            if word in words:
                filtered_columns[word] = matrix[doc][word]
        
        # Adiciona o documento e as colunas filtradas para o novo dicionário
        filtered_matrix[doc] = filtered_columns

    # Cria um novo dicionário para armazenar a matriz filtrada
    # Cria um novo dicionário para armazenar a matriz filtrada
    filtered_matrix_new = {}

    # Loop for para filtrar as chaves que possuem algum valor maior que zero
    for doc in filtered_matrix.keys():
        if any(val > 0 for val in filtered_matrix[doc].values()):
            filtered_matrix_new[doc] = filtered_matrix[doc]


    # Calcule a magnitude para cada vetor na matriz filtrada
    magnitudes = {doc: magnitude(vector) for doc, vector in filtered_matrix_new.items()}
    # Inicialize um dicionário para armazenar os resultados
    import csv

    N = 5  # Número de documentos mais similares para retornar por consulta

    # Inicialize uma lista para armazenar os resultados
    results = []

    # Loop através de cada consulta em query_dict
    for query_number, query in query_dict.items():
        
        # Calcule a magnitude do vetor de consulta
        query_magnitude = magnitude(query)
        
        # Calcule a similaridade do cosseno para cada vetor na matriz filtrada
        cosine_similarities = {doc: cosine_similarity(vector, query) for doc, vector in filtered_matrix_new.items()}

        # Classifique os documentos por similaridade em ordem decrescente
        sorted_docs = sorted(cosine_similarities.items(), key=lambda item: item[1], reverse=True)
        
        # Pegue os top N documentos
        top_docs = sorted_docs[:N]

        # Se a similaridade for maior que zero, adicione os resultados à lista
        for rank, (doc, similarity) in enumerate(top_docs, start=1):
            if similarity > 0:
                # Transforme doc em uma string de tamanho 5
                doc_str = str(doc).zfill(5)
                results.append([f'{query_number:05}', rank, doc_str, similarity])

    # Escreva os resultados em um arquivo CSV
    with open('./results/resultados.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['QueryNumber', 'DocRanking', 'DocNumber', 'Similarity'])
        for result in results:
            writer.writerow(result)
    logger.info('Arquivo ./results/resultados.csv escrito com sucesso...')


if __name__ == '__main__':
    main()