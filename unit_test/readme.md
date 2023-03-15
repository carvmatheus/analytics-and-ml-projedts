## Teste Unitário
### Resumo
Nesse repositório, temos a execução de técnica de teste unitário em da biblioteca unittest. 
Foi criada uma classe de empregados contendo informações de nome, sobre nome e salário
de cientistas de dados de uma grande coorporação.

### Objetivo
Validar que os elementos da classe estava retornando valores conforme esperados

### Resultado
Conforme resultado, executando o comando 
```
python test_employee.py
```
Obtemos o seguinte resultado
![image](https://user-images.githubusercontent.com/100801745/225204305-01e7f0be-e4a7-480f-8f6b-f1ed6d03f38b.png)
Mostrando que a validação funcionou perfeitamente, detectando anomalia de valores para o empregado número 3.
Nesse caso, era esperado o valor 4000, porém retornado (corretamente) o valor 3000

Posteriormente foi alterado o arquivo de teste e obtivemos exito no teste.
![image](https://user-images.githubusercontent.com/100801745/225204558-fd3e0555-c7ab-480e-9e8d-556888f6cc7f.png)
