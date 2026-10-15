# Golfight 🏌️‍♂️
## Nom du Projet : Golfight

C'est un jeu de mini-golf 2D en vue du dessus, en 1 contre 1. Sa particularité est le placement inversé : chaque joueur choisit où son adversaire commence et où se trouve le trou de son adversaire. 
Il faut donc piéger l'autre tout en se sortant du piège qu'il nous a tendu.
---
## Installation (doit être 1 seule ligne)

**1. Récupérer le projet**
```bash
git clone [https://github.com/Hitghul/golfight.git](https://github.com/Hitghul/golfight.git)
cd golfight

```

**2. Créer et activer l'environnement virtuel**

*Sur MacOS / Linux :*

```bash
python3 -m venv env
source env/bin/activate

```

*Sur Windows :*

```cmd
python -m venv env
env\Scripts\activate

```

**3. Installer les dépendances**

```bash
pip install -r requirements.txt

```

**4. Lancer le jeu**

```bash
python main.py

```

**5. Lancer le site en local**

```bash
daphne server.asgi:application

```

Puis ouvrir http://localhost:8000 dans le navigateur. 

---

## Comptes par défaut
admin / projetinfo1A

---
## Roadmap
### Besoins fonctionnels

Priorités : **Doit** (MVP) · **Devrait** (important) · **Bonus** (si le temps le permet).

### Jeu et physique
| ID | Fonctionnalité | Priorité | Sprint | Statut |
|---|---|---|---|------|
| F1 | Tir par cliquer-glisser, avec flèche de visée | Doit | 1 | Fait |
| F2 | Physique : trajectoire droite, ralentissement, arrêt net, rebonds | Doit | 1 | Fait |
| F3 | Chargement d'une carte depuis un fichier JSON | Doit | 1 | Fait |
| F4 | Détection de la balle dans le trou | Doit | 1 | Fait |
| F5 | Indicateur de vitesse et seuil de tir | Devrait | 1 | Fait |
| F6 | Collision entre les deux balles | Doit | 3 | À faire |
| F7 | Mode solo | Doit | 2 | Fait |
| F8 | Ajout des objets de base de la phase de piégeage | Doit | 2 | À faire |


### Multijoueur et lobby
| ID | Fonctionnalité | Priorité | Sprint | Statut |
|---|---|-------|---|---|
| F10 | Saisie du pseudo à l'arrivée | Doit  | 2 | À faire |
| F11 | Liste en temps réel des joueurs connectés et disponibles | Doit  | 2 | À faire |
| F12 | Invitation d'un joueur, avec acceptation ou refus | Doit  | 2 | À faire |
| F13 | Lobby commun : choix de la carte et du mode, bouton « Prêt » | Devrait | 2 | À faire |
| F14 | Chercher ou rejoindre un lobby ouvert (sans invitation) | Bonus | 3 | À faire |
| F15 | Synchronisation en temps réel de la partie (le serveur fait autorité) | Doit  | 2 | À faire |
| F16 | Tir simultané avec seuil de vitesse (§4.3) | Devrait | 2 | À faire |
| F17 | Phase de placement inversé : balle et trou de l'adversaire (§4.2) | Doit  | 3 | À faire |
| F18 | Fin de manche, vote « Rejouer / Quitter », score de la session | Doit  | 3 | À faire |
| F19 | Gestion des déconnexions (forfait au bout de 30 s) | Devrait | 3 | À faire |

### Cartes
| ID | Fonctionnalité | Priorité | Sprint | Statut |
|---|---|---|---|-----|
| F20 | Au moins 3 cartes au choix (carré, triangle, octogone : déjà faites) | Doit | 1 | À faire |
| F21 | Cartes avec des agencements d'obstacles variés | Doit | 3 | À faire |
| F22 | Éditeur de cartes : poser murs et obstacles, puis sauvegarder en JSON | Bonus | 3 | À faire |

### Graphisme et interface
| ID | Fonctionnalité | Priorité | Sprint | Statut |
|---|---|---|---|---|
| F30 | Menu principal (Solo / 1v1 / Réglages) dans le navigateur | Doit | 2 | À faire |
| F31 | Interface en jeu : tir possible ou non, score, pseudos | Doit | 3 | À faire |
| F32 | Chargement et application de textures (gazon, murs, balle, trou) | Devrait | 3 | À faire |
| F33 | Particules (impact sur un mur, balle dans le trou) | Bonus | 3 | À faire |
| F34 | Animation de transition entre les écrans | Bonus | 3 | À faire |
| F35 | Effets sonores | Bonus | — | À faire |

---


## Modèle de données
![graphe des modèles](docs/models.png)
