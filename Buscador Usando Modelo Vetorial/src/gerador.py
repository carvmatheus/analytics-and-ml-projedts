import os
import re
import csv
import logging
from xml.etree import ElementTree as ET
from pathlib import Path
from collections import defaultdict

ARQUIVO_CONFIG = "gli.cfg"


def executando_no_notebook() -> bool:
    try:
        from IPython import get_ipython
        if "IPKernelApp" not in get_ipython().config:
            return False
        return True
    except (NameError, ImportError):
        return False


import logging
import os


def configurar_registro() -> logging.Logger:
    """
    Creates a logger instance for logging messages to a file.

    Returns:
        logging.Logger: The logger instance.
    """
    # Ensure the logs and results directories exist
    os.makedirs("logs", exist_ok=True)
    os.makedirs("results", exist_ok=True)

    # Create and configure the logger
    registrador = logging.getLogger('gerador')
    registrador.setLevel(logging.INFO)

    formatador = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    manipulador = logging.FileHandler("logs/gerador.log", encoding="utf-8")
    manipulador.setFormatter(formatador)
    registrador.addHandler(manipulador)

    return registrador


def ler_configuracao(arquivo_conf):
    """
    Read a configuration file and yield instructions and file names.

    Args:
        arquivo_conf (str): The name of the configuration file.

    Yields:
        tuple: A tuple of (instruction, file name) pairs.
    """
    with open(f"config/{arquivo_conf}") as arquivo_config:
        for linha in arquivo_config:
            linha = linha.rstrip()
            instrucao, nome_arquivo = linha.split("=")
            yield instrucao, nome_arquivo


def processar_arquivo_xml(nome_arquivo):
    """
    Processa um arquivo XML e retorna um gerador que produz tuplas contendo o número de registro e uma lista
    de palavras extraídas do elemento "ABSTRACT" ou "EXTRACT" de cada registro.

    :param nome_arquivo: O nome do arquivo XML a ser processado.
    :return: Um gerador que produz tuplas contendo o número de registro e uma lista de palavras.
    """
    with open(nome_arquivo) as arquivo_xml:
        arvore = ET.parse(arquivo_xml)
        raiz = arvore.getroot()

        for registro in raiz:
            num_registro = registro.find("RECORDNUM").text
            elem_texto = registro.find("ABSTRACT") or registro.find("EXTRACT")

            if elem_texto is not None:
                palavras = re.sub("[^a-zA-Z]", " ", elem_texto.text).split()
                yield num_registro, palavras


def ler(nome_arquivo):
    """
    Ler arquivo XML e processá-lo para retornar um dicionário de palavras e
    o número de registro em que aparecem.

    Args:
        nome_arquivo (str): Nome do arquivo a ser lido.

    Returns:
        Tuple[str, Dict[str, List[int]]]: Tupla contendo o nome do arquivo e
        o dicionário de palavras e registros.

    Raises:
        FileNotFoundError: Caso o arquivo não seja encontrado.
        ValueError: Caso o arquivo esteja vazio.
    """
    registrador = configurar_registro()
    registrador.info(f"Executando {nome_arquivo}")

    dicionario_gli = defaultdict(list)
    for instrucao, nome_arquivo in ler_configuracao(ARQUIVO_CONFIG):
        if instrucao == "LEIA":
            registrador.info(f"Processando {nome_arquivo}")
            for num_registro, palavras in processar_arquivo_xml(nome_arquivo):
                for palavra in palavras:
                    dicionario_gli[palavra].append(num_registro)
        elif instrucao == "ESCREVA":
            return nome_arquivo, dicionario_gli
        else:
            registrador.error(f"Erro ao ler {ARQUIVO_CONFIG}")


def escrever(nome_arquivo, dicionario_gli):
    """
    Write a dictionary to a CSV file.

    Args:
        nome_arquivo: The name of the output CSV file.
        dicionario_gli: A dictionary with string keys and integer values.
    """
    registrador = configurar_registro()
    with open(nome_arquivo, "w", newline="") as arquivo_csv:
        registrador.info(f"Abrindo {nome_arquivo}")

        escritor = csv.writer(arquivo_csv, delimiter=";")
        escritor.writerow(["Palavra", "Documentos"])

        linhas_escritas = 0
        for chave, valor in sorted(dicionario_gli.items()):
            escritor.writerow([chave, valor])
            linhas_escritas += 1

        registrador.info(f"{linhas_escritas} linhas escritas em {nome_arquivo}")
        registrador.info(f"Fechando {nome_arquivo}")


def main():
    logger = configurar_registro()
    if executando_no_notebook():
        caminho_arquivo = Path.cwd()
    else:
        caminho_arquivo = Path(__file__).parent.resolve()
    logger.info('Inicializando gerador de busca...')

    nome_arquivo, dicionario_gli = ler(nome_arquivo=caminho_arquivo)
    logger.info(f'Leitura do arquivo de configuração: {caminho_arquivo} com sucesso...')
    escrever('./results/inverted_list.csv', dicionario_gli)
    logger.info(f'Lista Invertida salva em ./results/inverted_list.csv com sucesso...')

if __name__ == "__main__":
    main()

