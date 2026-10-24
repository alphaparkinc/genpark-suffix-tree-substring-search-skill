"""Suffix Tree Substring Search Engine.
100% Python Standard Library.
"""

from typing import Dict, List, Any

class SuffixTreeNode:
    def __init__(self):
        self.children: Dict[str, "SuffixTreeNode"] = {}
        self.indexes: List[int] = []

class SuffixTree:
    """Full-text indexing tree providing exact substring match discovery and offset extraction."""

    def __init__(self):
        self.root = SuffixTreeNode()
        self.text = ""

    def build(self, text: str):
        self.text = text
        self.root = SuffixTreeNode()
        n = len(text)
        for i in range(n):
            curr = self.root
            curr.indexes.append(i)
            for j in range(i, n):
                char = text[j]
                if char not in curr.children:
                    curr.children[char] = SuffixTreeNode()
                curr = curr.children[char]
                curr.indexes.append(i)

    def search(self, pattern: str) -> List[int]:
        if not pattern or not self.text:
            return []
        curr = self.root
        for char in pattern:
            if char not in curr.children:
                return []
            curr = curr.children[char]
        return sorted(list(set(curr.indexes)))

    def contains(self, pattern: str) -> bool:
        return len(self.search(pattern)) > 0
