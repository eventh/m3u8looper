#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module for serving loop of ts segments playlist.
"""
import sys
import time

from m3u8_generator import generate_playlist
from m3u8_parser import load_playlists
from serve_files import start_http_server

SEQUENCES_IN_A_PLAYLIST = 5


def serve_playlist(out_path, target_duration, all_segments):
    """Continuesly write output playlist to 'out_path'."""
    sequence_number = 0

    try:
        while True:
            segments = get_sequence_window(all_segments, sequence_number)            
            content = generate_playlist(target_duration, sequence_number, segments)

            with open(out_path, "w") as f:
                f.write(content)
            
            sequence_number += 1
            time.sleep(segments[0][0] if segments else 1)
            
    except KeyboardInterrupt:
        print("Shutting down..")


def get_sequence_window(all_segments, sequence_number):
    """Get the segments to include in the current playlist iteration."""
    first = sequence_number % len(all_segments)
    last = first + SEQUENCES_IN_A_PLAYLIST
    segments = all_segments[first:last]

    # Fill up wrapped all_sequences until we have enough
    while all_segments and len(segments) < SEQUENCES_IN_A_PLAYLIST:
        segments += all_segments[0:SEQUENCES_IN_A_PLAYLIST-len(segments)]

    #print("[%s] %s" % (first, ",".join(os.path.basename(i) for _, i in segments)))
    
    return segments


def main(out_path, *playlist_paths):
    if not playlist_paths:
        print("Usage: python looper.py <out.m3u8> <url.m3u8>...")
        sys.exit(1)
        
    target_duration, all_segments = load_playlists(playlist_paths, out_path)
    start_http_server()
    serve_playlist(out_path, target_duration, all_segments)


if __name__ == '__main__':
    main(*sys.argv[1:])
