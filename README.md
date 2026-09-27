# plex-discover

Builds/refreshes "Discover" playlists in a Plex music library, so you always
have fresh smart playlists surfacing music you haven't listened to in a
while — instead of replaying the same favorites.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- A Plex Media Server with a music library, and a [Plex token](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/)

## Setup

```bash
cp .env.example .env
# edit .env with your PLEX_URL and PLEX_TOKEN
uv sync
```

### Configuration

| Variable      | Description                                  | Default                |
|---------------|-----------------------------------------------|-------------------------|
| `PLEX_URL`    | Base URL of your Plex server                  | —                        |
| `PLEX_TOKEN`  | Plex authentication token                     | —                        |
| `PLEX_LIBRARY`| Name of the music library section to target   | `Music`                  |

## Usage

```bash
uv run plex-discover
```

Run it on a schedule (cron, launchd, etc.) to keep the playlists fresh.

## Playlists

Smart playlists (native Plex filters, auto-refresh on their own):

- `Discover - Never Played`
- `Discover - Forgotten`
- `Discover - Buried Favorites`
- `Discover - New Arrivals`
- `Discover - Mood: <mood>` (one per entry in `MOODS`)
- `Discover - Style: <style>` (one per entry in `STYLES`)
- `Discover - Full Album Cold Start`
- `Discover - Decade: <decade>` (one per entry in `DECADES`)

Regular playlists (computed on each run):

- `Discover - Deep Cuts`
- `Discover - On This Day`

`MOODS`, `STYLES`, and `DECADES` are defined in `src/plex_discover/main.py` — adjust them to match the tags in your library's Mood/Style filter dropdowns.

## License

MIT
