import socket
import pickle
import msvcrt
import time

def menu_principal():
    while True:
        print()
        print('1. Uso de memória')
        print('2. Uso de disco')
        print('3. Informações de CPU')
        print('4. Navegar diretórios')
        print('5. Informações de processos')
        print('6. Informações de redes')
        print('0. Sair')
        print('')

        sair = False
        
        while True:
            try:
                opcao = int(input(''))
            except:
                print('Insira um número válido.')
                continue

            if(opcao == 1):
                loop_info_memoria()
                break
            elif(opcao == 2):
                pdisco = get_data('disco')
                if pdisco == None:
                    break
                imprimir_uso_disco(pdisco)
                break
            elif(opcao == 3):
                sub_menu_cpu()
                break
            elif(opcao == 4):
                navegar_diretorio()
                break
            elif(opcao == 5):
                processos = get_data('processos')
                if processos == None:
                    break
                imprimir_processos(processos)
                break
            elif(opcao == 6):
                info_redes = get_data('rede')
                if info_redes == None:
                    break
                imprimir_info_redes(info_redes)
                break
            elif(opcao == 0):
                print('Fechando a aplicação...')
                sair = True
                break
            else:
                print('Opção inválida!')
            
        if sair: break
            

def sub_menu_cpu():
    while True:
        print()
        print('Informações de CPU')
        print('1. Sumário das informações')
        print('2. Nome e modelo')
        print('3. Arquitetura')
        print('4. Palavra do processador')
        print('5. Frequência')
        print('6. Núcleos')
        print('7. Uso de CPU')
        print('0. Voltar')

        voltar = False
            
        while True:
            try:
                opcao = int(input(''))
            except:
                print('Insira um número válido.')
                continue

            if(opcao == 1):
                info_cpu = get_data('cpu')
                if info_cpu == None:
                    break
                imprimir_info_cpu(info_cpu)
                break
            elif(opcao == 2):
                info_cpu = get_data('cpu')
                if info_cpu == None:
                    break
                imprimir_modelo_cpu(info_cpu['modelo'])
                break
            elif(opcao == 3):
                info_cpu = get_data('cpu')
                if info_cpu == None:
                    break
                imprimir_arq_cpu(info_cpu['arquitetura'])
                break
            elif(opcao == 4):
                info_cpu = get_data('cpu')
                if info_cpu == None:
                    break
                imprimir_palavra_cpu(info_cpu['palavra'])
                break
            elif(opcao == 5):
                info_cpu = get_data('cpu')
                if info_cpu == None:
                    break
                imprimir_freq_cpu(info_cpu['frequencia'])
                break
            elif(opcao == 6):
                info_cpu = get_data('cpu')
                if info_cpu == None:
                    break
                imprimir_nucleos_cpu(info_cpu['nucleos'], info_cpu['nucleos_fisicos'])
                break
            elif(opcao == 7):
                info_cpu = get_data('cpu')
                if info_cpu == None:
                    break
                imprimir_uso_cpu(info_cpu['pcpu'])
                break
            elif(opcao == 0):
                voltar = True
                break
            else:
                print('Opção inválida!')
                
        if voltar: break

def instancia_socket():
    try:
        host = socket.gethostname()
        port = 20666
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
        sckt.connect((host, port))
    except Exception:
        raise Exception

    return sckt
    

def imprimir_uso_memoria(pmem):
    print("Porcentagem de uso de memória: {}% - Pressione qualquer tecla para continuar...".format(pmem), end='\r')

def loop_info_memoria():
    while True:
        pmem = get_data('memoria')
        if pmem == None:
            return
        imprimir_uso_memoria(pmem)
        time.sleep(0.5)
        if msvcrt.kbhit():
            print()
            break

def imprimir_uso_disco(pdisco):
    print("Porcentagem de uso de disco: {}%".format(pdisco))

