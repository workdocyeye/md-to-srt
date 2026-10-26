#!/usr/bin/env python3
"""
Markdown to SRT Subtitle Generator

This script converts markdown files to SRT subtitle format with intelligent
text segmentation and timing calculation.
"""

import re
import sys
import argparse
from pathlib import Path
from typing import List, Tuple


# 词内标点的占位符：切分时先保护、切完再还原。
# 等长替换（1 char -> 1 char），不影响字数统计和时长计算。
DOT = '\x00'    # opencode.json / v1.5.2 / example.com / 3.0
COMMA = '\x01'  # 1,000


class SRTGenerator:
    """Generate SRT subtitles from markdown content."""

    def __init__(
        self,
        max_chars: int = 30,
        reading_speed: float = 4.0,  # characters per second (slower for longer display)
        gap_min: float = 0.3,
        gap_max: float = 0.6
    ):
        """
        Initialize the SRT generator.

        Args:
            max_chars: Maximum characters per subtitle line
            reading_speed: Reading speed in characters per second
            gap_min: Minimum gap between subtitles in seconds
            gap_max: Maximum gap between subtitles in seconds
        """
        self.max_chars = max_chars
        self.reading_speed = reading_speed
        self.gap_min = gap_min
        self.gap_max = gap_max

    def parse_markdown(self, content: str) -> List[str]:
        """
        Parse markdown content into segments.

        Args:
            content: Raw markdown content

        Returns:
            List of text segments
        """
        segments = []

        # Split by lines
        lines = content.split('\n')

        for line in lines:
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Skip code blocks for now (can be enhanced later)
            if line.startswith('```'):
                continue

            # Handle headers - add as segments
            if line.startswith('#'):
                # Remove # symbols and whitespace
                header_text = re.sub(r'^#+\s*', '', line)
                if header_text:
                    segments.append(header_text)
                continue

            # Handle list items
            if line.startswith(('-', '*', '+')):
                list_text = re.sub(r'^[-*+]\s*', '', line)
                if list_text:
                    segments.append(list_text)
                continue

            # Handle numbered lists
            if re.match(r'^\d+\.\s*', line):
                num_text = re.sub(r'^\d+\.\s*', '', line)
                if num_text:
                    segments.append(num_text)
                continue

            # Regular paragraph text - add as is
            segments.append(line)

        return segments

    def split_segment(self, text: str) -> List[str]:
        """
        Split a text segment into multiple subtitle lines if needed.

        Args:
            text: Text segment to split

        Returns:
            List of subtitle lines
        """
        if len(text) <= self.max_chars:
            return [text]

        # 词内标点不算句界，先换成等长占位符再切分：
        #   opencode.json / v1.5.2 / example.com / 3.0  -> 英文点不切
        #   1,000                                       -> 千分位逗号不切
        protected = re.sub(r'(?<=[A-Za-z0-9])\.(?=[A-Za-z0-9])', DOT, text)
        protected = re.sub(r'(?<=\d),(?=\d)', COMMA, protected)

        # Need to split the text
        lines = []
        current_line = ""

        # Split by sentences first
        sentences = re.split(r'([。！？.!?])', protected)

        i = 0
        while i < len(sentences):
            sentence = sentences[i]

            # Add punctuation back if it exists
            if i + 1 < len(sentences) and sentences[i + 1] in '。！？.!?':
                sentence += sentences[i + 1]
                i += 2
            else:
                i += 1

            sentence = sentence.strip()
            if not sentence:
                continue

            # Check if adding this sentence would exceed max_chars
            if len(current_line) + len(sentence) <= self.max_chars:
                if current_line:
                    current_line += sentence
                else:
                    current_line = sentence
            else:
                # Save current line if it exists
                if current_line:
                    lines.append(current_line)

                # Check if sentence itself is too long
                if len(sentence) <= self.max_chars:
                    current_line = sentence
                else:
                    # Split long sentence by phrases
                    phrases = re.split(r'([，,、;；])', sentence)
                    temp_line = ""

                    for j in range(0, len(phrases), 2):
                        phrase = phrases[j]
                        # Add punctuation if it exists
                        if j + 1 < len(phrases):
                            phrase += phrases[j + 1]

                        if len(temp_line) + len(phrase) <= self.max_chars:
                            temp_line += phrase
                        else:
                            if temp_line:
                                lines.append(temp_line)
                            temp_line = phrase

                    current_line = temp_line

        # Add remaining content
        if current_line:
            lines.append(current_line)

        # 还原受保护的词内标点
        return [line.replace(DOT, '.').replace(COMMA, ',') for line in lines]

    def calculate_duration(self, text: str) -> float:
        """
        Calculate display duration for a text segment.

        Args:
            text: Text segment

        Returns:
            Duration in seconds
        """
        char_count = len(text)
        duration = char_count / self.reading_speed

        return round(duration, 2)

    def format_time(self, seconds: float) -> str:
        """
        Convert seconds to SRT time format.

        Args:
            seconds: Time in seconds

        Returns:
            Formatted time string (HH:MM:SS,mmm)
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds % 1) * 1000)

        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"

    def generate_srt(self, markdown_content: str) -> str:
        """
        Generate SRT content from markdown.

        Args:
            markdown_content: Raw markdown content

        Returns:
            SRT formatted content
        """
        # Parse markdown into segments
        segments = self.parse_markdown(markdown_content)

        # Split segments into subtitle lines
        subtitle_lines = []
        for segment in segments:
            lines = self.split_segment(segment)
            subtitle_lines.extend(lines)

        # Generate SRT entries
        srt_entries = []
        current_time = 0.0

        for i, line in enumerate(subtitle_lines, 1):
            # Calculate duration
            duration = self.calculate_duration(line)

            # Format times
            start_time = self.format_time(current_time)
            end_time = self.format_time(current_time + duration)

            # Create SRT entry
            entry = f"{i}\n{start_time} --> {end_time}\n{line}\n"
            srt_entries.append(entry)

            current_time += duration

        return '\n'.join(srt_entries)


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Convert markdown file to SRT subtitles'
    )
    parser.add_argument(
        'input_file',
        type=Path,
        help='Input markdown file path'
    )
    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=None,
        help='Output SRT file path (default: input_file.srt)'
    )
    parser.add_argument(
        '--max-chars',
        type=int,
        default=30,
        help='Maximum characters per subtitle line (default: 30)'
    )
    parser.add_argument(
        '--reading-speed',
        type=float,
        default=4.0,
        help='Reading speed in characters per second (default: 4.0 - slower for longer display)'
    )
    parser.add_argument(
        '--gap-min',
        type=float,
        default=0.3,
        help='Minimum gap between subtitles in seconds (default: 0.3)'
    )
    parser.add_argument(
        '--gap-max',
        type=float,
        default=0.6,
        help='Maximum gap between subtitles in seconds (default: 0.6)'
    )

    args = parser.parse_args()

    # Validate input file
    if not args.input_file.exists():
        print(f"Error: Input file '{args.input_file}' does not exist.", file=sys.stderr)
        sys.exit(1)

    # Determine output file
    if args.output is None:
        args.output = args.input_file.with_suffix('.srt')

    # Read markdown content
    with open(args.input_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    # Generate SRT
    generator = SRTGenerator(
        max_chars=args.max_chars,
        reading_speed=args.reading_speed,
        gap_min=args.gap_min,
        gap_max=args.gap_max
    )

    srt_content = generator.generate_srt(markdown_content)

    # Write SRT file
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(srt_content)

    print(f"✅ Generated SRT file: {args.output}")
    print(f"   Input: {args.input_file}")
    print(f"   Output: {args.output}")
    print(f"   Max chars per line: {args.max_chars}")
    print(f"   Reading speed: {args.reading_speed} chars/sec")


if __name__ == '__main__':
    main()
