# Publication automatique sur Bluesky

Ce projet peut maintenant publier automatiquement les articles de blogs bioinformatiques sur un compte Bluesky.

## Configuration

### 1. Installer les dépendances

```bash
pip install atproto pyyaml
```

Ou ajoutez à votre `pyproject.toml` :

```toml
dependencies = [
    "feedparser>=6.0.12",
    "jinja2>=3.1.6",
    "atproto>=0.0.55",
    "pyyaml>=6.0",
]
```

### 2. Créer un mot de passe d'application Bluesky

1. Connectez-vous à Bluesky
2. Allez dans **Settings → App Passwords**
3. Créez un nouveau mot de passe d'application
4. Sauvegardez-le en lieu sûr

### 3. Configuration des identifiants

Créez un fichier `.env` (qui ne sera pas commité grâce au `.gitignore`) :

```bash
cp .env.example .env
```

Puis modifiez `.env` avec vos identifiants :

```
BLUESKY_USERNAME=votre-handle.bsky.social
BLUESKY_PASSWORD=votre-mot-de-passe-application
```

## Utilisation

### Mode test (dry-run)

Pour voir ce qui serait publié sans réellement poster :

```bash
python bluesky_publisher.py \
  --username votre-handle.bsky.social \
  --password votre-mot-de-passe \
  --dry-run
```

### Publication réelle

```bash
python bluesky_publisher.py \
  --username votre-handle.bsky.social \
  --password votre-mot-de-passe
```

### Options

- `--hours N` : Récupérer les articles des N dernières heures (défaut: 24)
- `--dry-run` : Mode test sans publication réelle

## Automatisation avec GitHub Actions

Créez `.github/workflows/bluesky.yml` :

```yaml
name: Publier sur Bluesky

on:
  schedule:
    # Exécuter toutes les 6 heures
    - cron: '0 */6 * * *'
  workflow_dispatch: # Permet l'exécution manuelle

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      
      - name: Install dependencies
        run: |
          pip install atproto feedparser pyyaml
      
      - name: Publish to Bluesky
        env:
          BLUESKY_USERNAME: ${{ secrets.BLUESKY_USERNAME }}
          BLUESKY_PASSWORD: ${{ secrets.BLUESKY_PASSWORD }}
        run: |
          python bluesky_publisher.py \
            --username "$BLUESKY_USERNAME" \
            --password "$BLUESKY_PASSWORD" \
            --hours 24
```

N'oubliez pas d'ajouter vos secrets dans **Settings → Secrets and variables → Actions** :
- `BLUESKY_USERNAME`
- `BLUESKY_PASSWORD`

## Fonctionnement
yaml`
2. Il récupère uniquement les articles publiés dans les dernières 24h (configurable avec `--hours`)
3. Il publie chaque article sur Bluesky avec :
   - Le titre de l'article
   - La source (nom du blog)
   - Un lien riche vers l'article
4. Pas de système de doublons : si le CI tourne toutes les 24h, seuls les nouveaux articles sont récupéré
5. Il sauvegarde les URLs publiées pour éviter les doublons

## Format des posts

Exemple de post généré :

```
📝 A new method for genome assembly
✍️ Dave Tang's blog
🔗 https://davetang.org/muse/...
```

## Conseils
Gestion des flux RSS

Les flux RSS sont définis dans [feeds.yaml](feeds.yaml) :

```yaml
feeds:
  - name: "Nom du blog"
    url: "https://exemple.com/feed.xml"
  
  - name: "Autre blog"
    url: "https://exemple2.com/rss"
```

Pour ajouter un nouveau flux, éditez simplement ce fichier.

## Conseils

- Utilisez toujours `--dry-run` d'abord pour vérifier ce qui sera publié
- Ajustez `--hours` selon votre fréquence d'exécution du CI
- Si le CI tourne toutes les 24h, utilisez `--hours 24` pour éviter les doublons
- Pas besoin de système de cache, la fenêtre temporelle suffit