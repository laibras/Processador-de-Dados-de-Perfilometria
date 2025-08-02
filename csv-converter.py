import pandas as pd
import csv
import os

def processar_perfis(filename, start_x, step_x, direction):
    """
    Processa um arquivo LVM para extrair perfis (x, y, z) baseados na mudança de direção da coordenada y.

    Args:
        filename (str): Caminho para o arquivo .lvm.
        start_x (float): O valor inicial de x para o primeiro perfil.
        step_x (float): O incremento no valor de x para cada novo perfil.
        direction (str): A direção esperada da coordenada y ('increasing' ou 'decreasing').

    Returns:
        list: Uma lista de listas, onde cada lista interna é [x, y, z].
    """
    if not os.path.exists(filename):
        print(f"Erro: O arquivo '{filename}' não foi encontrado.")
        return []

    processed_data = []
    current_x = start_x
    last_y = None

    # Tenta ler o arquivo com diferentes codificações
    for encoding in ['latin-1', 'utf-8', 'cp1252']:
        try:
            with open(filename, 'r', encoding=encoding) as f:
                # Pula o cabeçalho complexo do LVM
                header_ends = 0
                for line in f:
                    if '***End_of_Header***' in line:
                        header_ends += 1
                    if header_ends >= 2:
                        # A próxima linha pode ser o cabeçalho das colunas, então a pulamos
                        next(f, None)
                        break
                
                # Lê as linhas de dados
                reader = csv.reader(f, delimiter='\t')
                
                # Pega a primeira linha de dados para inicializar last_y
                try:
                    first_row = next(reader)
                    # Garante que a primeira linha tenha dados suficientes
                    if len(first_row) >= 3:
                        last_y = float(first_row[1])
                        y = float(first_row[1])
                        z = float(first_row[2])
                        processed_data.append([current_x, y, z])
                    else:
                        continue # Pula para a próxima linha se a primeira estiver mal formatada
                except (StopIteration, ValueError, IndexError):
                    # Se não conseguir ler a primeira linha, o arquivo pode estar vazio ou mal formatado
                    break

                # Processa o resto das linhas
                for row in reader:
                    if not row or len(row) < 3:
                        continue
                    
                    try:
                        y = float(row[1])
                        z = float(row[2])
                    except (ValueError, IndexError):
                        continue

                    # Lógica de detecção de novo perfil
                    profile_changed = False
                    if direction == 'increasing' and y < last_y:
                        # Para o arquivo 'front', o perfil muda quando y, que estava crescendo, de repente diminui
                        profile_changed = True
                    elif direction == 'decreasing' and y > last_y:
                        # Para o arquivo 'back', o perfil muda quando y, que estava diminuindo, de repente aumenta
                        profile_changed = True
                    
                    if profile_changed:
                        current_x += step_x
                    
                    processed_data.append([current_x, y, z])
                    last_y = y
            
            # Se a leitura foi bem-sucedida, retorna os dados
            return processed_data
        except (UnicodeDecodeError, Exception) as e:
            # Se ocorrer um erro, tenta o próximo encoding
            # print(f"Falha ao ler '{filename}' com encoding {encoding}: {e}") # Descomente para depuração
            continue
            
    print(f"Não foi possível processar o arquivo '{filename}' com os encodings testados.")
    return []

# --- Início da Execução Principal ---

# Nomes dos arquivos de entrada
front_file = 'Jac14_50_01_front_2.lvm'
back_file = 'Jac14_50_01_back.lvm'

print("Iniciando processamento...")

# Processa o arquivo 'front'
print(f"Processando '{front_file}' (y crescente)...")
front_data = processar_perfis(front_file, start_x=0.0, step_x=0.2, direction='increasing')
if front_data:
    print(f"Processamento de '{front_file}' concluído. Encontrados {len(front_data)} pontos.")

# Processa o arquivo 'back'
print(f"\nProcessando '{back_file}' (y decrescente)...")
back_data = processar_perfis(back_file, start_x=0.1, step_x=0.2, direction='decreasing')
if back_data:
    print(f"Processamento de '{back_file}' concluído. Encontrados {len(back_data)} pontos.")

# Combina e salva os resultados
if front_data and back_data:
    print("\nCombinando e salvando os dados...")
    
    # Combina as listas de dados
    combined_data = front_data + back_data
    
    # Cria o DataFrame final
    df_final = pd.DataFrame(combined_data, columns=['x', 'y', 'z'])
    
    # Ordena os valores para garantir a sequência correta dos perfis
    df_final.sort_values(by=['x', 'y'], inplace=True)
    
    # Salva em um arquivo CSV
    output_filename = 'perfis_combinados_final.csv'
    # Usando ';' como separador decimal para facilitar a abertura em softwares como o Excel
    df_final.to_csv(output_filename, index=False, sep=';') 
    
    print(f"\nArquivo '{output_filename}' criado com sucesso!")
    print("Visualização dos 5 primeiros dados combinados:")
    print(df_final.head())
    print("\nVisualização dos 5 últimos dados combinados:")
    print(df_final.tail())
else:
    print("\nNão foi possível gerar o arquivo CSV final, pois um ou ambos os arquivos de entrada não puderam ser processados.")