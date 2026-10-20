# Arabic IPTV Playlists

Auto-updated M3U playlists of free, publicly available Arabic TV channels, built from the [iptv-org](https://github.com/iptv-org/iptv) database.

| Playlist | Contents |
|---|---|
| `playlists/arabic_general.m3u` | News, sports, movies, music, etc. |
| `playlists/arabic_kids.m3u` | Kids / animation channels only |

Channels are health-checked (dead links dropped), real resolution is read from each stream, and the list is sorted best quality first. Default minimum is 480p; kids channels are scarce at 720p+.

## Use on an LG webOS TV

1. Install an IPTV app from the LG Content Store (e.g. **Smart IPTV**, **SS IPTV**, **IPTV Smarters**).
2. Add the playlists by URL (after pushing to GitHub, replace `USER`/`REPO`):
   - `https://raw.githubusercontent.com/USER/REPO/main/playlists/arabic_general.m3u`
   - `https://raw.githubusercontent.com/USER/REPO/main/playlists/arabic_kids.m3u`
3. Keep them as two separate playlists so kids content stays separate.

The apps re-fetch the URL, so weekly rebuilds reach the TV automatically.

## Rebuild manually

```
python build.py              # min 480p
python build.py --min 720    # HD only
python build.py --no-check   # skip liveness check (fast, may include dead links)
```

Requires Python 3.9+, no extra packages. Source data is downloaded into `data/` on first run (delete it to refresh).

A GitHub Actions workflow (`.github/workflows/rebuild.yml`) rebuilds every Monday and commits changes.

## Notes

- Streams are third-party and can disappear or be geo-blocked; the weekly rebuild prunes dead ones.
- Only legally free-to-air / publicly listed streams from iptv-org are used.
