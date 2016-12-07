#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module for generating a playlist for a sequence of segments.
"""
LIVE_FORMAT = """#EXTM3U
#EXT-X-TARGETDURATION:{target_duration}
#EXT-X-VERSION:3
#EXT-X-MEDIA-SEQUENCE:{sequence_number}
{sequences}"""

SEQUENCE_FORMAT = "#EXTINF:{0},\n{1}"


def generate_playlist(target_duration, sequence_number, sequences):
    sequence_string = "\n".join(SEQUENCE_FORMAT.format(d, u) for d, u in sequences)
    return LIVE_FORMAT.format(target_duration=target_duration,
                              sequence_number=sequence_number,
                              sequences=sequence_string)


def test_generator():
    segments = [(9.0, 'frag-1.ts'), (9.0, 'frag-2.ts'), (3.0, 'frag-3.ts')]
    assert generate_playlist(10, 3, segments) == """#EXTM3U
#EXT-X-TARGETDURATION:10
#EXT-X-VERSION:3
#EXT-X-MEDIA-SEQUENCE:3
#EXTINF:9.0,
frag-1.ts
#EXTINF:9.0,
frag-2.ts
#EXTINF:3.0,
frag-3.ts"""


if __name__ == '__main__':
    test_generator()
