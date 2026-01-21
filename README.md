[![CC BY SA 4.0][cc-by-sa-shield]][cc-by-sa]

# Automatic Publication to Bluesky

This project uses a CI workflow to automatically publish bioinformatics blog posts from selected RSS feeds to a Bluesky account every day at 09:00 UTC.
Each run scans for posts published within the previous 24 hours and shares them on Bluesky with rich link previews, ensuring no duplicates are posted and avoiding the need to track previously published entries.

The use case here is [bioinfoblogs](https://bsky.app/profile/bioinfoblogs.bsky.social).

## Setup

### 1. Install dependencies

```bash
pip install atproto pyyaml
```

Or add to your `pyproject.toml`:

```toml
dependencies = [
    "feedparser>=6.0.12",
    "jinja2>=3.1.6",
    "atproto>=0.0.55",
    "pyyaml>=6.0",
]
```

### 2. Create a Bluesky app password

1. Log in to Bluesky
2. Go to **Settings → App Passwords**
3. Create a new app password
4. Save it securely

### 3. Configure credentials in GitHub

1. Go to your repository on GitHub
2. Navigate to **Settings → Secrets and variables → Actions**
3. Click **New repository secret**
4. Add two secrets:
   - **Name**: `BLUESKY_USERNAME`  
     **Value**: `your-handle.bsky.social` (without the @)
   - **Name**: `BLUESKY_PASSWORD`  
     **Value**: Your Bluesky app password created in step 2

These secrets will be securely used by the GitHub Actions workflow.

## Usage

### Test mode (dry-run)

To see what would be published without actually posting:

```bash
python bluesky_publisher.py \
  --username your-handle.bsky.social \
  --password your-app-password \
  --dry-run
```

### Real publication

```bash
python bluesky_publisher.py \
  --username your-handle.bsky.social \
  --password your-app-password
```

### Options

- `--hours N`: Fetch posts from the last N hours (default: 24)
- `--dry-run`: Test mode without actual publication

## Automation with GitHub Actions

Create `.github/workflows/bluesky.yml`:

```yaml
name: Publish to Bluesky

on:
  schedule:
    # Run every 6 hours
    - cron: '0 */6 * * *'
  workflow_dispatch: # Allow manual execution

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

## How it works

1. The script reads RSS feeds from [feeds.yaml](feeds.yaml)
2. It fetches only posts published in the last 24 hours (configurable with `--hours`)
3. It publishes each post on Bluesky with:
   - The article title
   - The source (blog name)
   - A rich link to the article
4. It saves published URLs to avoid duplicates

## Post format

Example of a generated post:

```
📝 A new method for genome assembly
✍️ Dave Tang's blog
🔗 https://davetang.org/muse/...
```

## RSS Feed Management

RSS feeds are defined in [feeds.yaml](feeds.yaml):

```yaml
feeds:
  - name: "Blog name"
    url: "https://example.com/feed.xml"
  
  - name: "Another blog"
    url: "https://example2.com/rss"
```

To add a new feed, simply edit this file.

## Tips

- Always use `--dry-run` first to check what will be published
- Adjust `--hours` according to your CI execution frequency
- If CI runs every 24h, use `--hours 24` to avoid duplicates

[cc-by-sa]: https://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-shield]: https://img.shields.io/badge/License-CC%20BY%20SA-blue.svg
