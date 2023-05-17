import processador
import indexador
import gerador
import buscador

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
