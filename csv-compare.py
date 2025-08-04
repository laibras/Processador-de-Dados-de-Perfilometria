import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.stats import skew, kurtosis

def load_and_trim_data(filepath, border_percentage=0.10):
    """
    Carrega um arquivo CSV, remove uma porcentagem das bordas e retorna um DataFrame.
    """
    if not os.path.exists(filepath):
        print(f"  Aviso: Arquivo não encontrado {filepath}")
        return None
        
    df = pd.read_csv(filepath, sep=';')
    
    # Calcula os limites para x e y
    x_min, x_max = df['x'].min(), df['x'].max()
    y_min, y_max = df['y'].min(), df['y'].max()
    
    x_border = (x_max - x_min) * border_percentage
    y_border = (y_max - y_min) * border_percentage
    
    # Filtra o DataFrame, mantendo apenas a área central
    df_trimmed = df[
        (df['x'] >= x_min + x_border) & (df['x'] <= x_max - x_border) &
        (df['y'] >= y_min + y_border) & (df['y'] <= y_max - y_border)
    ]
    
    return df_trimmed

def calculate_surface_parameters(df):
    """
    Calcula os parâmetros de rugosidade 3D de um DataFrame de pontos (x, y, z).
    """
    if df is None or df.empty:
        return None

    points = df[['x', 'y', 'z']].values
    
    # Ajusta um plano aos dados (detrend) para remover a forma/inclinação
    # z = ax + by + c => A*C = z
    A = np.c_[points[:, 0], points[:, 1], np.ones(points.shape[0])]
    C, _, _, _ = np.linalg.lstsq(A, points[:, 2], rcond=None)
    
    # Calcula a diferença entre o z real e o z do plano (resíduos)
    z_plane = A @ C
    residuals = points[:, 2] - z_plane
    
    # Calcula os parâmetros de rugosidade 3D (análogos a Ra, Rq, etc.)
    Sa = np.mean(np.abs(residuals))
    Sq = np.sqrt(np.mean(residuals**2))
    Sp = np.max(residuals)
    Sv = np.min(residuals)
    Sz = Sp - Sv 
    
    # Skewness (Ssk) e Kurtosis (Sku)
    Ssk = skew(residuals)
    Sku = kurtosis(residuals, fisher=False) # Kurtosis padrão (não excesso)

    return {
        'Sa (µm)': Sa,
        'Sq (µm)': Sq,
        'Sz (µm)': Sz,
        'Ssk': Ssk,
        'Sku': Sku
    }

def main():
    """
    Função principal para orquestrar a análise comparativa.
    """
    folder_path = input("Por favor, insira o caminho para a pasta com os arquivos CSV: ")

    if not os.path.isdir(folder_path):
        print(f"Erro: O caminho '{folder_path}' não é um diretório válido.")
        return

    # Mapeia identificadores nos nomes dos arquivos para nomes legíveis
    file_map = {
        '50_01': 'V50_P0.01',
        '50_02': 'V50_P0.02',
        '100_01': 'V100_P0.01',
        '100_02': 'V100_P0.02'
    }

    all_files = os.listdir(folder_path)
    results = []

    print("\nIniciando análise...")
    for key, name in file_map.items():
        # Encontra o arquivo CSV correspondente
        target_file = next((f for f in all_files if key in f and f.endswith('.csv')), None)
        
        if target_file:
            print(f"Processando amostra: {name} (arquivo: {target_file})")
            filepath = os.path.join(folder_path, target_file)
            
            # Carrega e remove as bordas dos dados
            df_trimmed = load_and_trim_data(filepath)
            
            # Calcula os parâmetros
            params = calculate_surface_parameters(df_trimmed)
            
            if params:
                params['Amostra'] = name
                results.append(params)
        else:
            print(f"Aviso: Não foi encontrado um arquivo CSV para a condição '{key}'")

    if not results:
        print("\nNenhum resultado foi gerado. Verifique se os arquivos CSV estão na pasta.")
        return
        
    # Cria e exibe a tabela comparativa
    df_results = pd.DataFrame(results).set_index('Amostra')
    print("\n--- Tabela de Resultados Comparativos ---")
    print(df_results.to_string(float_format="%.4f"))

    # Gera e salva os gráficos comparativos
    print("\nGerando gráficos comparativos...")
    try:
        # Gráfico para Sa
        plt.figure(figsize=(10, 6))
        df_results['Sa (µm)'].plot(kind='bar', color=['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78'])
        plt.title('Comparação de Rugosidade Média (Sa)')
        plt.ylabel('Sa (µm)')
        plt.xlabel('Condição de Teste (Velocidade_Passo)')
        plt.xticks(rotation=0)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        sa_path = os.path.join(folder_path, 'comparacao_Sa.png')
        plt.savefig(sa_path)
        plt.close()

        # Gráfico para Sq
        plt.figure(figsize=(10, 6))
        df_results['Sq (µm)'].plot(kind='bar', color=['#2ca02c', '#98df8a', '#d62728', '#ff9896'])
        plt.title('Comparação de Rugosidade RMS (Sq)')
        plt.ylabel('Sq (µm)')
        plt.xlabel('Condição de Teste (Velocidade_Passo)')
        plt.xticks(rotation=0)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        sq_path = os.path.join(folder_path, 'comparacao_Sq.png')
        plt.savefig(sq_path)
        plt.close()
        
        print(f"Gráficos salvos em '{folder_path}'")
    except Exception as e:
        print(f"Ocorreu um erro ao gerar os gráficos: {e}")


if __name__ == "__main__":
    main()