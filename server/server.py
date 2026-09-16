import socket

# 1. Création du socket (IPv4, TCP)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8765))
server.listen()

print("Serveur en attente de connexion...")

# 2. Le serveur bloque ici jusqu'à ce qu'un client se connecte
client_socket, address = server.accept()
print(f"Connecté avec : {address}")

# 3. Réception du message (1024 octets max) et décodage du texte
message = client_socket.recv(1024).decode('utf-8')
print(f"Message reçu du client : {message}")

# 4. Fermeture des connexions
client_socket.close()
server.close()