def imprimir_diretorio(data):
    print('{:<40}'.format('Nome'), end='')
    print('{:<9}'.format('Tipo'), end='')
    print('{:<13}'.format('Tamanho'), end='')
    print('{:<35}'.format('Caminho Absoluto'), end='')
    print()
    for arq in data:
        print('{:<40}'.format(arq['nome']), end='')
        print('{:<9}'.format('Pasta' if arq['tamanho'] == 0 else 'Arquivo'), end='')
        print('{:<13}'.format('' if arq['tamanho'] == 0 else formatar_tamanho(arq['tamanho'])), end='')
        print('{:<35}'.format(arq['abspath']), end='')
        print()

def formatar_tamanho(tamanho):
    tamanho_formatado = ''
    tamanho = int(round(tamanho/1024))
    tamanho_formatado = str(tamanho) + 'KB'
    return tamanho_formatado
    
    

def navegar_diretorio():
    print('Escreva abaixo o diretório sobre o qual quer ver informações.')
    print('Dica: Você pode digitar \".\" (sem aspas) para ver informações do diretório em que o servidor está sendo executado.')
    dir = input()

    info_diretorio = get_data('diretorio ' + dir)
    if info_diretorio == None:
        print('Não foi possível encontrar o diretório. Tem certeza que digitou o caminho corretamente?')
        return
    imprimir_diretorio(info_diretorio)

def imprimir_processos(processos):
    print('{:<6}'.format('PID'), end='')
    print('{:<25}'.format('Nome'), end='')
    print('{:<25}'.format('Usuário'), end='')
    print()
    for p in processos:
        pid = p['pid']
        nome = p['name']
        usuario = '--' if p['username'] == None else p['username']
        print('{:<6}'.format(pid), end='')
        print('{:<25}'.format(nome), end='')
        print('{:<25}'.format(usuario), end='')
        print()

def imprimir_info_redes(data):
    for interface in data:
        print('Lista de endereços da interface', interface)        
        print('{:<10}'.format('Família'), end='')
        print('{:<15}'.format('Máscara'), end='')
        print('{:<25}'.format('Endereço'), end='')
        print()
        for endereco in data[interface]:
            print('{:<10}'.format(endereco['familia']), end='')
            print('{:<15}'.format('--' if endereco['mascara'] == None else endereco['mascara']), end='')
            print('{:<25}'.format(endereco['endereco']), end='')
            print()
        print()

def imprimir_info_cpu(data):
    print()
    print('Resumo das informações:')
    print('{:<19}'.format('Modelo:'), data['modelo'])
    print('{:<19}'.format('Palavra:'), str(data['palavra']) + ' bits')
    print('{:<19}'.format('Arquitetura:'), data['arquitetura'])
    print('{:<19}'.format('Frequência:'), str(data['frequencia']) + 'Hz')
    print('{:<19}'.format('Nucleos (físicos):'), (str(data['nucleos']) + '(' + str(data['nucleos_fisicos']) +')'))

def imprimir_modelo_cpu(modelo):
    print('Modelo:', modelo)

def imprimir_arq_cpu(arquitetura):
    print('Arquitetura:', arquitetura)

def imprimir_palavra_cpu(palavra):
    print('Palavra:', str(palavra) + ' bits')

def imprimir_freq_cpu(frequencia):
    print('Frequência:', str(frequencia) + 'Hz')

def imprimir_nucleos_cpu(nucleos, nucleos_fisicos):
    print('Nucleos (físicos):', str(nucleos) + '(' + str(nucleos_fisicos) +')')

def imprimir_uso_cpu(pcpu):
    for n in range(1, len(pcpu)+1):
        print('Porcentagem de uso do núcleo {}:'.format(n), pcpu[n-1])

def get_data(mensagem):
    data = None
    try:
        s = instancia_socket()
        s.send(mensagem.encode('ascii'))
        b = s.recv(16000)

        data = pickle.loads(b)
    except:
        print('Não foi possível abrir uma conexão com o servidor remoto.')
    return data
    



if __name__ == '__main__':
    menu_principal()
