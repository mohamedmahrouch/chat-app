# Application de Chat en Python

Cette application est un système de chat client-serveur développé en Python avec une interface graphique Tkinter.

## Fonctionnalités

- Interface graphique utilisateur avec Tkinter
- Système d'authentification (connexion/création de compte)
- Chat en temps réel
- Messages privés
- Affichage des utilisateurs en ligne
- Historique des messages
- Gestion des profils utilisateurs
- Possibilité de modifier son nom d'utilisateur

## Prérequis

- Python 3.x
- PIL (Python Imaging Library)
- Tkinter (généralement inclus avec Python)

## Installation

1. Clonez le dépôt
2. Assurez-vous d'avoir les dépendances requises
3. Lancez le serveur : `python serveur_final.py`
4. Lancez le client : `python client_finale.py`

## Utilisation

1. Démarrez le serveur
2. Lancez l'application cliente
3. Créez un compte ou connectez-vous
4. Commencez à chatter !

### Fonctionnalités détaillées

- **Chat public** : Envoyez des messages visibles par tous les utilisateurs connectés
- **Chat privé** : Envoyez des messages privés à un utilisateur spécifique
- **Liste des utilisateurs** : Visualisez les utilisateurs actuellement connectés
- **Historique** : Consultez l'historique des messages
- **Profil** : Gérez votre profil utilisateur et modifiez votre nom

## Structure du projet

- `client_finale.py` : Application cliente avec interface graphique
- `serveur_final.py` : Serveur de chat
- `images.png` : image

## Sécurité

- Mots de passe protégés
- Communication client-serveur sécurisée
- Gestion des sessions utilisateurs
