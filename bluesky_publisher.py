import feedparser
import yaml
import calendar
from pathlib import Path
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
from atproto import Client, models


# === Config ===
FEEDS_FILE = Path("feeds.yaml")
MAX_POST_LENGTH = 300  # Bluesky limit


def extract_dt(entry) -> datetime:
    """Prefer parsed structs from feedparser"""
    for attr in ("published_parsed", "updated_parsed"):
        t = entry.get(attr)
        if t:
            # t is time.struct_time (UTC). Make it aware.
            return datetime.fromtimestamp(calendar.timegm(t), tz=timezone.utc)
    # Fallback: try RFC2822/ISO-ish strings
    for attr in ("published", "updated"):
        s = entry.get(attr)
        if s:
            try:
                return parsedate_to_datetime(s).astimezone(timezone.utc)
            except Exception:
                pass
    # No date at all → push to the end
    return datetime(1970, 1, 1, tzinfo=timezone.utc)


def create_post_text(item):
    """Créer le texte du post pour Bluesky"""
    title = item["title"]
    source = item["source"]
    link = item["link"]
    
    # Format: "📝 [Titre] par [Source]\n🔗 [lien]"
    base_text = f"📝 {title}\n✍️ {source}"
    
    # Vérifier la longueur et tronquer si nécessaire
    if len(base_text) + len(link) + 3 > MAX_POST_LENGTH:
        max_title_len = MAX_POST_LENGTH - len(source) - len(link) - 20
        title = title[:max_title_len] + "..."
        base_text = f"📝 {title}\n✍️ {source}"
    
    return base_text, link


def publish_to_bluesky(username, password, dry_run=False, hours_back=24):
    """
    Publie les nouveaux articles sur Bluesky
    
    Args:
        username: Identifiant Bluesky (ex: votre-handle.bsky.social)
        password: Mot de passe d'application Bluesky
        dry_run: Si True, affiche ce qui serait posté sans publier
        hours_back: Nombre d'heures dans le passé pour récupérer les articles
    """
    # Se connecter à Bluesky
    client = Client()
    if not dry_run:
        client.login(username, password)
        print(f"✅ Connecté à Bluesky en tant que {username}")
    
    # Charger les URLs déjà postées
    posted_urls = load_posted_urls()
    
    # === Load feeds ===
    feeds = []
    for line in FEEDS_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "," in line:
            name, url = line.split(",", 1)
      === Load feeds from YAML ===
    with open(FEEDS_FILE, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    feeds = [(feed["name"], feed["url"]) for feed in config.get("feeds", [])])
            title = name.strip() if name.strip() else raw_title.strip() or url
            
            for entry in feed.entries[:5]:
                dt = extract_dt(entry)
                
                # Ignorer les articles trop anciens
                if dt < cutoff_time:
                    continue
                
                # Ignorer les articles déjà postés
                if entry.link in posted_urls:
                    continue
                
                display_date = (
                    entry.get("published")
                    or entry.get("updated")
                    or dt.st
                        "title": entry.title,
                        "link": entry.link,
                        "source": title,
                        "published": display_date,
                        "dt": dt,
                    }
                )
        except Exception as e:
            print(f"⚠️ Erreur lors de la récupération de {name}: {e}")
            continue
    
    # === Trier par date (plus ancien en premier) ===
    items.sort(key=lambda x: x["dt"])
    
    # === Publier les articles ===
    newly_posted = []
    
    for item in items:
        text, link = create_post_text(item)
        
        if dry_run:
            print(f"\n{'='*60}")
            print(f"🔍 [DRY RUN] Article à publier:")
            print(f"Titre: {item['title']}")
            print(f"Source: {item['source']}")
            print(f"Date: {item['published']}")
            print(f"Lien: {link}")
            print(f"\n📱 Post Bluesky:\n{text}\n🔗 {link}")
    published_count = 0
    
    for item in items:
        text, link = create_post_text(item)
        
        if dry_run:
            print(f"\n{'='*60}")
            print(f"🔍 [DRY RUN] Article à publier:")
            print(f"Titre: {item['title']}")
            print(f"Source: {item['source']}")
            print(f"Date: {item['published']}")
            print(f"Lien: {link}")
            print(f"\n📱 Post Bluesky:\n{text}\n🔗 {link}")
            published_count += 1
        else:
            try:
                # Créer le post avec un lien riche (embed)
                client.send_post(
                    text=text,
                    embed=models.AppBskyEmbedExternal.Main(
                        external=models.AppBskyEmbedExternal.External(
                            title=item["title"],
                            description=f"Article de {item['source']}",
                            uri=link,
                        )
                    )
                )
                print(f"✅ Publié: {item['title'][:50]}...")
                published_count += 1
            except Exception as e:
                print(f"❌ Erreur lors de la publication: {e}")
                continue
    
    # Résumé
    if published_count > 0 and not dry_run:
        print(f"\n🎉 {published_count} article(s) publié(s) sur Bluesky!")
    elif not items:
        print("\nℹ️  Aucun nouvel article à publier.")
    elif dry_run:
        print(f"\n🔍 [DRY RUN] {published_count
    parser.add_argument(
        "--password",
        required=True,
        help="Mot de passe d'application Bluesky",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mode test: affiche ce qui serait posté sans publier",
    )
    parser.add_argument(
        "--hours",
        type=int,
        default=24,
        help="Nombre d'heures dans le passé pour récupérer les articles (défaut: 24)",
    )
    
    args = parser.parse_args()
    
    publish_to_bluesky(
        username=args.username,
        password=args.password,
        dry_run=args.dry_run,
        hours_back=args.hours,
    )
