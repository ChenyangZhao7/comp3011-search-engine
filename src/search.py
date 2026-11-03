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


def find_pages(index, query):
    """Find all pages containing all words in the query."""
    words = [w.lower() for w in query.split()]

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
