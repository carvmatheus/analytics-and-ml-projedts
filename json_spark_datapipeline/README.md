# data-pipeline

## Objetivo
Essa sequencia de notebooks tem como objetivo descrever um pipeline de dados onde
arquivos em json são gerados com informações obtidas de crawlers.
Cada arquivo possue uma formatação e tamanho diferente.

## Implementação
Por esse motivo, foi escolhida a realização de processo de ELT dos dados. Com 
separações das informações por camadas. Onde a bronze contém o dado mais bruto,
a silver já está com os dados em formato de negócio. 
A camada analítica (ou gold) serve para a execução da extração:
1. dos top 10 produtos onde o variação do valor do fabricante com o anúncio é maior. 
2. a extração dos top 10 produtos que mais se encontram indisponíveis

## Execução.
Foi considerado para esse desenvolvimento que os notebooks estejam setados para o 
ambiente de desenvolvimento do Databricks. Foi utilizado conversão de arquivo
para Delta pois como são inúmeros pequenos arquivos, através do comando optimize
é possível agrupar os mesmos em porções maiores. Aumentando com isso a eficiencia 
nas queries.

## Composição desse repositorio
Os notebooks em pyspark estão dividos por execução
1. bronze_layer - irá ler os arquivos json, converter para delta e criar as 
manipulações necessárias para composição da tabela
2. silver_layer - irá separar a estrutura de array do json em colunas específicas 
com os dados que foram necessários para o desenvolvimento. Nessa camada foram 
definidas as tipagens 
3. analytical_layer - irá executar e imprimir os top produtos desejados.
4. utils - contendo o script necessário para descompactar os arquivos dentro da pasta

Também foi anexado uma pasta com amostragem dos arquivos que foram lidos e carregados
no databricks. Para replicação, os mesmos precisam estar dentro do diretório presente
no código.

Foi anexado um arquivo .zip com todos os dados, para facilitar a execução dos 

## Tecnologias
1. Cluster com local dbfs para alocação dos arquivos
2. ambiente serverless databricks
3. pyspark como intermediário para Spark
4. Spark.sql para consulta dos dados em bancos (facilita a compreensão e leitura)
5. Divisão do refinamento dos dados em camadas.

## Resultado
Foi possível encontrar que os seguintes produtos são os que mais estão indisponíveis (com uma validação se há ou não titulo, para pegar alguma falha na hora da criação do json)

![image](https://user-images.githubusercontent.com/100801745/223368581-8949d137-b6e0-4126-86fd-3885f70cbb19.png)

Analisando os dados de produtos com maior diferença de valor, podemos ver que temos discrepancias muito grandes.

![image](https://user-images.githubusercontent.com/100801745/223381473-4624b4a2-3691-4293-b2ca-e66fe13cf619.png)

Analisando um dos casos, foi possível verificar que o resultado estava igual a 0 para o valor da fabrica.
![image](https://user-images.githubusercontent.com/100801745/223382030-e0f4465e-ac36-4919-a271-78dbe37510b9.png)

Claramente se tratando de um erro. Ou falha na leitura, ou problema no cadastro da base.

Filtrando para valores diferentes de 0 (em ambas as variáveis), temos 
![image](https://user-images.githubusercontent.com/100801745/223380993-7ba75bb6-f05b-49e3-bb75-6ea45f2e75f7.png)

Adotando um threshold 20% do valor de retail ser maior ou igual ao de manufacturing (e vice versa)
```
df_2 = df.withColumn('diff', f.when((f.col('retailerPrice') >= f.col('manufacturerPrice')*0.2)\ 
                                    & (f.col('manufacturerPrice') >= f.col('retailerPrice')*0.2)\
                                    , (f.col('retailerPrice')) - (f.col('manufacturerPrice'))))
```
Conseguimos chegar a um resultado muito melhor

![image](https://user-images.githubusercontent.com/100801745/223383094-5e7e3c01-a3de-45f9-9a0f-77344be4f83d.png)


