class BasicInterpreter:

    def __init__(self, tree, env):
        self.env = env
        result = self.walk_tree(tree)
        if result is not None and isinstance(result, int):
            print(result)
        if isinstance(result, str) and result[0] == '"':
            print(result)

    def walk_tree(self, node):

        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node
        
        if node is None:
            return None

        if node[0] == 'program':
            if node[1] == None:
                self.walk_tree(node[2])
            else:
                self.walk_tree(node[1])
                self.walk_tree(node[2])
        
        if node[0] == 'num':
            return node[1]
        
        if node[0] == 'str':
            return node[1]
        
        if node[0] == 'add':
            return self.walk_tree(node[1]) + self.walk_tree(node[2])
        elif node[0] == 'sub':
            return self.walk_tree(node[1]) - self.walk_tree(node[2])
        elif node[0] == 'mul':
            return self.walk_tree(node[1]) * self.walk_tree(node[2])
        elif node[0] == 'div':
            return self.walk_tree(node[1]) / self.walk_tree(node[2])

        if node[0] == 'var_assign':
            self.env[node[1]] = self.walk_tree(node[2])
            return node[1]
        
        if node[0] == 'var':
            try:
                return self.env[node[1]]
            except LookupError:
                print("Undefined variable '"+node[1]+"' found!")
                return 0
