# TVBox source audit (preliminary)

Audit date: 2026-11-19  
Repository: `LDeom/tvbox`  
Base: `master` at `641db3307d076547a383841491b17f9280433c5e`  
Working branch: `audit/repair-sources-2026-11`

## Repairs made on this branch

1. `0825.json`: repaired missing Wogg-style filter-data references by pointing them to the existing `./json/wogg.json`.
2. `js.json`: repaired the same missing filter-data references. Removed the active `西门[V2]` entry because its referenced `./js/西门[V2].js` script is absent from the repository.
3. `dianshi.json` and `tools/dianshi.json`: replaced the missing `./tv.txt` live-list path with the existing `./list.txt` playlist. The replacement uses the repository's existing channel-name/URL text format.

All four edited JSON files were parsed successfully after the changes. Their scanned local file references resolve against files in the repository.

## Playlist inventory (static parsing only)

URL counts below describe entries found in repository files; they do **not** mean the streams were reachable or playable during this audit.

| File | URL entries | Distinct hosts | Notes |
|---|---:|---:|---|
| `list.m3u` | 860 | 142 | General TV playlist |
| `list.txt` | 202 | 18 | General TV text playlist |
| `tvboxtv.txt` | 1,391 | 110 | General TV text playlist |
| `tvlive.txt` | 1,420 | 110 | General TV text playlist |
| `ITV.txt` | 637 | 1 | Single-provider domain |
| `radio.m3u` | 1,478 | 111 | Radio playlist |
| `radio.txt` | 1,478 | 111 | Same 1,456 unique stream URLs as `radio.m3u`, alternate format |

The two general TV files `tvboxtv.txt` and `tvlive.txt` share 1,387 distinct URLs. `tvlive.txt` has 32 URLs not found in `tvboxtv.txt`; `tvboxtv.txt` has 4 not found in `tvlive.txt`.

The repository also contains separate adult-content playlists/configuration. These have been classified separately and are not included in any proposed public mirror distribution.

## Other findings and cautions

- `listx.m3u` is **not empty**. The Git blob contains about 6.27 MB of data; a normal file-content read returned an empty result for this large file, so the blob was used to verify it.
- The `XYQ.json` reference to `XYQHiker/玩偶妹妹.json` is inside a commented-out entry, so it is not an active missing dependency.
- The percent-encoded path in `fty.json` resolves to the existing `FTY/兔小贝.js`.
- Some nested XBPQ/XYQHiker source files contain comments or trailing commas. A strict JSON parser rejects those forms, but that alone does not prove they are unusable; their expected parser behavior must be confirmed before rewriting them.
- Static URL parsing and local-reference checks do not validate DNS, HTTP responses, authentication, geo-restrictions, expiry, or media playback. Network probes from the audit environment failed at DNS resolution, so no stream is marked as playback-tested.
- The repository README disclaims accuracy/legality and explicitly warns against use within mainland China. No mainland mirror/CDN links are being generated until the rights and distribution constraints are resolved.

## Status

This is a preliminary static audit, not a certification that every source works. No changes have been made to `master`; all repairs are isolated on the working branch for review.
