import json
import os
from .azure_blob import download_text_if_exists

_cache = {}


def _load_local(path: str):
    with open(path, 'r') as f:
        return json.load(f)


# path_or_blob examples:
# 'data/ranges/preflop_live_fullring_100bb.json' or blob path
def load_ranges(path_or_blob: str):
    if path_or_blob in _cache:
        return _cache[path_or_blob]

    if os.path.exists(path_or_blob):
        data = _load_local(path_or_blob)
    else:
        txt = download_text_if_exists(path_or_blob)
        data = json.loads(txt) if txt else {}

    _cache[path_or_blob] = data
    return data


# Helper to check if combo is in the chart (e.g. 'AKs', 'QJo', '77')
def in_range(ranges: dict, position: str, combo: str) -> bool:
    pos = ranges.get(position.upper(), {})
    return combo in pos.get('open', [])
