"""Priority Set"""

__all__ = ['Prioset']

import heapq

class Prioset:
    """Priority Set
    Provides a priority queue implemented with sets for faster insertion & membership checking
    """
    def __init__(self):
        self._sets = {0: set()}
        self._prios = [0]

    def add(self, item, prio):
        """Add a new item with associated priority level

        item -- item to add
        prio -- priority of item to add
        """
        if prio in self._sets:
            self._sets[prio].add(item)
            return
        self._sets[prio] = {item}
        heapq.heappush(self._prios, prio)

    def pop(self):
        """Retrieve a random item from the minimum priority level

        Returns item and its associated priority level
        """
        if not self._prios:
            raise IndexError('No values to pop')
        prio = self._prios[0]
        item = self._sets[prio].pop()
        if not self._sets[prio]:
            heapq.heappop(self._prios)
            del self._sets[prio]
        return item, prio

    def prios(self):
        """Get the list of priority levels present"""
        return sorted(self._prios)

    def __bool__(self):
        """Returns true if any priority levels are present"""
        return bool(self._prios)

    def __len__(self):
        """Returns total count of all contained items"""
        return sum(len(s) for s in self._sets.values())

    def __contains__(self, key):
        """Checks for given item in all priority levels"""
        for s in self._sets.values():
            if key in s:
                return True
        return False

    def __getitem__(self, key):
        """Returns the set of items for a given priority level"""
        if key in self._sets:
            return self._sets[key]
        raise ValueError(f'Priority level {key} not present')
