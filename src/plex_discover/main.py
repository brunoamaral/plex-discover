"""Builds/refreshes 'Discover' playlists in Plex.

Smart playlists (native Plex filters, auto-refresh on their own):
    Discover - Never Played
    Discover - Forgotten
    Discover - Buried Favorites
    Discover - New Arrivals
    Discover - Mood: <mood>      one per entry in MOODS
    Discover - Style: <style>    one per entry in STYLES
    Discover - Full Album Cold Start
    Discover - Decade: <decade>  one per entry in DECADES

Regular playlists (computed here, rebuilt on each run):
    Discover - Deep Cuts
    Discover - On This Day
"""

import datetime
import os
import random
from collections import defaultdict

from dotenv import load_dotenv
from plexapi.server import PlexServer

LIBRARY_NAME = "Music"
PREFIX = "Discover"

MOODS = ["Melancholic", "Energetic", "Chill"]  # match tags shown in your Mood filter dropdown
STYLES = ["Alternative Rock", "Deep House"]  # match tags shown in your Style filter dropdown
DECADES = [(1990, 1999), (2000, 2009), (2010, 2019)]


def replace_smart_playlist(plex, section, title, filters, limit, libtype="track"):
    existing = next((p for p in plex.playlists() if p.title == title), None)
    if existing:
        existing.delete()
    plex.createPlaylist(
        title=title,
        section=section,
        smart=True,
        limit=limit,
        sort="random",
        libtype=libtype,
        filters=filters,
    )
    print(f"Rebuilt: {title}")


def replace_regular_playlist(plex, title, items):
    existing = next((p for p in plex.playlists() if p.title == title), None)
    if existing:
        existing.delete()
    if items:
        plex.createPlaylist(title=title, items=items)
    print(f"Rebuilt: {title} ({len(items)} tracks)")


def build_smart_playlists(plex, section):
    replace_smart_playlist(
        plex, section, f"{PREFIX} - Never Played",
        filters={"viewCount": 0}, limit=50,
    )
    replace_smart_playlist(
        plex, section, f"{PREFIX} - Forgotten",
        filters={"and": [{"viewCount__gte": 1}, {"lastViewedAt__lte": "-90d"}]}, limit=30,
    )
    replace_smart_playlist(
        plex, section, f"{PREFIX} - Buried Favorites",
        filters={"and": [{"userRating__gte": 7}, {"viewCount__lt": 3}]}, limit=30,
    )
    replace_smart_playlist(
        plex, section, f"{PREFIX} - New Arrivals",
        filters={"and": [{"addedAt__gte": "-60d"}, {"viewCount": 0}]}, limit=25,
    )
    for mood in MOODS:
        replace_smart_playlist(
            plex, section, f"{PREFIX} - Mood: {mood}",
            filters={"and": [{"mood": mood}, {"lastViewedAt__lte": "-60d"}]}, limit=25,
        )
    for style in STYLES:
        replace_smart_playlist(
            plex, section, f"{PREFIX} - Style: {style}",
            filters={"and": [{"style": style}, {"viewCount__lt": 2}]}, limit=25,
        )
    replace_smart_playlist(
        plex, section, f"{PREFIX} - Full Album Cold Start",
        filters={"viewCount": 0}, limit=1, libtype="album",
    )
    for start, end in DECADES:
        replace_smart_playlist(
            plex, section, f"{PREFIX} - Decade: {start}s",
            filters={"and": [{"year__gte": start}, {"year__lte": end}, {"lastViewedAt__lte": "-180d"}]},
            limit=30,
        )


def build_deep_cuts(plex, section, min_artist_plays=50, max_track_plays=1, limit=25):
    tracks = section.searchTracks()
    artist_plays = defaultdict(int)
    for t in tracks:
        artist_plays[t.grandparentTitle] += t.viewCount

    candidates = [
        t for t in tracks
        if artist_plays[t.grandparentTitle] >= min_artist_plays and t.viewCount <= max_track_plays
    ]
    picks = random.sample(candidates, min(limit, len(candidates)))
    replace_regular_playlist(plex, f"{PREFIX} - Deep Cuts", picks)


def build_on_this_day(plex, section, window_days=3, limit=25):
    today = datetime.date.today()
    tracks = section.searchTracks()

    def matches(t):
        ref = t.lastViewedAt or t.addedAt
        if not ref:
            return False
        ref = ref.date()
        if ref.year == today.year:
            return False
        try:
            same_year = ref.replace(year=today.year)
        except ValueError:
            return False  # Feb 29 on a non-leap year
        return abs((same_year - today).days) <= window_days

    candidates = [t for t in tracks if matches(t)]
    picks = random.sample(candidates, min(limit, len(candidates)))
    replace_regular_playlist(plex, f"{PREFIX} - On This Day", picks)


def main():
    load_dotenv()

    plex_url = os.environ["PLEX_URL"]
    plex_token = os.environ["PLEX_TOKEN"]
    library_name = os.environ.get("PLEX_LIBRARY", LIBRARY_NAME)

    plex = PlexServer(plex_url, plex_token)
    section = plex.library.section(library_name)

    build_smart_playlists(plex, section)
    build_deep_cuts(plex, section)
    build_on_this_day(plex, section)


if __name__ == "__main__":
    main()
