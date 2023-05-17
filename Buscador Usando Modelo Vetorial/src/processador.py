import os, re, csv, logging
from xml.etree import ElementTree as ET
from pathlib import Path

ARQUIVO_CONFIG = "pc.cfg"

def executando_no_notebook() -> bool:
    """
    Retorna True se o código estiver sendo executado em um Jupyter notebook ou similar.
    Caso contrário, retorna False.
    """
    try:
        from IPython import get_ipython
        if "IPKernelApp" not in get_ipython().config:
            return False
        return True
    except (NameError, ImportError):
        return False

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
    registrador = logging.getLogger(__name__)

    # Configura o registrador para nível de informação
    registrador.setLevel(logging.INFO)

    # Formata a mensagem de log
    formatador = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Cria um arquivo de log
    manipulador = logging.FileHandler("logs/processador.log", encoding="utf-8")

    # Configura o manipulador
    manipulador.setFormatter(formatador)
    registrador.addHandler(manipulador)

    return registrador

from pathlib import Path

def parse_arquivo_config(arquivo_config: Path) -> dict:
    """
    Parse a configuration file and return a dictionary of the contents.

    Args:
        arquivo_config (Path): The path to the configuration file.

    Returns:
        dict: A dictionary of the configuration file contents, where each key
        is an instruction and each value is the corresponding file name.
    """
    # Initialize an empty dictionary to store the configuration file contents.
    config = {}

    # Open the configuration file.
    with arquivo_config.open() as f:
        for linha in f:
            linha = linha.rstrip()
            instrucao, nome_arquivo = linha.split('=')
            config[instrucao] = nome_arquivo
    return config


def processar_arquivo_xml(arquivo_leia: Path, arquivo_consultas: Path, arquivo_esperados: Path, logger: logging.Logger):
    """
    Processa um arquivo XML com consultas para o formato necessário para o sistema.

    :param arquivo_leia: O arquivo XML com as consultas.
    :param arquivo_consultas: O arquivo CSV a ser gerado com as consultas processadas.
    :param arquivo_esperados: O arquivo CSV a ser gerado com os resultados esperados das consultas.
    :param logger: O objeto logger para registrar as informações de progresso.
    """
    with arquivo_leia.open() as leia_f, arquivo_consultas.open("w", newline='') as consultas_f, arquivo_esperados.open("w", newline='') as esperados_f:
        logger.info(f"Abrindo {arquivo_leia}, {arquivo_consultas} e {arquivo_esperados}")
        arvore = ET.parse(leia_f)
        raiz = arvore.getroot()

        escritor_consultas = csv.writer(consultas_f, delimiter=";")
        escritor_consultas.writerow(["QueryNumber", "QueryText"])

        escritor_esperados = csv.writer(esperados_f, delimiter=";")
        escritor_esperados.writerow(["QueryNumber", "DocNumber", "DocVotes"])

        consultas_lidas = 0
        linhas_escritas_consultas = 0
        linhas_escritas_esperados = 0

        for consulta in raiz:
            consultas_lidas += 1
            linhas_escritas_consultas += 1
            
            numero_consulta = consulta.find("QueryNumber")
            texto_consulta = consulta.find("QueryText")
            texto_processado = re.sub('[^a-zA-Z]', ' ', texto_consulta.text)
            escritor_consultas.writerow([numero_consulta.text, texto_processado.upper()])
            registros = consulta.find("Records")
            for item in registros:
                linhas_escritas_esperados += 1
                pontuacao = item.attrib['score']
                s = sum(1 for x in pontuacao if x != "0")
                escritor_esperados.writerow([numero_consulta.text, item.text, s])

        logger.info(f"{consultas_lidas} consultas processadas de {arquivo_leia}")
        logger.info(f"{linhas_escritas_consultas} linhas escritas em {arquivo_consultas}")
        logger.info(f"{linhas_escritas_esperados} linhas escritas em {arquivo_esperados}")
        logger.info(f"Fechando {arquivo_leia}, {arquivo_consultas} e {arquivo_esperados}")

def main():
    logger = configurar_registro()

    if executando_no_notebook():
        nome_arquivo = Path.cwd()
    else:
        nome_arquivo = Path(__file__).parent.resolve()

    logger.info(f'Executando {nome_arquivo}')

    caminho_config = nome_arquivo / "config" / ARQUIVO_CONFIG
    logger.info(f'Abrindo {caminho_config}')
    
    config = parse_arquivo_config(caminho_config)

    arquivo_leia = nome_arquivo / config["LEIA"]
    arquivo_consultas = nome_arquivo / config["CONSULTAS"]
    arquivo_esperados = nome_arquivo / config["ESPERADOS"]

    processar_arquivo_xml(arquivo_leia, arquivo_consultas, arquivo_esperados, logger)

# if __name__ == "__main__":
#     main()