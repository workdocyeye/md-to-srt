---
name: md-to-srt
description: Generate SRT subtitle files from markdown content. Use this skill when users request converting markdown files to subtitles, creating captions for video content, or need to transform text scripts into timed subtitle format. This skill handles text segmentation, timing calculation, and SRT formatting automatically.
---

# Markdown to SRT Subtitle Generator

## Overview

Convert markdown documents into properly formatted SRT (SubRip) subtitle files with intelligent text segmentation, automatic timing calculation, and optimal display durations. This skill transforms text content into video-ready subtitles with appropriate character limits, reading speeds, and timing gaps.

## Quick Start

To convert a markdown file to SRT subtitles, use the provided Python script:

```bash
python scripts/md_to_srt.py input.md -o output.srt
```

The script automatically:
- Parses markdown content (headers, paragraphs, lists)
- Splits text into appropriate subtitle segments (max 30 characters by default)
- Calculates display duration based on reading speed (4.0 chars/second by default)
- Subtitles play continuously without gaps (each starts when previous ends)
- Outputs properly formatted SRT file

## Core Parameters

Adjust these parameters based on content type and audience:

### Character Limits

- **Default**: 30 characters per subtitle line
- **Fast-paced content**: 20-25 characters
- **Educational content**: 35-40 characters
- **Technical content**: 25-30 characters (allow reading time)

Modify with `--max-chars` parameter:
```bash
python scripts/md_to_srt.py input.md --max-chars 25
```

### Reading Speed

**⭐ DEFAULT & RECOMMENDED: 4.0 chars/sec (舒适阅读速度)**

This speed provides optimal reading time for most content. **Use this unless specifically requested otherwise.**

Controls how fast subtitles display (characters per second):
- **Default (推荐)**: 4.0 chars/sec (舒适阅读，适合绝大多数内容)
- **Faster**: 6-8 chars/sec (for quick readers, simple content)
- **Slower**: 2-3 chars/sec (for complex topics, detailed explanations)

Modify with `--reading-speed` parameter:
```bash
python scripts/md_to_srt.py input.md --reading-speed 4.0
```

**💡 Important**: Unless user explicitly requests different speed, always use 4.0 chars/sec.

### Timing Gaps

⚠️ **Note**: Current implementation does not add timing gaps between subtitles. Each subtitle starts immediately after the previous one ends (continuous playback).

The `--gap-min` and `--gap-max` parameters are defined but not yet implemented in the script. Subtitles play back-to-back without pauses.

## Usage Examples

### Example 1: Standard Content (Recommended)

Use default settings for normal video content:

```bash
python scripts/md_to_srt.py content.md
```

This uses the recommended reading speed (4.0 chars/sec) and 30 characters per line. Suitable for most content.

### Example 2: Tutorial Video Script

Convert a detailed tutorial markdown with technical explanations:

```bash
python scripts/md_to_srt.py tutorial.md -o tutorial.srt \
  --max-chars 25 \
  --reading-speed 3.0
```

This creates even slower-paced subtitles suitable for learning complex technical content.

### Example 3: Fast-Paced Overview

Convert a quick overview or summary:

```bash
python scripts/md_to_srt.py overview.md -o overview.srt \
  --max-chars 35 \
  --reading-speed 6.0
```

This creates faster, information-dense subtitles while maintaining readability.

## Text Processing Rules

The script automatically handles common markdown patterns:

### Headers

Convert headers to regular subtitle text:
```markdown
# Introduction to AI
## What is Machine Learning?
```
Becomes:
```
1
00:00:00,000 --> 00:00:02,500
Introduction to AI

2
00:00:02,800 --> 00:00:05,300
What is Machine Learning?
```

### Lists

Preserves list structure as separate subtitles:
```markdown
- First point
- Second point
- Third point
```

Each bullet point becomes a separate subtitle entry.

### Long Paragraphs

Automatically splits long text at sentence boundaries and phrase breaks:
- Splits at periods, question marks, exclamation points
- Further splits at commas if still too long
- Maintains logical flow and readability

## Troubleshooting

### Subtitles Too Fast/Slow

**Problem**: Viewers can't read in time or subtitles feel too slow

**Solutions**:
- Adjust `--reading-speed` parameter (lower = slower)
- Reduce `--max-chars` for shorter segments
- Increase minimum duration by modifying script

### Text Breaks Awkwardly

**Problem**: Subtitles break at unnatural points

**Solutions**:
- Reduce `--max-chars` to force shorter segments
- Edit source markdown to add punctuation (commas, periods) at preferred break points
- Manually edit the generated SRT file

### Encoding Issues

**Problem**: Special characters display incorrectly

**Solutions**:
- Script automatically saves with UTF-8 encoding
- Ensure markdown source file is UTF-8 encoded
- Test with different video players

### Missing Content

**Problem**: Some content not included in subtitles

**Solutions**:
- Code blocks (```) are currently skipped by design
- Empty lines are skipped
- Check that content isn't in skipped markdown patterns

## Manual Adjustments

After generating the SRT file, manual adjustments may be needed:

1. **Timing adjustments**: Open in text editor and adjust timestamps
2. **Text refinement**: Improve phrasing or fix awkward breaks
3. **Merge entries**: Combine consecutive short subtitles
4. **Split entries**: Break up long or complex subtitles

## SRT Format Reference

For detailed information about SRT format specifications, best practices, and guidelines, consult the reference documentation:

`references/srt_format_guide.md`

This reference includes:
- Complete SRT format structure
- Time format specifications
- Character limit guidelines
- Duration and timing best practices
- Common issues and solutions

## Advanced Customization

For specific requirements beyond parameter adjustments, modify the `SRTGenerator` class in `scripts/md_to_srt.py`:

- Adjust minimum duration calculation
- Customize text splitting logic
- Add special handling for specific markdown patterns
- Implement custom timing strategies

## Integration Workflow

When users request subtitle generation:

1. **Identify source**: Locate the markdown file to convert
2. **Use default settings**: Always start with reading-speed=4.0 unless user explicitly requests otherwise
3. **Generate SRT**: Run the script with default parameters
```bash
python scripts/md_to_srt.py input.md -o output.srt
```
4. **Review output**: Check generated SRT file for quality
5. **Adjust only if requested**: If user asks for different speed, adjust `--reading-speed` parameter
6. **Manual polish**: Make final adjustments for optimal viewer experience

**⭐ Remember**: Default to 4.0 chars/sec reading speed. This is the recommended setting for optimal readability.
