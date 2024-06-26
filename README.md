# Análise de uso de solo com Random Forest

Script em Python para classificação floresta e não floresta com um modelo treinado para 500 árvores utilizando Random Forest, com integração de geoprocessamento e banco de dados.

## Requisitos:
1. Docker;
2. Banco Postgres local;
3. GitHub;

## Estrutura do projeto:

```path
Processo_Seletivo/
│
├── data/
│   ├── Images/           
│   └── Shapefile/    
│
├── logs/    
│   └── .gitkeep
│        
├── results/
│   ├── class_areas.csv
│   ├── classification_report.png
│   ├── classification_result.shp
│   ├── classified_tiff.tif
│   ├── confusion_matrix.png
│   └── plot_map.png
│
├── models/
│   ├── train_model.py
│   └── classify_raster.py
│
├── SQL/
│   └── tables.sql
│
├── src/
│   ├── api/
│   │    ├── routers/
│   │    │    └── images.py
│   │    ├── __init__.py  
│   │    ├── crud.py  
│   │    ├── database.py  
│   │    ├── main.py
│   │    ├── models.py    
│   │    └── schemas.txt
│   ├── utils/ 
│   │    ├── data_reader.py  
│   │    ├── image_processing.py  
│   │    ├── model_training.py
│   │    ├── plotting.py
│   │    ├── result_report.py    
│   │    └── validation.txt
│   ├── __init__.py
│   └── main.py  
│
├── test_data/
│   ├── images/
│   │    ├── red.tif
│   │    ├── green.tif
│   │    └── blue.tif
│   └── shapefile/
│       └── amostra_treino.shp
│ 
├── tests/
│   ├── test_crud.py
│   ├── test_data_reader.py
│   ├── test_image_processing.py
│   ├── test_model_training.py
│   ├── test_plotting.py
│   ├── test_result_export.py
│   └── test_validation.py
│
├── .dockerignore
├── .env_example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```
### Arquivos de configuração 

Os dados de configuração mais sensíveis, como informações de banco de dados, estarão em um arquivo ".env". Na estrutura do projeto temos um ".env_example" para que fique mais fácil o preenchimento do mesmo.

```js
SERVER= seu_server
PORT= 0000
DATABASE= database_desejado
USER= user
PASSWORD= ********
```

## Iniciando o projeto:

### Docker:
Para iniciar o projeto é necessário construir o docker compose seguinto os seguintes passos:

```bash
    docker compose build
    docker compose up -u 
```           
Para verificar se o ambiente foi construido e está funcionando, basta rodar o seguinte comando:
```bash
    docker ps 
  ```

### Tabelas do banco:
É necessária a criação das tabelas e colunas no banco de dados Postgres, elas podem ser criadas rodando o seguinte comando SQL:
```sql
CREATE TABLE IF NOT EXISTS processed_images (
    id SERIAL PRIMARY KEY,
    date_processed DATE NOT NULL,
    cloud_coverage FLOAT NOT NULL,
    image_path VARCHAR(255) NOT NULL UNIQUE,
    classification_result VARCHAR(255) NOT NULL,
    evaluation_metric FLOAT NOT NULL
);
```


### FastAPI:
A API vai rodar em 'https://localhost/docs' e caso tenha necessidade de alterar a porta para a porta 81 por exemplo, basta alterar o seguinte trecho:
```python
version: "3.9"

services:
  api:
    container_name: spotsat
    build:
      context: .
      dockerfile: Dockerfile
    env_file: ".env"
    ports:
      - "81:80" <- Alterar porta
    volumes:
      - ./log:/code/log
```
**A API está documentada dentro da url fornecida**, nela contém exemplos, schemas e código dos retornos das requests. A baixo segue evidências das documentações:


