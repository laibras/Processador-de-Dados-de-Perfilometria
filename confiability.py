import pandas as pd
import numpy as np
import os

def analisar_confiabilidade_from_csv(filepath):
    """
    Lê um arquivo CSV consolidado e analisa os resultados para determinar
    o protocolo de medição mais confiável e consistente.
    """
    if not os.path.exists(filepath):
        print(f"Erro: O arquivo '{filepath}' não foi encontrado no diretório.")
        print("Por favor, certifique-se de que o script está na mesma pasta que o CSV.")
        return

    print(f"Lendo dados do arquivo: '{filepath}'...")
    
    # --- LEITURA E PREPARAÇÃO DOS DADOS ---
    try:
        # Lê o CSV. O skipinitialspace=True ajuda a lidar com espaços após a vírgula.
        df = pd.read_csv(filepath, sep=',', skipinitialspace=True)
        # Remove espaços extras dos nomes das colunas para garantir consistência
        df.columns = df.columns.str.strip()
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        return

    # 1. Cria colunas separadas para 'Sample_ID' e 'Protocolo'
    # para permitir o agrupamento correto dos dados.
    try:
        parts = df['Amostra'].str.split('_', expand=True)
        df['Sample_ID'] = parts[0]
        df['Protocolo'] = 'V' + parts[1] + '_P' + parts[2]
    except Exception as e:
        print(f"Erro ao processar a coluna 'Amostra': {e}")
        print("Verifique se os valores na coluna 'Amostra' seguem o padrão 'nome_velocidade_passo'.")
        return

    # Renomeia as colunas para remover caracteres especiais e garantir compatibilidade
    df.rename(columns={'Sa (µm)': 'Sa', 'Sq (µm)': 'Sq', 'Sz (µm)': 'Sz'}, inplace=True)
        
    # --- CÁLCULO DA CONFIABILIDADE ---
    
    # 2. Calcula a mediana ('valor de consenso') para Sa e Sz para cada amostra
    df['Sa_consenso'] = df.groupby('Sample_ID')['Sa'].transform('median')
    df['Sq_consenso'] = df.groupby('Sample_ID')['Sq'].transform('median')
    df['Sz_consenso'] = df.groupby('Sample_ID')['Sz'].transform('median')
    df['Ssk_consenso'] = df.groupby('Sample_ID')['Ssk'].transform('median')
    df['Sku_consenso'] = df.groupby('Sample_ID')['Sku'].transform('median')
    # 3. Calcula o desvio percentual de cada medição em relação ao consenso
    df['Sa_desvio_%'] = np.abs((df['Sa'] - df['Sa_consenso']) / df['Sa_consenso']) * 100
    df['Sq_desvio_%'] = np.abs((df['Sq'] - df['Sq_consenso']) / df['Sq_consenso']) * 100
    df['Sz_desvio_%'] = np.abs((df['Sz'] - df['Sz_consenso']) / df['Sz_consenso']) * 100
    df['Ssk_desvio_%'] = np.abs((df['Ssk'] - df['Ssk_consenso']) / df['Ssk_consenso']) * 100
    df['Sku_desvio_%'] = np.abs((df['Sku'] - df['Sku_consenso']) / df['Sku_consenso']) * 100
    # 4. Calcula o 'Índice de Instabilidade' médio para cada protocolo
    scores = df.groupby('Protocolo')[['Sa_desvio_%', 'Sq_desvio_%','Sz_desvio_%','Ssk_desvio_%','Sku_desvio_%']].mean()
    scores.rename(columns={
        'Sa_desvio_%': 'Instabilidade Sa (%)',
        'Sq_desvio_%':'Instabilidade Sq (%)',
        'Sz_desvio_%': 'Instabilidade Sz (%)',
        'Ssk_desvio_%': 'Instabilidade Ssk (%)',
        'Sku_desvio_%': 'Instabilidade Sku (%)'
    }, inplace=True)

    # 5. Adiciona uma pontuação geral e ordena os resultados
    scores['Instabilidade Geral (Média)'] = scores.mean(axis=1)
    scores = scores.sort_values(by='Instabilidade Geral (Média)')
    
    # --- SAÍDA ---
    
    print("\n--- Ranking de Confiabilidade dos Protocolos de Medição ---")
    print(f"Baseado na análise de {df['Sample_ID'].nunique()} amostras distintas do arquivo CSV.\n")
    print("Lembrete: Quanto menor o 'Índice de Instabilidade', mais confiável é o método.\n")
    print(scores.to_string(float_format="%.2f"))
    
    best_protocol = scores.index[0]
    print(f"\nConclusão: O protocolo '{best_protocol}' demonstrou ser o mais confiável e consistente em geral.")


# --- Início da Execução Principal ---
if __name__ == "__main__":
    # O nome do arquivo CSV a ser lido no mesmo diretório do script
    csv_filename = 'resultado.csv'
    analisar_confiabilidade_from_csv(csv_filename)