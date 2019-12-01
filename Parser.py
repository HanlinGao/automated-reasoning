# construct a parser tree for logic proposition sentence with priority: unary operator > binary operator(AND > OR).


class TreeNode:
    # defination of parser tree node
    def __init__(self, label):
        self.label = label
        self.children = []
        self.tf = None     # Store the boolean value

    def add_node(self, new_node):
        self.children.append(new_node)

    def __str__(self, level=0):
        result = '\t' * level + self.label + "\n"
        for child in self.children:
            result += child.__str__(level + 1)
        return result

    # Set value of the node
    def set_value(self, value):
        self.tf = value


def tree_generation(suffix_expr):
    # generate a tree from suffix expression
    stack = []
    for each_char in suffix_expr:
        # if char is a capital character, which means it's a atom proposition. Push it into the stack
        if each_char.isupper():
            stack.append(each_char)
        else:
            # if char is an unary operator, pop one element to generate a sub-tree and push the tree back into the stack
            if each_char == '!':
                root = TreeNode('!')
                child = stack.pop()
                if isinstance(child, str):
                    # if child is an atom proposition, create a node for it
                    child = TreeNode(child)
                root.add_node(child)
                stack.append(root)
            else:
                # char is binary operator, pop two element to generate a sub-tree and push the tree back into the stack
                root = TreeNode(each_char)
                right_child = stack.pop()
                left_child = stack.pop()
                if isinstance(right_child, str):
                    # if child is an atom proposition, create a node for it
                    right_child = TreeNode(right_child)
                if isinstance(left_child, str):
                    left_child = TreeNode(left_child)

                root.add_node(left_child)
                root.add_node(right_child)
                stack.append(root)
    temp = stack.pop()
    if isinstance(temp, str):
        temp = TreeNode(temp)
    return temp


def suffix_transform(character_list):
    '''
    operands: all capital character which represent atom propositions
    operator: [!, ^, v, =>, <=>]
    :param character_list: a list of characters in form of ['(', 'A', 'v', 'B', ')']
    :return: a list of suffix expression of these characters
    '''
    stack = []
    results = []
    for each_char in character_list:
        # if char is an operand, output it directly
        if each_char.isupper():
            results.append(each_char)

        # else: all kinds of operators
        else:
            # if '(', push into the stack
            if each_char == '(':
                stack.append(each_char)
            # if ')', pop from the stack one by one
            elif each_char == ')':
                temp = stack.pop()
                while temp != '(':
                    results.append(temp)
                    temp = stack.pop()

            # not brackets: compare char with top of the stack. if char's priority is higher, push char into the stack;
            # else, pop the top of the stack first and push the char into the stack
            else:
                if len(stack) == 0:
                    stack.append(each_char)
                else:
                    top = stack[-1]
                    if top == '!':
                        results.append(stack.pop())
                        stack.append(each_char)
                    elif top == '^':
                        if each_char == '!':
                            stack.append(each_char)
                        else:
                            results.append(stack.pop())
                            stack.append(each_char)
                    elif top == 'v':
                        if each_char == '!' or each_char == '^':
                            stack.append(each_char)
                        else:
                            results.append(stack.pop())
                            stack.append(each_char)
                    else:
                        stack.append(each_char)

    # when finishing reading characters, pop the elements left in the stack
    length = len(stack)
    while length:
        results.append(stack.pop())
        length -= 1
    return results


def parser(string):
    # transform a sentence into a parser tree by sentence -> suffix expression -> tree
    characters = string.split()
    suffix = suffix_transform(characters)
    root = tree_generation(suffix)

    return root


def biconditional_operation(current_root):
    # change the biconditional operation into two =>
    new_root = TreeNode('^')
    new_root.add_node(TreeNode('=>'))
    new_root.add_node(TreeNode('=>'))
    new_root.children[0].add_node(current_root.children[0])
    new_root.children[0].add_node(current_root.children[1])

    new_root.children[1].add_node(current_root.children[1])
    new_root.children[1].add_node(current_root.children[0])

    return new_root


def implication_operation(current_root):
    # change the => into v
    new_root = TreeNode('v')
    new_root.add_node(TreeNode('!'))
    new_root.children[0].add_node(current_root.children[0])
    new_root.add_node(current_root.children[1])

    new_root.children[0] = negation_operation(new_root.children[0])
    return new_root


