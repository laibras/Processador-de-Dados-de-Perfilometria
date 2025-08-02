import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

def visualizar_dispersao_3d_interativa(csv_filepath):
    """
    Cria e exibe um gráfico de dispersão 3D interativo a partir de um arquivo CSV.

    Args:
        csv_filepath (str): O caminho completo para o arquivo CSV.
    """
    # Verifica se o arquivo existe
    if not os.path.exists(csv_filepath):
        print(f"Erro: O arquivo '{csv_filepath}' não foi encontrado.")
        return

    print(f"Lendo dados de '{os.path.basename(csv_filepath)}'...")
    try:
        df = pd.read_csv(csv_filepath, sep=';')
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        return
        
    if not all(col in df.columns for col in ['x', 'y', 'z']):
        print("Erro: O arquivo CSV deve conter as colunas 'x', 'y' e 'z'.")
        return

    x = df['x']
    y = df['y']
    z = df['z']

    print("Gerando o gráfico de dispersão 3D...")
    
    # Cria a figura e o eixo 3D
    fig = plt.figure(figsize=(12, 9)) # Aumentei um pouco a altura para melhor visualização
    ax = fig.add_subplot(111, projection='3d')

    # Plota os pontos de dispersão
    scatter = ax.scatter(x, y, z, c=z, cmap='viridis', s=5)

    # Configura os rótulos dos eixos e título
    ax.set_xlabel('Eixo X (Perfís)')
    ax.set_ylabel('Eixo Y')
    ax.set_zlabel('Eixo Z')
    ax.set_title('Visualização 3D dos Pontos Medidos\n(Use o mouse para girar e dar zoom)')

    # Adiciona a barra de cores
    fig.colorbar(scatter, shrink=0.5, aspect=5, label='Valores de Z')

    # **MODIFICAÇÃO PRINCIPAL AQUI**
    # Em vez de salvar, o comando abaixo abre a janela interativa.
    try:
        print("\nExibindo o gráfico. Feche a janela do gráfico para encerrar o programa.")
        plt.show()
    except Exception as e:
        print(f"\nOcorreu um erro ao tentar exibir o gráfico: {e}")
        print("Pode ser necessário instalar ou configurar um 'backend' de interface gráfica para o matplotlib, como o 'tk'.")

# --- Início da Execução Principal ---
if __name__ == "__main__":
    csv_file = input("Por favor, insira o caminho para o arquivo CSV que deseja visualizar: ")
    visualizar_dispersao_3d_interativa(csv_file)