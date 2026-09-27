# plex-discover

Builds/refreshes "Discover" playlists in a Plex music library.

## Setup

```bash
cp .env.example .env
# edit .env with your PLEX_URL and PLEX_TOKEN
uv sync
```

## Usage

```bash
uv run plex-discover
```

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
