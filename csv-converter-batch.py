import pandas as pd
import csv
import os
from collections import defaultdict

def processar_perfis(filename, start_x, step_x, direction):
    """
    Processa um arquivo LVM para extrair perfis (x, y, z) baseados na mudança de direção da coordenada y.
    Esta função permanece a mesma da versão anterior.
    """
    if not os.path.exists(filename):
        print(f"  Aviso: O arquivo '{filename}' não foi encontrado.")
        return []

    processed_data = []
    current_x = start_x
    last_y = None

    for encoding in ['latin-1', 'utf-8', 'cp1252']:
        try:
            with open(filename, 'r', encoding=encoding) as f:
                header_ends = 0
                for line in f:
                    if '***End_of_Header***' in line:
                        header_ends += 1
                    if header_ends >= 2:
                        next(f, None)
                        break
                
                reader = csv.reader(f, delimiter='\t')
                
                try:
                    first_row = next(reader)
                    if len(first_row) >= 3:
                        last_y = float(first_row[1])
                        y = float(first_row[1])
                        z = float(first_row[2])
                        processed_data.append([current_x, y, z])
                except (StopIteration, ValueError, IndexError):
                    break

                for row in reader:
                    if not row or len(row) < 3: continue
                    try:
                        y = float(row[1])
                        z = float(row[2])
                    except (ValueError, IndexError):
                        continue

                    profile_changed = False
                    if direction == 'increasing' and y < last_y:
                        profile_changed = True
                    elif direction == 'decreasing' and y > last_y:
                        profile_changed = True
                    
                    if profile_changed:
                        current_x += step_x
                    
                    processed_data.append([current_x, y, z])
                    last_y = y
            
            return processed_data
        except (UnicodeDecodeError, Exception):
            continue
            
    print(f"  Erro: Não foi possível processar o arquivo '{filename}' com os encodings testados.")
    return []

# --- Início da Execução Principal ---

def main():
    """
    Função principal que solicita um caminho, escaneia o diretório, agrupa os arquivos e processa cada par.
    """
    # **MODIFICAÇÃO AQUI**: Solicita o caminho da pasta ao usuário
    target_directory = input("Por favor, insira o caminho para a pasta com os arquivos LVM: ")

    # Verifica se o caminho fornecido é um diretório válido
    if not os.path.isdir(target_directory):
        print(f"Erro: O caminho '{target_directory}' não é um diretório válido ou não foi encontrado.")
        return

    print(f"\nEscaneando arquivos .lvm no diretório: '{target_directory}'...")
    
    file_pairs = defaultdict(dict)

    # Percorre todos os arquivos no diretório fornecido
    for filename in os.listdir(target_directory):
        if filename.lower().endswith('_front.lvm'):
            base_name = filename.lower().replace('_front.lvm', '')
            # Armazena o caminho completo do arquivo
            file_pairs[base_name]['front'] = os.path.join(target_directory, filename)
        elif filename.lower().endswith('_back.lvm'):
            base_name = filename.lower().replace('_back.lvm', '')
            # Armazena o caminho completo do arquivo
            file_pairs[base_name]['back'] = os.path.join(target_directory, filename)
    
    if not file_pairs:
        print("Nenhum par de arquivos _front.lvm e _back.lvm foi encontrado no diretório especificado.")
        return

    print(f"Encontrados {len(file_pairs)} pares de arquivos para processar.")

    # Processa cada par encontrado
    for base_name, files in file_pairs.items():
        print(f"\n--- Processando par: {base_name} ---")

        front_file = files.get('front')
        back_file = files.get('back')

        if not front_file or not back_file:
            print(f"  Aviso: Par incompleto para '{base_name}'. Pulando.")
            continue

        print(f"  Lendo '{os.path.basename(front_file)}' (y crescente)...")
        front_data = processar_perfis(front_file, start_x=0.0, step_x=0.4, direction='increasing')

        print(f"  Lendo '{os.path.basename(back_file)}' (y decrescente)...")
        back_data = processar_perfis(back_file, start_x=0.2, step_x=0.4, direction='decreasing')

        if front_data and back_data:
            combined_data = front_data + back_data
            df_final = pd.DataFrame(combined_data, columns=['x', 'y', 'z'])
            df_final.sort_values(by=['x', 'y'], inplace=True)
            
            # **MODIFICAÇÃO AQUI**: Garante que o arquivo de saída seja salvo na pasta de entrada
            output_filename = os.path.join(target_directory, f'{base_name}_perfis.csv')
            df_final.to_csv(output_filename, index=False, sep=';') 
            
            print(f"  SUCESSO: Arquivo '{os.path.basename(output_filename)}' gerado com {len(df_final)} pontos de dados.")
        else:
            print(f"  FALHA: Não foi possível gerar o arquivo CSV para '{base_name}' devido a erros na leitura dos arquivos de entrada.")

# Garante que o script seja executado apenas quando chamado diretamente
if __name__ == "__main__":
    main()