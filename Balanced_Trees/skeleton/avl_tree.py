from avl_node import AVLNode


class AVLTree:
    class NodeGroup:
        def __init__(self):
            self.a = None
            self.b = None
            self.c = None
            self.t0 = None
            self.t1 = None
            self.t2 = None
            self.t3 = None

    def __init__(self):
        self.root = None
        self.size = 0
        self.to_restruct = None

    def get_tree_root(self):
        """
        Method to get the root node of the AVLTree
        :return AVLNode -- the root node of the AVL tree
        """
        return self.root


    def get_tree_height(self):
        """Retrieves tree height.
        :return -1 in case of empty tree, current tree height otherwise.
        """
        if self.root is None:
            return -1
        else:
            return self.root.height


    def get_tree_size(self):
        """Return number of key/value pairs in the tree.
        :return Number of key/value pairs.
        """
        return self.size


    def find_by_key(self, key):
        """Returns value of node with given key.
        :param key: Key to search.
        :return Corresponding value if key was found, None otherwise.
        :raises ValueError if the key is None
        """
        if key is None:
            raise ValueError("Cannot search for null key!")
        current = self.root
        while current is not None:
            if current.key == key:
                return current.value
            elif current.key < key:
                current = current.right
            else:
                current = current.left

        return None


    def insert(self, key, value):
        """Inserts a new node into AVL tree.
        :param key: Key of the new node.
        :param value: Data of the new node. Must not be None. Nodes with the same key
        are not allowed. In this case False is returned. None-Keys and None-Values are
        not allowed. In this case an error is raised.
        :return True if the insert was successful, False otherwise.
        :raises ValueError if the key or value is None.
        """
        if key is None:
            raise ValueError("Null keys are not allowed!")

        if self.root is None:
            self.root = AVLNode(key, value)
            self.update_height(self.root)
            inserted = self.root
        else:
            current = self.root
            while True:
                if current.key == key:
                    return False
                elif current.key < key:
                    if current.right is not None:
                        current = current.right
                    else:
                        self.set_right(current, AVLNode(key, value))
                        self.update_height(current)
                        inserted = current
                        break
                else:
                    if current.left is not None:
                        current = current.left
                    else:
                        self.set_left(current, AVLNode(key, value))
                        self.update_height(current)
                        inserted = current
                        break
        self.size += 1
        current_1 = inserted
        while current_1 is not None:
            current_1.height = self.update_height(current_1)
            current_1 = self.restructure(current_1)
            current_1 = current_1.parent
        return True


    def remove_by_key(self, key):
        """Removes node with given key.
        :param key: Key of node to remove.
        :return True If node was found and deleted, False otherwise.
        @raises ValueError if the key is None.
        """
        if key is None:
            raise ValueError("Null key is not allowed!")

        parent = None
        current = self.root
        new_sub_root = None

        while not (current is None):
            if current.key == key:
                if parent is None:
                    self.root = self._remove_bst(current)
                    if self.root is not None:
                        self.root.parent = None
                elif parent.left == current:
                    new_sub_root = self._remove_bst(current)
                    self.set_left(parent, new_sub_root)
                elif parent.right == current:
                    new_sub_root = self._remove_bst(current)
                    self.set_right(parent, new_sub_root)
                else:
                    raise ValueError()

                self.size -= 1
                if self.to_restruct is not None:
                    current = self.to_restruct
                    while current is not None:
                        current.height = self.update_height(current)
                        balance_check = self.get_balance(current)
                        if balance_check > 1 or balance_check < -1:
                            current = self.restructure(current)
                            current = current.parent
                        else:
                            current = current.parent
                return True
            else:
                parent = current
                if current.key > key:
                    current = current.left
                else:
                    current = current.right

        return False

    #auxiliary functions
    def get_current_node_height(self, node):
        if node is None:
            return -1
        else:
            return node.height
    def get_balance(self, node):
        if node is None:
            return 0
        else:
            return self.get_current_node_height(node.left) - self.get_current_node_height(node.right)
    def update_height(self, node):
        if node is None:
            return -1
        else:
            return 1 + max(self.get_current_node_height(node.left), self.get_current_node_height(node.right))

    def restructure(self, node):
        if node is None:
            return node

        node.height = self.update_height(node)
        balance = self.get_balance(node)

        if balance > 1:
            if self.get_balance(node.left) >= 0:
                return self.right_rotate(node)
            else:
                node.left = self.left_rotate(node.left)
                return self.right_rotate(node)
        elif balance < -1:
            if self.get_balance(node.right) <= 0:
                return self.left_rotate(node)
            else:
                node.right = self.right_rotate(node.right)
                return self.left_rotate(node)

        return node
    def left_rotate(self, node):
        new_node = node.right
        node.right = new_node.left
        if new_node.left is not None:
            new_node.left.parent = node
        new_node.parent = node.parent
        if node.parent is None:
            self.root = new_node
        elif node.parent.left == node:
            node.parent.left = new_node
        else:
            node.parent.right = new_node
        new_node.left = node
        node.parent = new_node
        node.height = self.update_height(node)
        new_node.height = self.update_height(new_node)
        return new_node
    def right_rotate(self, node):
        new_node = node.left
        node.left = new_node.right
        if new_node.right is not None:
            new_node.right.parent = node
        new_node.parent = node.parent
        if node.parent is None:
            self.root = new_node
        elif node.parent.left == node:
            node.parent.left = new_node
        else:
            node.parent.right = new_node
        new_node.right = node
        node.parent = new_node
        node.height = self.update_height(node)
        new_node.height = self.update_height(new_node)
        return new_node
    def _remove_bst(self, old_sub_root):
        new_sub_root = None
        if old_sub_root.left is None and old_sub_root.right is None:
            new_sub_root = None
            self.to_restruct = old_sub_root.parent
        elif old_sub_root.left is None:
            new_sub_root = old_sub_root.right
            self.to_restruct = new_sub_root
        elif old_sub_root.right is None:
            new_sub_root = old_sub_root.left
            self.to_restruct = new_sub_root
        elif old_sub_root.left.right is None:
            new_sub_root = old_sub_root.left
            self.set_right(new_sub_root, old_sub_root.right)
            self.to_restruct = new_sub_root
        elif old_sub_root.right.left is None:
            new_sub_root = old_sub_root.right
            self.set_left(new_sub_root, old_sub_root.left)
            self.to_restruct = new_sub_root
        else:
            new_sub_root = old_sub_root.left
            while new_sub_root.right is not None:
                new_sub_root = new_sub_root.right
            predecessor_p = new_sub_root.parent
            self.set_right(predecessor_p, new_sub_root.left)
            self.set_right(new_sub_root, old_sub_root.right)
            self.set_left(new_sub_root, old_sub_root.left)
            self.to_restruct = predecessor_p

        return new_sub_root

    def set_left(self, parent, child):
        parent.left = child
        if child is not None:
            child.parent = parent

    def set_right(self, parent, child):
        parent.right = child
        if child is not None:
            child.parent = parent

