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

        Imagem aqui

2. **Exmplo de schema**

        Imagem aqui 

3. **Exemplo de retorno**

        Imagem aqui 
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


# Testes unitários:

Os testes unitários ficarão na seguinte estrutura de pastas e arquivos:
```
├── tests/
│   ├── test_crud.py
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

1.
2.
3.
4.
5. Tratamento de erros ou condições dentro das funções.



