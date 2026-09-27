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

### What each playlist contains

| Playlist | Logic |
|---|---|
| `Discover - Never Played` | Up to 50 random tracks with 0 plays. |
| `Discover - Forgotten` | Up to 30 random tracks played at least once, but not in the last 90 days. |
| `Discover - Buried Favorites` | Up to 30 random tracks rated 7+ (out of 10) that have been played fewer than 3 times — favorites you rated highly but rarely revisit. |
| `Discover - New Arrivals` | Up to 25 random tracks added to the library in the last 60 days that have never been played. |
| `Discover - Mood: <mood>` | Up to 25 random tracks tagged with that mood, not played in the last 60 days. See [Customizing the lists](#customizing-the-lists). |
| `Discover - Style: <style>` | Up to 25 random tracks tagged with that style, played fewer than 2 times. See [Customizing the lists](#customizing-the-lists). |
| `Discover - Full Album Cold Start` | A single random, entirely unplayed album — for when you want to commit to a whole album instead of shuffled tracks. |
| `Discover - Decade: <decade>s` | Up to 30 random tracks released in that decade, not played in the last 180 days. See [Customizing the lists](#customizing-the-lists). |
| `Discover - Deep Cuts` | Up to 25 random tracks by artists you've played 50+ times total, but where the specific track itself has 1 play or fewer — the overlooked songs by artists you already love. |
| `Discover - On This Day` | Up to 25 random tracks last played (or, if never played, added) on this calendar day ±3 days in a *previous* year — a "this day in your listening history" throwback. |

The smart playlists (everything above `Deep Cuts`) are built with native Plex filters, so Plex keeps them live/auto-refreshing on its own between runs. `Deep Cuts` and `On This Day` are computed in Python each time the script runs and rebuilt as regular (non-smart) playlists, since their logic (aggregating per-artist play counts, comparing calendar dates across years) isn't expressible as a single Plex filter.

### Customizing the lists

`MOODS`, `STYLES`, and `DECADES` are defined at the top of `src/plex_discover/main.py`:

```python
MOODS = ["Melancholic", "Energetic", "Chill"]
STYLES = ["Alternative Rock", "Deep House"]
DECADES = [(1990, 1999), (2000, 2009), (2010, 2019)]
```

- **`MOODS`** — must match the tags shown in your library's *Mood* filter dropdown in Plex Web. For each entry, a `Discover - Mood: <mood>` playlist is created with tracks tagged that mood that haven't been played in the last 60 days.
- **`STYLES`** — must match the tags shown in your library's *Style* filter dropdown. For each entry, a `Discover - Style: <style>` playlist is created with tracks tagged that style that have been played fewer than 2 times.
- **`DECADES`** — a list of `(start_year, end_year)` tuples. For each entry, a `Discover - Decade: <decade>s` playlist is created with tracks released in that year range that haven't been played in the last 180 days.

`mood` and `style` come from Plex's own audio-tag metadata, so they only work if your tracks are tagged (via Plex's metadata agent or your own tagging). If an entry in `MOODS`/`STYLES` doesn't match anything in your library, that playlist will simply come back empty — check the filter dropdowns in Plex Web to see which tags actually exist in your library before adding them here.

## License

MIT
