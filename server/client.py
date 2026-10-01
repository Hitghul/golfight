import socket
import threading

def ecouter():
    while True:
        message = client.recv(1024)
        if message == b'': break
        print(message.decode('utf-8'))

# 1. Création du socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Connexion au serveur
client.connect(('localhost', 8765))

# 3. Thread d'écoute
threading.Thread(target=ecouter).start()

# 4. Envoi du message (converti en octets)
while True:
    message_a_envoyer = input()
    client.sendall(message_a_envoyer.encode('utf-8'))
