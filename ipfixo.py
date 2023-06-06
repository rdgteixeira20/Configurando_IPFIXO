import tkinter as tk
import paramiko
import time
import subprocess

# Função para configurar o IP estático
def configure_static_ip():
    # Obtém os valores dos campos de entrada
    host = host_entry.get()
    static_ip = static_ip_entry.get()
    ssid = ssid_entry.get()

    # Configurações de conexão SSH
    port = 22  # Porta SSH padrão
    username = 'root'  # Nome de usuário SSH
    password = 'k2on2020'  # Senha SSH

    # Comandos para configurar o IP estático

    # commands = [
    #     f'nmcli con modify wlan0 ipv4.addresses {static_ip}',
    #     f'nmcli con modify wlan0 ipv4.method manual',
    #     f'nmcli con up wlan0',
    #     'systemctl restart NetworkManager',
    # ]

    try:
        # Cria uma instância do cliente SSH
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Conecta-se ao servidor Armbian
        client.connect(hostname=host, port=port, username=username, password=password)

        # Executa os comandos no servidor
        # for command in commands:
        #     stdin, stdout, stderr = client.exec_command(command)
        #     output = stdout.read().decode('utf-8')
        #     print(output)

        command = "nmcli con modify {} ipv4.addresses {}".format(ssid,static_ip)
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode('utf-8')
        print(output)

        # Fecha a conexão SSH
        client.close()

        # Ativa o botão de reinicialização
        reboot_button.config(state=tk.NORMAL)
        status_label.config(text="Configuração concluída com sucesso!", fg="green")
    except Exception as e:
        print('Ocorreu um erro:', str(e))
        status_label.config(text="Erro ao configurar IP estático", fg="red")

# Função para reinicializar o sistema
def reboot_system():
    # Obtém o endereço IP do host
    host = host_entry.get()

    # Configurações de conexão SSH
    port = 22  # Porta SSH padrão
    username = 'root'  # Nome de usuário SSH
    password = 'k2on2020'  # Senha SSH

    try:
        # Cria uma instância do cliente SSH
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Conecta-se ao servidor Armbian
        client.connect(hostname=host, port=port, username=username, password=password)

        # Reinicializa o sistema
        stdin, stdout, stderr = client.exec_command('sudo reboot')

        # Fecha a conexão SSH
        client.close()

        print('Reinicialização iniciada com sucesso!')

        # Exibe mensagem de reinicialização iniciada
        status_label.config(text="Reinicialização iniciada. Aguarde...")

        # Espera até que o sistema esteja online novamente
        while not check_host_online(host):
            time.sleep(1)

        # Exibe mensagem de reinicialização concluída
        status_label.config(text="Sistema reiniciado com sucesso!", fg="green")

    except Exception as e:
        print('Ocorreu um erro ao reinicializar o sistema:', str(e))
        status_label.config(text="Erro ao reiniciar o sistema", fg="red")

# Função para verificar se o host está online
def check_host_online(host):
    # Executa o comando de ping para verificar a conectividade
    result = subprocess.run(['ping', '-c', '1', host], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0

# Função para fechar a janela
def close_window():
    window.destroy()

# Cria uma janela Tkinter
window = tk.Tk()
window.title("Configuração de IP Estático")
window.geometry("300x350")

# Configura o estilo para o fundo preto e bordas cinzas
window.configure(bg="black")

# Cria um frame para conter os elementos da interface
frame = tk.Frame(window, bg="black")
frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

# Rótulo e campo de entrada para o endereço IP do host
host_label = tk.Label(frame, text="Endereço IP do Host:", bg="black", fg="white")
host_label.pack()
host_entry = tk.Entry(frame)
host_entry.pack()

# Rótulo e campo de entrada para o IP estático
static_ip_label = tk.Label(frame, text="IP Estático:", bg="black", fg="white")
static_ip_label.pack()
static_ip_entry = tk.Entry(frame)
static_ip_entry.pack()

# SSID do host a ser modificado
ssid_label = tk.Label(frame, text="SSID do Host a ser modificado", bg="black", fg="white")
ssid_label.pack()
ssid_entry = tk.Entry(frame)
ssid_entry.pack()

# Botão para executar a configuração
configure_button = tk.Button(frame, text="Configurar", command=configure_static_ip, bg="black", fg="white", bd=2, relief="raised")
configure_button.pack()

# Rótulo para exibir o status da configuração
status_label = tk.Label(frame, text="", bg="black", fg="white")
status_label.pack()

# Botão para reinicializar o sistema
reboot_button = tk.Button(frame, text="Reiniciar Sistema", command=reboot_system, state=tk.DISABLED, bg="black", fg="white", bd=2, relief="raised")
reboot_button.pack()

# Botão para fechar a janela
close_button = tk.Button(frame, text="Fechar", command=close_window, bg="black", fg="white", bd=2, relief="raised")
close_button.pack()

# Inicia o loop principal do Tkinter
window.mainloop()
