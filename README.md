# Arabic IPTV Playlists

Free, auto-updating **M3U playlists of Arabic TV channels**, split into two lists so kids' channels stay separate from everything else.

| Playlist | What's in it | URL |
|---|---|---|
| **General** | News, sports, movies, music, entertainment, religion, etc. (480p and up) | `https://raw.githubusercontent.com/spyzoro/iptv-arabic-playlists/main/playlists/arabic_general.m3u` |
| **Kids** | Kids and animation channels only (480p and up) | `https://raw.githubusercontent.com/spyzoro/iptv-arabic-playlists/main/playlists/arabic_kids.m3u` |
| **General 720p+ (HD)** | Same as General, but only channels confirmed at 720p or better | `https://raw.githubusercontent.com/spyzoro/iptv-arabic-playlists/main/playlists/arabic_general_720p.m3u` |
| **Kids 720p+ (HD)** | Same as Kids, but only 720p or better | `https://raw.githubusercontent.com/spyzoro/iptv-arabic-playlists/main/playlists/arabic_kids_720p.m3u` |

Not sure which to pick? Use the **720p+ (HD)** lists if your TV and internet are good. They have fewer channels, but all of them are HD. Use the standard lists if you want the most channels.

- Dead links are removed. Every stream is tested before it is listed.
- Quality is read from the stream itself, and each channel name shows it (for example `[1080p]`).
- Best quality is listed first, and only the best stream per channel is kept.
- The lists are rebuilt automatically every Monday, so you never need to re-download anything.

> **Heads up:** the kids list is small (about 8 channels, 6 in HD). Free Arabic kids channels in HD are rare.

---

## Quick start (60 seconds)

1. Open any IPTV player (see [Apps](#apps-that-work) below).
2. Choose **Add playlist** and then **From URL**.
3. Paste the General URL from the table above. Add the Kids URL as a second, separate playlist.
4. Done. Your player re-downloads the list on its own, so you get updates automatically.

Tip: if your player asks for a "name", call them `Arabic` and `Arabic Kids`. You can then put a PIN or parental lock on the kids list, or just leave the general one off the kids' profile.

---

## Apps that work

Any player that accepts an M3U URL works. Some common ones:

| Device | App | How to add the playlist |
|---|---|---|
| **LG webOS TV** | Smart IPTV (paid, one-time fee), SS IPTV, IPTV Smarters | Install from the LG Content Store. Add the URL in the app's settings, or use the app's website with your TV's MAC address. |
| **Samsung Tizen TV** | Smart IPTV, SS IPTV | Same as above. |
| **Android / Android TV / Fire TV** | TiviMate, IPTV Smarters, OTT Navigator | Add playlist, then M3U URL. |
| **iPhone / iPad / Apple TV** | IPTVX, GSE Smart IPTV | Add playlist, then Remote URL. |
| **Windows / Mac / Linux / any** | VLC | Media, then Open Network Stream, then paste the URL. |
| **Kodi** | PVR IPTV Simple Client | Add-on settings, then General, then M3U playlist URL. |

App availability changes by region and over time. If one isn't in your store, try another from the list.

### LG webOS example (Smart IPTV)

1. Install **Smart IPTV** from the LG Content Store and open it. Note the **MAC address** shown on screen.
2. On your phone or PC, go to the Smart IPTV website, "My list" page.
3. Enter the MAC address, paste the General URL, and upload. Repeat the process for the Kids URL if the app supports a second list.
4. Restart the app on the TV.

---

## What if a channel doesn't play?

- **Streams are run by third parties** and can go offline at any time. The weekly rebuild removes dead ones.
- Some channels are **geo-blocked** and only play in certain countries. A VPN may help, or may not.
- If the whole list is empty, check that you pasted the **raw** URL (it starts with `raw.githubusercontent.com`) and not the normal GitHub page URL.
- If an app complains about the format, make sure it supports `.m3u` / `.m3u8` playlists.

---

## Make your own copy (optional)

You can run your own copy, for example to change the quality limit or to include other countries. No server is needed. GitHub does the work for free.

1. Click **Fork** at the top of this page.
2. In your fork, open the **Actions** tab and click *"I understand my workflows, go ahead and enable them"*.
3. Open **Actions**, then **Rebuild playlists**, then **Run workflow**. This builds your lists straight away, and after that they rebuild weekly.
4. Your playlist URLs become:
   `https://raw.githubusercontent.com/YOUR-USERNAME/iptv-arabic-playlists/main/playlists/arabic_general.m3u`
   (and the same for `arabic_kids.m3u`).

### Run it on your own computer

You need **Python 3.9 or newer**. No extra packages are required.

```bash
git clone https://github.com/spyzoro/iptv-arabic-playlists.git
cd iptv-arabic-playlists
python build.py
```

The new lists are written to the `playlists/` folder. Options:

| Option | Meaning |
|---|---|
| `--min 720` | Make the standard lists 720p or better too. The default is `480`. |
| `--hd 1080` | Change the cutoff of the `*_720p` lists (default `720`). Use `--hd 0` to skip them. |
| `--min 0` | Keep everything, even if the quality is unknown. |
| `--no-check` | Skip the "is it alive?" test. Faster, but may include dead links. |

The channel data is downloaded into a `data/` folder on the first run. Delete that folder to fetch fresh data.

### Customise

Open `build.py` and edit the settings at the top:

- `ARAB_COUNTRIES` is the list of countries treated as Arabic.
- `KIDS_CATS` is the categories that go into the Kids list.

---

## How it works

1. Downloads the open channel database from [iptv-org](https://github.com/iptv-org/iptv).
2. Keeps channels that broadcast in Arabic or come from Arab countries. Adult channels and closed channels are removed.
3. Fetches every stream to check it's alive and reads its real resolution.
4. Splits channels into Kids and General, keeps the best stream per channel, and writes the `.m3u` files (standard and HD).
5. A GitHub Actions workflow (`.github/workflows/rebuild.yml`) repeats this every Monday and commits the result.

---

## Disclaimer

This project **does not host or restream any content**. It only publishes a list of links that are already publicly listed in the [iptv-org](https://github.com/iptv-org/iptv) database. All channels belong to their respective owners. You are responsible for making sure that watching them is legal where you live. If you own a channel and want it removed, contact iptv-org, since it is the source of the data, or open an issue here.

## Credits

Channel data and logos: [iptv-org](https://github.com/iptv-org/iptv) (Unlicense).

Found a bug or a missing channel? Open an issue. Pull requests are welcome.
