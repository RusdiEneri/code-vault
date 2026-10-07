class PrefixTree:
    def __init__(self):
        self.trie = {}
    def add(self, s):
        curr = self.trie
        for c in s:
            curr = curr.setdefault(c, {})
        curr['#'] = True
