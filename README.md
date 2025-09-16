### Setup de l'environnement virtuel

Tout d'abord, créez un environnement virtuel Python:
```bash
python -m venv discovery
```
> vous pouvez bien sûr le nommer autrement que `discovery`

Ensuite, activez l'environnement:
```bash
source discovery/bin/activate
```
> pour désactiver l'environnement, il suffira d'utiliser la commande `deactivate`

Et installez les dépendances avec la commande suivante:

```bash
pip install -r requirements.txt
```