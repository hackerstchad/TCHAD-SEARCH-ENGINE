# TCHAD SEARCH ENGINE v10.0

**Développé par HiddenWorld Communauté Tchadienne**

Moteur de recherche avancé en Python, inspiré de Yandex, Google et Bing. Recherche web, images, actualités, traduction, météo, infos IP, index local, multi-moteurs.

## Installation

```bash
pip install -r requirements_TCHAD_SEARCH.txt
python3 TCHAD_SEARCH_ENGINE.py
```

## Utilisation

### Mode interactif
```bash
python3 TCHAD_SEARCH_ENGINE.py
```

### Mode CLI
```bash
# Recherche simple
python3 TCHAD_SEARCH_ENGINE.py -q "cybersécurité"

# Multi-moteurs
python3 TCHAD_SEARCH_ENGINE.py -q "Tchad" --multi

# Images
python3 TCHAD_SEARCH_ENGINE.py -q "paysage" --images

# Actualités
python3 TCHAD_SEARCH_ENGINE.py -q "technologie" --news

# Météo
python3 TCHAD_SEARCH_ENGINE.py -q "N'Djamena" --weather

# Infos IP
python3 TCHAD_SEARCH_ENGINE.py --ip

# Sortie JSON
python3 TCHAD_SEARCH_ENGINE.py -q "python" --json
```

## Commandes interactives

- `/help` - Aide
- `/engines` - Liste des moteurs
- `/engine <nom>` - Changer de moteur
- `/multi <requête>` - Recherche multi-moteurs
- `/images <requête>` - Recherche d'images
- `/news <requête>` - Actualités
- `/translate <texte>` - Traduction
- `/weather <ville>` - Météo
- `/ip` - Infos IP
- `/history` - Historique
- `/local <requête>` - Index local
- `/save` - Sauvegarder
- `/quit` - Quitter

## Moteurs supportés

- Google
- Bing
- DuckDuckGo
- Yandex
- Yahoo
- Brave
- Ecosia

## Licence

MIT - Usage éducatif