def negation_operation(current_root):
    # process negation label, combine it with variables(literals) in the same time
    if current_root.children[0].label == '!':
        return preprocess_CNF(current_root.children[0].children[0])
    elif current_root.children[0].label.isupper():
        if current_root.children[0].label[0] == '!':
            return TreeNode(current_root.children[0].label[1:])
        else:
            return TreeNode('!' + current_root.children[0].label)
    elif current_root.children[0].label == '<=>':
        current_root.children[0] = biconditional_operation(current_root.children[0])
        return current_root
    elif current_root.children[0].label == '=>':
        current_root.children[0] = implication_operation(current_root.children[0])
        return current_root
    elif current_root.children[0].label == 'v':
        new_root = TreeNode('^')
        new_root.add_node(TreeNode('!'))
        new_root.add_node(TreeNode('!'))
        new_root.children[0].add_node(current_root.children[0].children[0])
        new_root.children[1].add_node(current_root.children[0].children[1])

        new_root.children[0] = negation_operation(new_root.children[0])
        new_root.children[1] = negation_operation(new_root.children[1])
        return new_root
    else:   # !-^
        new_root = TreeNode('v')
        new_root.add_node(TreeNode('!'))
        new_root.add_node(TreeNode('!'))
        new_root.children[0].add_node(current_root.children[0].children[0])
        new_root.children[1].add_node(current_root.children[0].children[1])

        new_root.children[0] = negation_operation(new_root.children[0])
        new_root.children[1] = negation_operation(new_root.children[1])
        return new_root


def preprocess_CNF(root=TreeNode(None)):
    '''
    transform a parser tree into a CNF parser tree, return result without distribution operation
    '''
    if root.label == '!':
        root = negation_operation(root)
    elif root.label == 'v' or root.label == '^':
        pass
    elif root.label == '=>':
        root = implication_operation(root)
    elif root.label == '<=>':
        root = biconditional_operation(root)
    else:   # root.label is an atom proposition
        pass

    # print(root)
    length = len(root.children)
    for i in range(length):
        root.children[i] = preprocess_CNF(root.children[i])

    return root


def check_node(current_root):
    # traverse the whole tree, check every node and process according to the label, return the tree after process
    if current_root.label == 'v':
        current_root = distribution_law(current_root)
    else:
        length = len(current_root.children)
        for i in range(length):
            current_root.children[i] = check_node(current_root.children[i])
    return current_root


def distribution_law(current_root):
    # deal with all situations where v-^ (distribution law), return the root after process

    # if v-!A , v-A links, and current_root = A
    if current_root.label.isupper():
        return current_root

    # if children are 'v' ---> v-(v-v)
    left = current_root.children[0]
    right = current_root.children[1]
    if (left.label == 'v' or left.label.isupper()) and (right.label == 'v' or right.label.isupper()):
        current_root.children[0] = distribution_law(current_root.children[0])
        current_root.children[1] = distribution_law(current_root.children[1])

    # after the processing above, if v-^ link exists
    if current_root.children[0].label == '^' or current_root.children[1].label == '^':
        new_root = TreeNode('^')
        new_root.add_node(TreeNode('v'))
        new_root.add_node(TreeNode('v'))

        # if left child is ^ node, combine each child of '^' with the right child
        if current_root.children[0].label == '^':
            new_root.children[0].add_node(current_root.children[0].children[0])
            new_root.children[0].add_node(current_root.children[1])

            new_root.children[1].add_node(current_root.children[0].children[1])
            new_root.children[1].add_node(current_root.children[1])

        else:
            new_root.children[0].add_node(current_root.children[0])
            new_root.children[0].add_node(current_root.children[1].children[0])

            new_root.children[1].add_node(current_root.children[0])
            new_root.children[1].add_node(current_root.children[1].children[1])

        new_root.children[0] = distribution_law(new_root.children[0])
        new_root.children[1] = distribution_law(new_root.children[1])

        return new_root
    return current_root


def to_CNF(root=TreeNode(None)):
    # transform a parser tree into a CNF tree
    pre_cnf = preprocess_CNF(root)
    cnf = check_node(pre_cnf)

    return cnf


# Get a list of propositional symbols in KB and alpha
def get_symbol(node, symbol):
    # Get the symbols from the leaf nodes
    if not node.children:
        if node.label not in symbol:   # Make sure not to add redundant symbol
            symbol.append(node.label)

    # If only has one child(negation case)
    elif len(node.children) == 1:
        get_symbol(node.children[0], symbol)

    # The normal case that has children
    else:
        # Deep first search to run over the tree
        left = node.children[0]
        right = node.children[1]
        get_symbol(left, symbol)
        get_symbol(right, symbol)


def remove_dups(clause):
    # remove all the duplicate clauses
    new_clause = []
    for each in clause:
        if isinstance(each, list):
            each.sort()
        if each not in new_clause:
            new_clause.append(each)
    return new_clause


def get_atom(node):
    # deal with the situation when have a *-v link
    atom_list = []
    for each in node.children:
        if each.label != 'v':
            atom_list.append(each.label)
        else:
            atom_list = atom_list + get_atom(each)
    atom_list = remove_dups(atom_list)                      # remove duplicate clauses
    return atom_list


def get_each_clause(TreeNode):
    # search tree and get clauses
    result_list = []
    for each in TreeNode.children:
        if each.label == 'v':
            result_list.append(get_atom(each))
        elif each.label != '^':
            result = []
            result.append(each.label)
            result_list.append(result)
        else:
            result_list = result_list + get_each_clause(each)
    return result_list


def merge_tree(node1, node2):
    # merge KB and query
    root = TreeNode('^')
    root.add_node(node1)
    root.add_node(node2)
    return root


def to_negation(root):
    node = TreeNode('!')
    node.add_node(root)
    return node
