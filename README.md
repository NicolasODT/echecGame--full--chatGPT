# Jeu d'échecs avec interface utilisateur Pygame

Ce dépôt contient un jeu d'échecs développé à 100% avec ChatGPT en Python avec l'aide de la bibliothèque Pygame pour l'interface utilisateur et la bibliothèque Python Chess pour la logique du jeu. Stockfish est utilisé pour l'intelligence artificielle (IA) des adversaires.

## Prérequis

- Python 3.6 ou supérieur
- Pygame
- Python Chess
- Stockfish

## Installation

1. Clonez ce dépôt et accédez au dossier cloné :

```
git clone https://github.com/votre_identifiant/votre_dépôt.git
cd votre_dépôt
```

2. Installez les dépendances :

```
pip install -r requirements.txt
```

3. Téléchargez et installez Stockfish depuis le site officiel : https://stockfishchess.org/download/

4. Modifiez le chemin vers l'exécutable de Stockfish dans le fichier `main.py` :

```python
with chess.engine.SimpleEngine.popen_uci("stockfish") as engine:  # Remplacez "stockfish" par le chemin vers l'exécutable de Stockfish sur votre système
```

## Utilisation

Exécutez le fichier `main.py` pour lancer le jeu d'échecs :

```
python main.py
```

Vous pouvez choisir la difficulté de l'IA et redémarrer la partie à l'aide des options d'interface utilisateur disponibles à droite de l'échiquier.
