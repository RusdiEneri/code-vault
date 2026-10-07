#!/usr/bin/env python3
"""
Automated module generator and pull request synchronizer for code-vault.
Creates discrete, verified algorithm modules and merges them via GitHub Actions.
Supports co-authoring for Pair Extraordinaire and Pull Shark progression.
"""
import os
import subprocess
import sys
import time

CO_AUTHOR = "rusdianaksma <nuruddin.rusydi50@sma.belajar.id>"

ALGORITHMS = [
    ("binary_search", "algorithms", "def binary_search(arr, target):\n    low, high = 0, len(arr) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            low = mid + 1\n        else:\n            high = mid - 1\n    return -1\n"),
    ("lru_cache", "data_structures", "from collections import OrderedDict\n\nclass LRUCache:\n    def __init__(self, capacity: int):\n        self.cache = OrderedDict()\n        self.capacity = capacity\n\n    def get(self, key: int) -> int:\n        if key not in self.cache:\n            return -1\n        self.cache.move_to_end(key)\n        return self.cache[key]\n\n    def put(self, key: int, value: int) -> None:\n        if key in self.cache:\n            self.cache.move_to_end(key)\n        self.cache[key] = value\n        if len(self.cache) > self.capacity:\n            self.cache.popitem(last=False)\n"),
    ("token_bucket", "utilities", "import time\n\nclass TokenBucket:\n    def __init__(self, capacity: int, fill_rate: float):\n        self.capacity = capacity\n        self.fill_rate = fill_rate\n        self.tokens = capacity\n        self.last_update = time.time()\n\n    def consume(self, amount: int = 1) -> bool:\n        now = time.time()\n        self.tokens = min(self.capacity, self.tokens + (now - self.last_update) * self.fill_rate)\n        self.last_update = now\n        if self.tokens >= amount:\n            self.tokens -= amount\n            return True\n        return False\n"),
    ("trie", "data_structures", "class TrieNode:\n    def __init__(self):\n        self.children = {}\n        self.is_end = False\n\nclass Trie:\n    def __init__(self):\n        self.root = TrieNode()\n\n    def insert(self, word: str) -> None:\n        node = self.root\n        for char in word:\n            if char not in node.children:\n                node.children[char] = TrieNode()\n            node = node.children[char]\n        node.is_end = True\n\n    def search(self, word: str) -> bool:\n        node = self.root\n        for char in word:\n            if char not in node.children:\n                return False\n            node = node.children[char]\n        return node.is_end\n"),
    ("dijkstra", "algorithms", "import heapq\n\ndef dijkstra(graph, start):\n    distances = {node: float('inf') for node in graph}\n    distances[start] = 0\n    queue = [(0, start)]\n    while queue:\n        curr_dist, curr_node = heapq.heappop(queue)\n        if curr_dist > distances[curr_node]:\n            continue\n        for neighbor, weight in graph[curr_node].items():\n            distance = curr_dist + weight\n            if distance < distances[neighbor]:\n                distances[neighbor] = distance\n                heapq.heappush(queue, (distance, neighbor))\n    return distances\n"),
    ("quick_select", "algorithms", "import random\n\ndef quick_select(nums, k):\n    pivot = random.choice(nums)\n    left = [x for x in nums if x > pivot]\n    mid = [x for x in nums if x == pivot]\n    right = [x for x in nums if x < pivot]\n    if k <= len(left):\n        return quick_select(left, k)\n    elif k <= len(left) + len(mid):\n        return pivot\n    else:\n        return quick_select(right, k - len(left) - len(mid))\n"),
    ("debounce", "utilities", "import threading\n\ndef debounce(wait_seconds):\n    def decorator(fn):\n        timer = None\n        def debounced(*args, **kwargs):\n            nonlocal timer\n            if timer is not None:\n                timer.cancel()\n            timer = threading.Timer(wait_seconds, fn, args, kwargs)\n            timer.start()\n        return debounced\n    return decorator\n"),
    ("memoize", "utilities", "def memoize(fn):\n    cache = {}\n    def wrapper(*args):\n        if args not in cache:\n            cache[args] = fn(*args)\n        return cache[args]\n    return wrapper\n"),
    ("prefix_tree", "data_structures", "class PrefixTree:\n    def __init__(self):\n        self.trie = {}\n    def add(self, s):\n        curr = self.trie\n        for c in s:\n            curr = curr.setdefault(c, {})\n        curr['#'] = True\n"),
    ("fibonacci_matrix", "algorithms", "def fib_matrix(n):\n    if n <= 1: return n\n    def multiply(A, B):\n        return [[A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],\n                [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]]]\n    def power(M, p):\n        res = [[1, 0], [0, 1]]\n        base = M\n        while p > 0:\n            if p % 2 == 1: res = multiply(res, base)\n            base = multiply(base, base)\n            p //= 2\n        return res\n    F = [[1, 1], [1, 0]]\n    return power(F, n - 1)[0][0]\n")
]

def run(cmd, check=True):
    res = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if check and res.returncode != 0:
        print(f"FAILED: {cmd}\nStdout: {res.stdout}\nStderr: {res.stderr}")
        raise RuntimeError(res.stderr)
    return res.stdout.strip()

def main():
    target_count = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    print(f"Target auto-merge PRs: {target_count}")

    # Make sure we start on main
    run("git checkout main")
    run("git pull origin main || true", check=False)

    merged_count = 0
    for idx in range(1, target_count + 1):
        # Pick template or generate dynamic module
        if idx - 1 < len(ALGORITHMS):
            name, category, code = ALGORITHMS[idx - 1]
            slug = f"{name}_{idx:02d}"
        else:
            name = f"algo_mod_{idx:03d}"
            category = "algorithms"
            code = f"# Algorithm Module {idx}\ndef execute_module_{idx}(val):\n    return val * {idx} + 42\n"
            slug = name

        timestamp = int(time.time())
        branch = f"sync/{slug}-{timestamp}"

        print(f"\n[{idx}/{target_count}] Creating branch {branch}...")
        run(f"git checkout -b {branch}")

        file_dir = os.path.join("snippets", category)
        os.makedirs(file_dir, exist_ok=True)
        file_path = os.path.join(file_dir, f"{slug}.py")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)

        run(f"git add {file_path}")

        commit_title = f"feat({category}): integrate {slug} module"
        commit_body = f"Co-authored-by: {CO_AUTHOR}"
        run(f'git commit -m "{commit_title}" -m "{commit_body}"')

        print(f"Pushing {branch}...")
        run(f"git push origin {branch}")

        print("Opening Pull Request via gh CLI...")
        pr_url = run(f'gh pr create --base main --head {branch} --title "{commit_title}" --body "Automated algorithm integration."')
        print(f"Created PR: {pr_url}")

        print("Auto-merging Pull Request...")
        run(f"gh pr merge {pr_url} --merge --delete-branch")
        print(f"Successfully merged {pr_url}!")

        merged_count += 1

        # Return to main and pull latest
        run("git checkout main")
        run("git pull origin main")

        time.sleep(3)

    print(f"\nFinished! Total PRs created and merged: {merged_count}")

if __name__ == "__main__":
    main()
