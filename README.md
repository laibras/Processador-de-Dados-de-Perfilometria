# Processador de Dados de Perfilometria e Visualizador 3D

Este projeto contém um conjunto de scripts em Python para automatizar o processamento de dados brutos de perfilometria gerados pelo LabVIEW (arquivos `.lvm`) e para visualizar os dados processados em um gráfico 3D interativo.

## Descrição

O fluxo de trabalho é dividido em duas etapas principais:

1.  **Processamento:** Um script lê múltiplos pares de arquivos de medição (`_front.lvm` e `_back.lvm`), interpreta os dados para separar perfis sequenciais com base na direção do movimento do sensor (coordenada `y`) e consolida os pontos (`x, y, z`) em arquivos de valores separados por vírgula (`.csv`).
2.  **Visualização:** Um segundo script lê um dos arquivos `.csv` gerados e plota os dados em um gráfico de dispersão 3D, permitindo a exploração interativa (zoom, rotação) da nuvem de pontos.

## Funcionalidades

  - **Processamento em Lote:** Processa automaticamente todos os pares de arquivos `.lvm` dentro de uma pasta especificada.
  - **Lógica de Detecção de Perfil:** Identifica o início de um novo perfil medido analisando a inversão da direção da coordenada `y`.
  - **Exportação para CSV:** Salva os dados limpos e organizados (`x, y, z`) em um formato `.csv` universal.
  - **Visualização 3D Interativa:** Permite a análise visual e a exploração dos dados medidos em um ambiente 3D.

## Pré-requisitos

Para executar os scripts, você precisará ter o Python 3 instalado, juntamente com as seguintes bibliotecas:

  - pandas
  - matplotlib
  - scipy

Você pode instalar todas as dependências com um único comando:

```bash
pip install pandas matplotlib scipy
```

## Como Usar

### 1\. Processando os Arquivos `.lvm` (csv-converter-batch)

Este script consolida os dados brutos em arquivos `.csv` prontos para análise.

1.  **Organize seus arquivos:** Coloque todos os seus arquivos de medição em uma única pasta. O script espera que os arquivos sigam o padrão de nomenclatura de pares, como `ensaio1_front.lvm` e `ensaio1_back.lvm`.
2.  **Execute o script de processamento:** Rode o script `csv-converter-batch.py` a partir do seu terminal.
    ```bash
    csv-converter-batch.py
    ```
3.  **Forneça o caminho:** O programa solicitará que você insira o caminho para a pasta onde os arquivos `.lvm` estão localizados.
4.  **Verifique a saída:** Para cada par de arquivos (`ensaio1_front.lvm`, `ensaio1_back.lvm`), um novo arquivo chamado `ensaio1_perfis.csv` será gerado e salvo na mesma pasta.

### 2\. Visualizando os Dados em 3D (csv-visual-point)

Este script usa os arquivos `.csv` gerados na etapa anterior para criar uma visualização.

1.  **Execute o script de visualização:** Rode o script `csv-visual-point.py` a partir do seu terminal.
    ```bash
    python csv-visual-point.py
    ```
2.  **Forneça o caminho:** O programa solicitará que você insira o caminho completo para o arquivo `.csv` que deseja visualizar (por exemplo, `C:\Users\...\ensaio1_perfis.csv`).
3.  **Explore o gráfico:** Uma janela interativa aparecerá exibindo o gráfico 3D. Use o mouse para girar, o botão direito (ou scroll) para aplicar zoom e explorar sua nuvem de pontos. Feche a janela para encerrar o programa.

## Estrutura dos Arquivos

```
/seu-projeto/
|
|-- exemplo   #Pasta com arquivo LVM para teste
|-- csv-converter-batch.py     # Script para processar os arquivos LVM em lote
|-- csv-visual-point.py # Script para gerar o gráfico 3D interativo
|-- README.md                         # Este arquivo
|
|-- /pasta-de-dados/                  # Exemplo de pasta com seus dados
|   |-- ensaio1_front.lvm
|   |-- ensaio1_back.lvm
|   |-- ensaio2_front.lvm
|   |-- ensaio2_back.lvm
|   |-- ensaio1_perfis.csv            # (Arquivo de saída gerado pelo processador)
|   |-- ...
```

## Autor

Jose Roberto

## Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

-----
