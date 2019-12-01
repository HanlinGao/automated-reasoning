import Parser
import copy


# Do the calculation for the current knowledge base
def kb_calculate(opr):
    # If it is leaf, return the boolean value
    if not opr.children:
        return opr.tf

    # If the opr is negation(only has one child)
    if len(opr.children) == 1:
        child = opr.children[0]
        kb_calculate(child)
        # Negation
        if child.tf is False:
            opr.set_value(True)
        else:
            opr.set_value(False)
        return opr.tf

    # if the opr is another operation
    else:
        # Two children of the current node
        left = opr.children[0]
        right = opr.children[1]
        # Find the bool value(leaf) in the tree
        # It means you find the minimal propositional logic formula
        if right.children:
            kb_calculate(right)
        if left.children:
            kb_calculate(left)

        # True table of each operation(except negation) in the KB tree
        if opr.label == 'v':
            if left.tf is False and right.tf is False:
                opr.set_value(False)
            else:
                opr.set_value(True)
        elif opr.label == '^':
            if left.tf is True and right.tf is True:
                opr.set_value(True)
            else:
                opr.set_value(False)
        elif opr.label == '=>':
            if left.tf is True and right.tf is False:
                opr.set_value(False)
            else:
                opr.set_value(True)
        elif opr.label == '<=':
            if left.tf is False and right.tf is True:
                opr.set_value(False)
            else:
                opr.set_value(True)
        elif opr.label == '<=>':
            if left.tf is False and right.tf is False:
                opr.set_value(True)
            elif left.tf is True and right.tf is True:
                opr.set_value(True)
            else:
                opr.set_value(False)
        return opr.tf


# Change the symbols(leaves) in the tree into bool value based on the current model
def kb_leaf_bool(node, model):
    # Set up the bool value of the leaf node
    if not node.children:
        node.set_value(model[node.label])

    # If the node is negation (only has one child)
    elif len(node.children) == 1:
        child = node.children[0]
        kb_leaf_bool(child, model)

    # Normal case: do the deep first search
    else:
        # DFS, Left subtree first,then right subtree
        left = node.children[0]
        right = node.children[1]
        kb_leaf_bool(left, model)
        kb_leaf_bool(right, model)


# Return true is a sentence holds within a model
def pl_true(node, model):
    kb_leaf_bool(node, model)
    return kb_calculate(node)


# Return true if KB entails alpha
def tt_entails(kb, alpha):
    # Get the symbols from KB and alpha and add to the symbol list
    symbol = []
    Parser.get_symbol(kb, symbol)
    Parser.get_symbol(alpha, symbol)
    # Initial the model(partial model as an assignment to some of the symbols)
    model = {}
    check_all = tt_check_all(kb, alpha, symbol, model)
    check_one = tt_check_one(kb, alpha, symbol, model)
    if check_all and check_one:
        return True
    elif not check_all and not check_one:
        return False
    else:
        return "Maybe"


# Check all the possible truth table model
# and return true if every model of KB is also a model of alpha
def tt_check_all(kb, alpha, symbol, model):
    # If all the symbol has added to the model
    if not symbol:
        if pl_true(kb, model):  # Check if sentence holds within a model
            return pl_true(alpha, model)
        else:
            return True  # When KB is false, always return true to neglect the current model

    else:
        # Create two models based on the current symbol (False & True)
        symbol0 = copy.deepcopy(symbol)
        p = symbol0[0]
        del symbol0[0]
        rest = symbol0
        model1 = copy.deepcopy(model)
        model2 = copy.deepcopy(model)
        model1[p] = True
        model2[p] = False
        return tt_check_all(kb, alpha, rest, model1) and tt_check_all(kb, alpha, rest, model2)


# Check all the possible truth table model
# and return true if one model of KB is also a model of alpha
def tt_check_one(kb, alpha, symbol, model):
    # If all the symbol has added to the model
    if not symbol:
        if pl_true(kb, model):  # Check if sentence holds within a model
            return pl_true(alpha, model)
        else:
            return False  # When KB is false, always return False to neglect the current model

    else:
        # Create two models based on the current symbol (False & True)
        symbol0 = copy.deepcopy(symbol)
        p = symbol0[0]
        del symbol0[0]
        rest = symbol0
        model1 = copy.deepcopy(model)
        model2 = copy.deepcopy(model)
        model1[p] = True
        model2[p] = False
        return tt_check_one(kb, alpha, rest, model1) or tt_check_one(kb, alpha, rest, model2)