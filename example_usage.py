"""Example usage for GenPark Suffix Tree Substring Search.
100% Python Standard Library.
"""

from client import SuffixTree

def main():
    tree = SuffixTree()
    document = "The generative AI ecosystem requires high-speed deterministic indexing and safe agent coordination."
    tree.build(document)
    
    offsets_ai = tree.search("AI")
    print("Matches for 'AI':", offsets_ai)
    
    offsets_agent = tree.search("agent")
    print("Matches for 'agent':", offsets_agent)
    
    print("Contains 'deterministic':", tree.contains("deterministic"))
    print("Contains 'quantum':", tree.contains("quantum"))

if __name__ == "__main__":
    main()
