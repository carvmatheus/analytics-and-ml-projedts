import os
import re
import csv
import logging
import xml.etree.ElementTree as ET


os.makedirs('logs', exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('logs/processador.log', encoding='utf-8')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

def processador():
    logger.info(f'Executando Processador')
    conf_file = "pc.cfg"
    stem = False

    with open(f"config/{conf_file}") as config_file:
        logger.info(f'Abrindo {conf_file}')

        for line in config_file:
            line = line.rstrip()

            if line == "STEMMER":
                logger.info("Escolhida a configuração de fazer stemming das consultas")
                from nltk.stem import PorterStemmer
                ps = PorterStemmer()
                stem = True
                continue
            elif line == "NOSTEMMER":
                logger.info("Escolhida a configuração de não fazer stemming das consultas")
                stem = False
                continue

            instruct, filename = line.split('=')

            if instruct == "LEIA":
                leia = filename
            elif instruct == "CONSULTAS":
                consultas = filename
            elif instruct == "ESPERADOS":
                esperados = filename
            else:
                logger.error(f'Erro ao ler {conf_file}')
        
    with open(leia) as xml_file, \
        open(consultas, "w", newline='') as consulta_f, \
        open(esperados, "w", newline='') as esperado_f:
        logger.info(f"Abrindo {leia}, {consultas} e {esperados}")
        tree = ET.parse(xml_file)
        root = tree.getroot()

        consulta_w = csv.writer(consulta_f, delimiter=";")
        consulta_w.writerow(["QueryNumber", "QueryText"])
        
        esperado_w = csv.writer(esperado_f, delimiter=";")
        esperado_w.writerow(["QueryNumber", "DocNumber", "DocVotes"])
        
        lines_read = 0
        lines_written_consulta = 0
        lines_written_esperado = 0

        for query in root:
            lines_read += 1
            lines_written_consulta += 1
            
            query_number = query.find("QueryNumber")
            query_text = query.find("QueryText")
            processed_text = re.sub('[^a-zA-Z]', ' ', query_text.text)

            if stem:
                processed_text = ' '.join(ps.stem(word) for word in processed_text.split())

            consulta_w.writerow([query_number.text, processed_text.upper()])
            
            records = query.find("Records")
            for item in records:
                lines_written_esperado += 1
                score = item.attrib['score']
                
                s = 0
                for x in score:
                    if x != "0":
                        s += 1
                
                esperado_w.writerow([query_number.text, item.text, s])

        logger.info(f"{lines_read} consultas processadas de {leia}")
        logger.info(f"{lines_written_consulta} linhas escritas em {consultas}")
        logger.info(f"{lines_written_esperado} linhas escritas em {esperados}")
        logger.info(f"Fechando {leia}, {consultas} e {esperados}")

def main():
    processador()

if __name__ == "__main__":
    main()
