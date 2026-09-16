import socket

# 1. Création du socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Connexion au serveur
client.connect(('localhost', 8765))

# 3. Envoi du message (converti en octets)
message_a_envoyer = "Hello test"
client.send(message_a_envoyer.encode('utf-8'))

# 4. Fermeture
client.close()