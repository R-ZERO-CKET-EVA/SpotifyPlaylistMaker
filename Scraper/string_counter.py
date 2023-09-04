from typing import List, Dict

class StringCounter:
    def __init__(self):
        pass

    def count_strings(self, strings: List[str]) -> Dict[str, int]:
        counts = {}

        for string in strings:
            if string in counts:
                counts[string] += 1
            else:
                counts[string] = 1

        return counts
