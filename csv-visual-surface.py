import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
import os

def visualizar_mapa_de_calor_3d(csv_filepath):
    """
    Cria e salva um gráfico de superfície 3D (mapa de calor) a partir de um arquivo CSV.

    Args:
        csv_filepath (str): O caminho completo para o arquivo CSV.
    """
    # Verifica se o arquivo existe
    if not os.path.exists(csv_filepath):
        print(f"Erro: O arquivo '{csv_filepath}' não foi encontrado.")
        return

    print(f"Lendo dados de '{os.path.basename(csv_filepath)}'...")
    # Carrega os dados. Usando ';' como separador, conforme os scripts anteriores.
    try:
        df = pd.read_csv(csv_filepath, sep=';')
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        print("Certifique-se de que o arquivo está formatado corretamente com o separador ';'.")
        return
        
    # Extrai os dados x, y, z
    x = df['x']
    y = df['y']
    z = df['z']

    print("Preparando a grade de dados para o gráfico 3D (pode levar um momento)...")
    
    # Cria uma grade (grid) para a interpolação.
    # O número de pontos na grade (ex: 100j) define a resolução do gráfico final.
    xi = np.linspace(x.min(), x.max(), 100)
    yi = np.linspace(y.min(), y.max(), 100)
    X, Y = np.meshgrid(xi, yi)

    # Interpola os valores de Z na grade criada.
    # O método 'cubic' cria uma superfície suave. 'linear' é mais rápido.
    Z = griddata((x, y), z, (X, Y), method='cubic')

    print("Gerando o gráfico...")
    
    # Cria a figura e o eixo 3D
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plota a superfície 3D
    # 'cmap' define o esquema de cores (mapa de calor). 'viridis', 'plasma', 'jet' são boas opções.
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')

    # Configura os rótulos dos eixos
    ax.set_xlabel('Eixo X (Perfís)')
    ax.set_ylabel('Eixo Y')
    ax.set_zlabel('Eixo Z')
    ax.set_title('Mapa de Calor 3D da Superfície Medida')

    # Adiciona uma barra de cores para mapear os valores de Z
    fig.colorbar(surf, shrink=0.5, aspect=5, label='Valores de Z')

    # Define o nome do arquivo de saída
    base_name = os.path.splitext(os.path.basename(csv_filepath))[0]
    output_filename = f'{base_name}_mapa_3d.png'
    output_filepath = os.path.join(os.path.dirname(csv_filepath), output_filename)

    # Salva a figura
    try:
        plt.show();
        print(f"\nSUCESSO: Gráfico salvo como '{output_filename}'")
    except Exception as e:
        print(f"\nErro ao salvar o gráfico: {e}")

    # plt.show() # Descomente esta linha se quiser que o gráfico seja exibido na tela ao executar

# --- Início da Execução Principal ---
if __name__ == "__main__":
    csv_file = input("Por favor, insira o caminho para o arquivo CSV que deseja visualizar: ")
    visualizar_mapa_de_calor_3d(csv_file)