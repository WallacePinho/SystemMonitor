import socket
import pickle
import os
import psutil
import cpuinfo3 as cpuinfo

def levantar_servidor():
    host = socket.gethostname()
    port = 20666
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sckt.bind((host, port))
    sckt.listen()

    while True:
        aceitar_conexao(sckt)
    
    sckt.close()

def aceitar_conexao(s):
    (cliente, addrs) = s.accept()
    req = cliente.recv(128).decode('ascii')
    responder_cliente(cliente, req)

def responder_cliente(cliente, msg):
    data = None
    if msg == 'memoria':
        data = get_info_memoria()
    elif msg == 'disco':
        data = get_info_disco()
    elif msg == 'cpu':
        data = get_info_cpu()
    elif 'diretorio' in msg:
        dir = msg.replace('diretorio ', '')
        data = get_info_diretorio(dir)
    elif msg == 'processos':
        data = get_info_processos()
    elif msg == 'rede':
        data = get_info_rede()

    b = pickle.dumps(data)
    cliente.send(b)

def get_info_memoria():
    pmemory = psutil.virtual_memory().percent
    return pmemory

def get_info_disco():
    pdisco = psutil.disk_usage('.').percent
    return pdisco

def get_info_cpu():
    info = cpuinfo.get_cpu_info()

    pcpu = psutil.cpu_percent(interval=0.1, percpu=True)
    modelo = info['brand']
    palavra = info['bits']
    arquitetura = info['arch']
    frequencia = psutil.cpu_freq().max
    nucleos = psutil.cpu_count()
    nucleos_fisicos = psutil.cpu_count(logical=False)

    info_cpu = {
        'modelo':modelo,
        'palavra':palavra,
        'arquitetura':arquitetura,
        'frequencia':frequencia,
        'nucleos':nucleos,
        'nucleos_fisicos':nucleos_fisicos,
        'pcpu':pcpu
    }
    return info_cpu

def get_info_diretorio(caminho):
    info_dir = []
    try:
        abspath = os.path.abspath(caminho)
        for item in os.listdir(abspath):
            arq = os.path.join(abspath, item)
            info = os.stat(arq)
            tamanho = info.st_size
            if os.path.isdir(arq):
                tamanho = 0
            info_dir.append({
                'nome':item,
                'tamanho':tamanho,
                'abspath':abspath
            })
    except:
        info_dir = None
    return info_dir

def get_info_processos():
    processos = []
    for p in psutil.process_iter():
        processos.append(p.as_dict(attrs = ['pid', 'name', 'username']))
    return processos

def get_info_rede():
    interfaces = psutil.net_if_addrs()
    data = {}
    for interface in interfaces:
        data[interface] = []
        for endereco in interfaces[interface]:
            data[interface].append({
                'familia':endereco.family.name,
                'endereco':endereco.address,
                'mascara':endereco.netmask
            })
    return data 

if __name__ == '__main__':
    levantar_servidor()
