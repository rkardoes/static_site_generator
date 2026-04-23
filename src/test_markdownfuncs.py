import unittest

from markdownfuncs import BlockType, extract_markdown_images, extract_markdown_links, markdown_to_blocks, block_to_block_type, extract_title

class TestMarkdownFunctions(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches2 = extract_markdown_links(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches2)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        md = """
# Heading1

## Heading2

This is **bolded** paragraph



So many extra lines







This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading1",
                "## Heading2",
                "This is **bolded** paragraph",
                "So many extra lines",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        
        md = """
# Heading1

## Heading2

####### Fake Heading

This is **bolded** paragraph



So many extra lines




```
This is a code block
```

1. Ordered
2. List
3. YES

1. Broken
2. Ordered
5. List

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

> This is a
> Quote block
"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            [BlockType.HEADING,
             BlockType.HEADING,
             BlockType.PARAGRAPH,
             BlockType.PARAGRAPH,
             BlockType.PARAGRAPH,
             BlockType.CODE,
             BlockType.O_LIST,
             BlockType.PARAGRAPH,
             BlockType.PARAGRAPH,
             BlockType.UO_LIST,
             BlockType.QUOTE,
             ],
             [block_to_block_type(b) for b in blocks]
        )

    def test_extract_title(self):
        md = """
This is a test

# Header test please work

Hopefully this is fine
"""
        self.assertEqual(
            extract_title(md),
            "Header test please work"
        )

        md = """
This is a test

# Header test please work

# Hopefully this is fine
"""
        self.assertEqual(
            extract_title(md),
            "Header test please work"
        )