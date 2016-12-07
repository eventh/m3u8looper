#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module for parsing the content of a m3u8 playlist.

To find the duration and path to ts segments.
"""
import os.path

START_TAG = "#EXTM3U"
TARGET_DURATION_TAG = "#EXT-X-TARGETDURATION:"
SEGMENT_TAG = "#EXTINF:"
OTHER_KNOWN_TAGS = {"", "#EXT-X-ENDLIST", "#EXT-X-VERSION:3"}


def load_playlists(playlist_paths, out_path):
    """Read input playlists for all segments."""
    max_target_duration = 0
    all_segments = []
    for path in playlist_paths:
        with open(path, 'r') as f:
            lines = f.readlines()

        target_duration, segments = parse_playlist(lines, path)
        if target_duration and segments:
            all_segments += _modify_segment_paths(segments, path, out_path)
            max_target_duration = max(max_target_duration, target_duration)
        
    return max_target_duration, all_segments


def parse_playlist(lines, path):
    valid_playlist = False
    target_duration = None
    segment_duration = None
    segments = []

    for line in lines:
        line = line.strip()
        if START_TAG in line:
            valid_playlist = True
        elif TARGET_DURATION_TAG in line:
            target_duration = _parse_target_duration(line, path)
        elif line.startswith(SEGMENT_TAG):
            segment_duration = _parse_duration(line, path)
        elif segment_duration != None:
            segments.append((segment_duration, line))
            segment_duration = None
        elif line not in OTHER_KNOWN_TAGS:
            print("Unknown line in playlist %s: %s" % (path, line))

    if target_duration is None or not valid_playlist:
        raise IOError("Not valid m3u8 playlist: %s" % path)

    return target_duration, segments


def _parse_target_duration(line, path):
    value_str = line.split(TARGET_DURATION_TAG)[1].strip()
    return _parse_float(value_str, path, 'target')


def _parse_duration(line, path):
    value_str = line.split(SEGMENT_TAG)[1].split(',')[0]
    return _parse_float(value_str, path, 'target')


def _parse_float(value, path, type_):
    try:
        return float(value)
    except ValueError as exc:
        print("Invalid %s duration %s: %s" % (type_, path, exc))


def _modify_segment_paths(segments, playlist_path, out_path):
    """If the playlist is a file and not url, add path prefix to output segments."""
    if not os.path.isfile(playlist_path):
        return segments
    prefix = os.path.relpath(os.path.dirname(playlist_path), os.path.dirname(out_path))
    return [(dur, os.path.join(prefix, url)) for dur, url in segments]


def test_parser():
    TEST_INPUT = """
#EXTM3U
#EXT-X-TARGETDURATION:9
#EXT-X-VERSION:3
#EXTINF:9,
frag-1.ts
#EXTINF:9,
frag-2.ts
#EXTINF:9,
frag-3.ts
#EXTINF:9,
frag-4.ts
#EXTINF:9,
frag-5.ts
#EXTINF:4,
frag-6.ts
#EXT-X-ENDLIST
"""
    duration, segments = parse_playlist(TEST_INPUT.split('\n'), 'test.m3u8')
    assert duration == 9.0
    assert segments == [(9.0, 'frag-1.ts'), (9.0, 'frag-2.ts'), (9.0, 'frag-3.ts'), (9.0, 'frag-4.ts'), (9.0, 'frag-5.ts'), (4.0, 'frag-6.ts')]


if __name__ == '__main__':
    test_parser()
