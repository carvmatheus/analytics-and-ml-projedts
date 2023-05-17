# Implementação de Um Sistema de Recuperação em Memória Segundo o Modelo Vetorial

Este projeto é uma coleção de módulos Python independentes que são orquestrados para rodar em uma sequência específica. A ordem de execução dos módulos é a seguinte:

1. Processador
2. Indexador
3. Gerador
4. Buscador

Cada módulo é um arquivo .py separado que está localizado na mesma raiz do projeto. Cada módulo possui uma função `main()` que serve como ponto de entrada para a execução do módulo.

## Orquestração dos Módulos

A orquestração dos módulos é feita através de um script Python separado chamado `main.py`. Este script importa cada um dos módulos e chama a função `main()` de cada módulo na ordem desejada.

Aqui está o código do script `main.py`:

```python
import src.processador as processador
import src.indexador as indexador
import src.gerador as gerador
import src.buscador as buscador

def main():
    print("Iniciando o processador...")
    processador.main()
    print("Processador concluído.")

    print("Iniciando o indexador...")
    indexador.main()
    print("Indexador concluído.")

    print("Iniciando o gerador...")
    gerador.main()
    print("Gerador concluído.")

    print("Iniciando o buscador...")
    buscador.main()
    print("Buscador concluído.")

if __name__ == "__main__":
    main()
```

## Pastas
`SRC` -> Todos os arquivos necessários para rodar o código estão na pasta.  
`LOGS` -> Os logs são dividos por módulos para facilitar a compreensão da execução.  
`RESULTS`-> Contém os arquivos resultados da execução dos módulos  
`CONFIG` -> Contém os arquivos de configuração para que os módulos rodem corretamente com instruções.  

## Como rodar?
Para executar o código completo, precisa clonar o repositório como todo.
Depois é somente executar o comando `python3 main.py` na raiz do projeto.