1. **Interface da API:**

      ![interface_api](https://github.com/ribeirojesse/spotsat/assets/86420765/d045e558-7958-4de4-8c7a-28e490354e61)

2. **Get Image:**

      ![get_image](https://github.com/ribeirojesse/spotsat/assets/86420765/d3ef2c91-151f-478d-a7d4-982255cbf65f)

3. **Get Image by ID:**

      ![get_by_id](https://github.com/ribeirojesse/spotsat/assets/86420765/cdf1b629-c080-4280-aa2a-92cfcae05b07)

4. **Get by Atributes:**

      ![get_by_atributtes](https://github.com/ribeirojesse/spotsat/assets/86420765/ea0379b1-e3d3-4cee-a384-12aad2a01ed0)

5. **Post:**
      ![post_method](https://github.com/ribeirojesse/spotsat/assets/86420765/f11c424b-7db0-4c30-8bba-3ece851c6e16)



# Resultado dos processamentos:
Para executar o processamento, basta executar o arquivo "main.py"(src/main.py).

Os resultado serão colocados na pasta "results" da nossa estrtura de pastas que ficará da seguinte forma:
```
├── results/
│   ├── classified_raster.tif
│   ├── classified_raster.shp
│   ├── classified_raster.gpkg
│   ├── confusion_matrix.png
│   └── accuracy_metrics.txt
``` 

### *Matriz de confusão:*

![confusion_matrix](https://github.com/ribeirojesse/spotsat/assets/86420765/4f8af6d1-ad3f-429d-909a-242f4a4d41ca)


A matriz de confusão possui quatro elementos principais, distribuídos em uma tabela 2x2. Cada célula da tabela representa a quantidade de observações previstas em cada categoria, comparadas com as observações reais.

Interpretação dos Valores na Matriz
Os valores presentes na matriz de confusão são:

- Verdadeiros Negativos (VN): 53

- Falsos Positivos (FP): 13

- Falsos Negativos (FN): 0

- Verdadeiros Positivos (VP): 66

***Detalhamento dos Resultados:***

- Verdadeiros Negativos (VN - 53):  
O modelo previu corretamente 53 instâncias como negativas (classe 0) e essas instâncias são realmente negativas.

- Falsos Positivos (FP - 13):  
 O modelo previu 13 instâncias como positivas (classe 1), mas essas instâncias são realmente negativas (classe 0). Isso representa os erros onde o modelo identifica algo como positivo quando na verdade é negativo.

- Falsos Negativos (FN - 0):   
O modelo não cometeu nenhum erro ao prever instâncias que são realmente positivas como negativas. Isso significa que todas as instâncias positivas foram corretamente identificadas.

- Verdadeiros Positivos (VP - 66):   
O modelo previu corretamente 66 instâncias como positivas e essas instâncias são realmente positivas.
Métricas Derivadas

#### Conclusão:    
   A matriz de confusão mostra que o modelo tem uma boa performance, com uma acurácia de 90.15% e um F1-Score de 91.01%. O modelo apresenta uma alta sensibilidade (recall) de 100%, o que indica que ele é muito eficaz em identificar as instâncias positivas. No entanto, a precisão de 83.54% sugere que há uma certa quantidade de falsos positivos, mas ainda assim é um desempenho bastante robusto.


### *Reporte de calssificação:*
![classification_report](https://github.com/ribeirojesse/spotsat/assets/86420765/42a795d0-37a9-49de-865a-8d11b272cd95)


O relatório de classificação mostra as seguintes métricas para cada classe (0 e 1):

- Precisão (Precision)
- Recall (Sensibilidade)
- F1-Score
- Suporte (Support)

***Interpretação das Métricas:***
- **Precisão (Precision)**: A precisão é a proporção de previsões positivas corretas em relação ao total de previsões positivas. Ela indica a exatidão do modelo na previsão da classe positiva.

  - Classe 0: Precisão = 1.00
  - Classe 1: Precisão = 0.84


- Recall (Sensibilidade): O recall é a proporção de verdadeiros positivos em relação ao total de reais positivos. Ele mede a capacidade do modelo de encontrar todas as instâncias positivas.

  - Classe 0: Recall = 0.80
  - Classe 1: Recall = 1.00


- **F1-Score**: O F1-Score é a média harmônica da precisão e do recall. Ele fornece uma medida balanceada que leva em consideração tanto os falsos positivos quanto os falsos negativos.

   - Classe 0: F1-Score = 0.89
   - Classe 1: F1-Score = 0.91

- **Suporte (Support)**: O suporte é o número de ocorrências reais de cada classe no conjunto de dados.

   - Classe 0: Suporte = 66
   - Classe 1: Suporte = 66

***Detalhamento dos Resultados:***

**Classe 0:**

- Precisão de 1.00 indica que todas as previsões para a classe 0 foram corretas.
- Recall de 0.80 indica que o modelo identificou corretamente 80% das instâncias reais da classe 0.
- F1-Score de 0.89 é um valor elevado, mostrando um bom equilíbrio entre precisão e recall para a classe 0.

**Classe 1:**

- Precisão de 0.84 indica que 84% das previsões para a classe 1 foram corretas.
- Recall de 1.00 indica que o modelo identificou todas as instâncias reais da classe 1.
- F1-Score de 0.91 mostra um excelente equilíbrio entre precisão e recall para a classe 1.

#### Conclusão
Este relatório de classificação mostra que o modelo de classificação possui um desempenho robusto em ambas as classes. O modelo apresenta uma alta precisão para a classe 0 e um recall perfeito para a classe 1, indicando que ele é particularmente bom em identificar todas as instâncias positivas (classe 1) sem deixar de ser preciso para a classe negativa (classe 0). O suporte igual para ambas as classes (66) sugere que os dados estão balanceados, o que facilita a interpretação e validação das métricas.


### *Plotagem do mapa:*
![plot_map](https://github.com/ribeirojesse/spotsat/assets/86420765/6db33808-23c2-4725-9afb-2ab5704872d1)

O mapa representa diferentes tipos de uso do solo na área geográfica mostrada.

**Escala de Cores:**  
A barra de cores à direita vai de 0.0 a 1.0, representando diferentes classes ou probabilidades associadas ao uso do solo. As cores variam de roxo (0.0) a amarelo (1.0), onde geralmente:

- Valores mais baixos (próximos de 0.0) podem representar áreas de solo nu, água ou vegetação esparsa.
- Valores mais altos (próximos de 1.0) podem representar áreas de vegetação densa ou agricultura intensiva.


**Eixos:** Os eixos x e y representam as coordenadas geográficas (latitude e longitude) da área em análise.

**Interpretação do Mapa:**   

 - Área Amarela (Valor próximo de 1.0): A maior parte do mapa é amarela, indicando que a área predominante tem uma classificação de uso do solo com valor próximo de 1.0. Isso pode indicar uma área de vegetação densa, floresta ou agricultura intensiva.

- Manchas Roxas (Valor próximo de 0.0): As manchas roxas espalhadas pelo mapa representam áreas com valor de classificação de uso do solo próximo de 0.0. Essas áreas podem ser regiões urbanas, água, solo nu ou vegetação esparsa.

- Distribuição Geográfica: As manchas de uso do solo com valores diferentes estão dispersas pela área geográfica representada, mostrando a variação espacial do uso do solo.

#### Conclusão
Este mapa de classificação de uso do solo visualiza a distribuição espacial das diferentes classes de uso do solo em uma determinada região. A predominância do amarelo sugere uma cobertura maior de vegetação ou agricultura, enquanto as manchas roxas indicam áreas com uso do solo diferente, possivelmente urbanas ou de vegetação esparsa. 

### *Cálculo de áreas:*

O cáculo de área está no arquivo csv, que também será gerado na pasta results.

- Classe 0.0: A área calculada é 1.143.522.523,37 km².
- Classe 1.0: A área calculada é 11.318.699.376,53 km².

Para cada classe (0.0 e 1.0), a tabela apresenta a área correspondente, esses valores indicam a extensão espacial ocupada por cada classe.


### ***Observação:***
Os números e resultados podem sofrer alteração de acordo com os dados passados.

# Testes unitários:

Os testes unitários ficarão na seguinte estrutura de pastas e arquivos:
```
├── tests/
│   ├── test_data_reader.py
│   ├── test_image_processing.py
│   ├── test_model_training.py
│   ├── test_plotting.py
│   ├── test_result_export.py
│   └── test_validation.py
```
E serão rodados através da integração contínua (CI) utilizando GitHub Actions para automatizar a execução dos testes a cada novo commit, mas também pode ser executado através do seguinte comando que executará todos os testes:

```bash
python -m unittest discover tests
```

# Melhorias previstas:

- Salvar modelos;
- Fazer endpoint pra fazer predição de imagens;
- Fazer limitação de tamanho de imagens;
- Fazer FastAPI ser async;
- Organização por Classes;
 



