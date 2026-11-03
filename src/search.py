from indexer import tokenize


def print_word(index, word):
    """Print the inverted index entry for a given word."""
    word = word.lower()

    if word not in index:
        print(f"Word '{word}' not found in index.")
        return

    print(f"\nInverted index for '{word}':")
    print(f"{'URL':<60} {'Frequency':<12} {'Positions'}")
    print("-" * 90)

    for url, stats in index[word].items():
        positions_preview = str(stats['positions'][:5])
        if len(stats['positions']) > 5:
            positions_preview = positions_preview[:-1] + ", ...]"
        print(f"{url:<60} {stats['frequency']:<12} {positions_preview}")


def _count_phrase(index, words, url):
    """Count how many times words appear consecutively, in order, on a page."""
    positions = [set(index[word][url]["positions"]) for word in words]
    count = 0
    for start in positions[0]:
        if all((start + offset) in positions[offset]
               for offset in range(1, len(words))):
            count += 1
    return count


def find_pages(index, query):
    """Find all pages containing all words in the query."""
    words = tokenize(query)

    if not words:
        print("Error: empty query.")
        return

    # Find pages that contain ALL query words
    result_sets = []
    for word in words:
        if word not in index:
            print(f"Word '{word}' not found in index.")
            return
        result_sets.append(set(index[word].keys()))

    # Intersection of all result sets
    common_pages = result_sets[0]
    for s in result_sets[1:]:
        common_pages = common_pages.intersection(s)

    if not common_pages:
        print(f"No pages found containing all words: {words}")
        return

    print(f"\nPages containing {words}:")
    for url in sorted(common_pages):
        # Show combined frequency across all query words
        total_freq = sum(index[w][url]['frequency'] for w in words)
        print(f"  {url}  (total frequency: {total_freq})")


def find_phrase(index, query):
    """Find pages where all query words appear consecutively, in order."""
    words = tokenize(query)

    if not words:
        print("Error: empty query.")
        return

    for word in words:
        if word not in index:
            print(f"Word '{word}' not found in index.")
            return

    # Only pages containing every query word can contain the phrase
    common_pages = set(index[words[0]])
    for word in words[1:]:
        common_pages = common_pages.intersection(index[word])

    matches = []
    for url in common_pages:
        if len(words) == 1:
            count = index[words[0]][url]["frequency"]
        else:
            count = _count_phrase(index, words, url)
        if count:
            matches.append((url, count))

    phrase = " ".join(words)

    if not matches:
        print(f"No pages found containing phrase: {phrase}")
        return

    # Most frequent phrase first; break ties by URL for stable output
    matches.sort(key=lambda item: (-item[1], item[0]))

    print(f"\nPages containing phrase '{phrase}':")
    for url, count in matches:
        print(f"  {url}  (phrase frequency: {count})")
