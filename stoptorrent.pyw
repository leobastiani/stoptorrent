#!python3

import subprocess
import sys
import time



DEBUG = sys.flags.debug


time_interval = 10 # seconds
max_waiting_time = 120 # seconds
torrent = 'uTorrent.exe' if not DEBUG else 'notepad.exe'
torrent_path = '%userprofile%\\AppData\\Roaming\\uTorrent\\' if not DEBUG else '%systemroot%\\'




def isOpenedExe(exe_name):
    output = subprocess.check_output('tasklist /FI "IMAGENAME eq '+exe_name+'" /FO CSV', creationflags=0x08000000)
    if output[0] == 34:
        return True
    return False



def command(cmd):
    print('command:', cmd)
    time.sleep(0.1)
    subprocess.call(cmd, shell=True , creationflags=0x08000000)





def main(search):
    print('--- Inicio da Main ---')
    seconds = 0
    while not (isOpenedExe(search) and isOpenedExe(torrent)) and seconds < max_waiting_time:
        print('Procurando por: "%s" e "%s", seconds: %d' % (search, torrent, seconds))
        # espera encontrar o programa
        # testa se o programa tá aberto de time_interval em time_interval segundos
        seconds += time_interval
        time.sleep(time_interval)
    if seconds >= max_waiting_time:
        # passou o tempo limite de espera
        print('Não encontrado')
        sys.exit(0)
    command('taskkill /f /im '+torrent)
    command('nircmd waitprocess "'+search+'" execmd "'+torrent_path+torrent+'" /HIDE')

    if DEBUG:
        print('Pressione ENTER para sair...')
        input()




if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage:\n stoptorrent.pyw "Search this .exe"\n')
        print('stoptorrent will kill "'+torrent+'"')
        print('download nircmd before')
        sys.exit(0)
    else:
        search = sys.argv[1] # procura o exe aberto

    print('Procurando por: "%s"' % search)
    main(search)