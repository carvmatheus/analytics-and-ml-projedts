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
import processador
import indexador
import gerador
import buscador

def main():
    print("Iniciando a orquestração dos módulos...")
    processador.main()
    print("Processamento concluído.")
    indexador.main()
    print("Indexação concluída.")
    gerador.main()
    print("Geração concluída.")
    buscador.main()
    print("Busca concluída.")
    print("Todos os módulos foram executados com sucesso!")

if __name__ == "__main__":
    main()
```


