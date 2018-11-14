class Tree:
    """
    Instances of this class are rooted trees with labels on the edges and values
    at the leaf nodes.
    An example of such a tree is a directory structure, where the labels are the
    names of the files and directories, and the values are the contents of the
    files.
    .. automethod:: __setitem__
    .. automethod:: __getitem__
    """

    def __init__(self):
        self._children = {}

    @staticmethod
    def from_items(items):
        """Create a tree from a sequence of (path, value) pairs.
        :param items: A sequence of (path, value) pairs.
        :returns: A tree.
        :rtype: Tree
        """
        t = Tree()
        for (path, value) in items:
            t[path] = value
        return t

    def __getitem__(self, path):
        """Get the value or the subtree at the node where the path
        ends.
        :param path: A single path segment, or a list of path segments.
        :returns: Either a tree, or a value at the leaf, depending on where the
                  path ends.
        """
        if not isinstance(path, list) and not isinstance(path, tuple):
            return self._children[path]
        if len(path) == 1:
            return self._children[path[0]]
        return self._children[path[0]].__getitem__(path[1:])

    def __setitem__(self, path, value):
        """Set the value for the leaf at the end of specified path.
        :param path: A single path segment, or a list of path segments at which
            to replace or set the value.
        :param value: The value at the leaf at the end of path.
        :returns: None
        """
        if not isinstance(path, list) and not isinstance(path, tuple):
            self._children[path] = value
        elif len(path) == 1:
            self._children[path[0]] = value
        else:
            child = self._children.setdefault(path[0], Tree())
            child.__setitem__(path[1:], value)

    def paths(self, prefix=None):
        """Return iterator over the maximal paths (from root to leaf) in the
        tree.
        :param prefix: List that gets prepended to every path.  Use `None` for
            the empty list.
        :rtype: An iterator.
        """
        return map(lambda p, _: p, self.items(prefix))

    def values(self):
        """Return iterator over the values at the leaves of the tree.
        :rtype: An iterator.
        """
        return map(lambda _, v: v, self.items())

    def items(self, prefix=None):
        """Return iterator over the (path, value) pairs in the tree, where path
        is a path from the root to a leaf, and value is the value at that leaf.
        :param prefix: List that gets prepended to every path.  Use `None` for
            the empty list.
        :rtype: An iterator.
        """
        prefix = prefix or []
        for (segment, t) in self._children.items():
            if isinstance(t, Tree):
                for p in t.items(prefix + [segment]):
                    yield p
            else:
                yield (prefix + [segment], t)
