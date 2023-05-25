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
        stem = False
        for line in config_file:
            line = line.rstrip()
            if line == "STEMMER":
                print(1)
                stem = True
                continue
            elif line == "NOSTEMMER":
                print(2)
                stem = False
                continue

            instruct, filename = line.split('=')

            if instruct == "MODELO":
                modelo = filename
            elif instruct == "CONSULTAS":
                consultas = filename
            elif instruct == "RESULTADOS":
                oldname, extension = filename.split('.')
                if stem:
                    resultados = oldname + "-stemmer." + extension
                else:
                    resultados = oldname + "-nostemmer." + extension
            elif instruct == "SIMILARIDADE":
                logger.info(f"Utilizando similaridade por {filename}")
                sim = filename
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

    with open(resultados, "w", newline='') as result_file:
        writer = csv.writer(result_file, delimiter=";")
        writer.writerow(["QueryNumber", "[DocRanking, DocNumber, Similarity]"])
    with open(consultas) as query_file:
        logger.info(f'Abrindo {consultas}')
        query_reader = csv.reader(query_file, delimiter=";")
        next(query_reader)
        
        query_num = 0
        result_lines = 0
        for query in query_reader:
            query_dict = {}
            
            words = query[1].split()
            words = [word for word in words if len(word) >= min_length]
            query_vec = Counter(words)
            
            for word in query_vec:
                if word in matrix_dict.keys():
                    current_dict = matrix_dict[word]
                    weight_list = []
                    for key in current_dict:
                        weight_list.append(current_dict[key])
                        if key not in query_dict:
                            query_dict[key] = current_dict[key] * query_vec[word]
                        else:
                            query_dict[key] += current_dict[key] * query_vec[word]
            
            query_num += 1
            sorted_values = sorted(query_dict.items(), key=lambda item: item[1], reverse=True)#[:100]
            
            with open(resultados, "a", newline='') as result_file:
                result_writer = csv.writer(result_file, delimiter=";")

                for i, elem in enumerate(sorted_values):
                    li = [i, elem[0], elem[1]]
                    result_writer.writerow([query[0], li])
                    result_lines += 1

        logger.info(f'{query_num} consultas processadas de {consultas}')
        logger.info(f'{result_lines} linhas escritas em {resultados}')
        logger.info(f'Fechando {consultas}')
    logger.info('Arquivo ./results/resultados_esperados.csv escrito com sucesso...')


if __name__ == '__main__':
    main()