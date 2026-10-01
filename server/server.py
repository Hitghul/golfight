import socket
import threading
def relayer (source, destination):
    while True:
        message = source.recv(1024)
        if message == b'':  break
        destination.sendall(message)

# 1. Création du socket (IPv4, TCP)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8765))
server.listen()

print("Serveur en attente de connexion...")

# 2. Le serveur bloque ici jusqu'à ce qu'un client se connecte
client_socket_1, address_1 = server.accept()
print(f"client 1 connecté avec : {address_1}")

client_socket_2, address_2 = server.accept()
print(f"client 2 connecté avec : {address_2}")

# 3. Réception du message (1024 octets max) et décodage du texte
"""message = client_socket_1.recv(1024).decode('utf-8')
print(f"Message reçu du client 1: {message}")

message = client_socket_2.recv(1024).decode('utf-8')
print(f"Message reçu du client 2: {message}") """


threading.Thread(target=relayer, args=(client_socket_1, client_socket_2)).start()
threading.Thread(target=relayer, args=(client_socket_2, client_socket_1)).start()
# 4. Fermeture des connexions
"""client_socket_1.close()
client_socket_2.close()
server.close()"""