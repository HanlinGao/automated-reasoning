import copy
import Parser


# check if two clauses are soluble to each other
def check_soluble(clause1, clause2):
    for atom1 in clause1:
        for atom2 in clause2:
            if atom1 == '!' + atom2 or '!' + atom1 == atom2:
                return True
    return False


# check is the list1 included in list2, return a boolean
def list_comparison(list1, list2):
    flag = True
    for each in list1:
        flag = flag and (each in list2)
    return flag


# resolve two clauses. Take in two clauses and output a list of resolved clauses, excluding useless clauses
def resolve(clause1, clause2):
    result_list = []  # a list will contain resolved clauses
    if not check_soluble(clause1, clause2):  # if two not soluble clauses, return themselves without any change
        result_list.append(clause1)
        result_list.append(clause2)
        return result_list
    else:  # if soluble，take all possible solved clauses into the list
        useless_flag = True  # a boolean variable shows if the solved clauses is useful
        for atom1 in clause1:
            for atom2 in clause2:
                result = []
                atom_new1 = copy.deepcopy(clause1)
                atom_new2 = copy.deepcopy(clause2)

                # resolution process
                if atom1 == '!' + atom2 or '!' + atom1 == atom2:
                    atom_new1.remove(atom1)
                    atom_new2.remove(atom2)
                    result = result + atom_new1 + atom_new2

                    # if the length is too long to be useful, discard
                    if len(result) > len(clause1) and len(result) > len(clause2):
                        continue

                    useless_flag = False
                    result = Parser.remove_dups(result)  # remove the duplicate within a clause

                    result_list.append(result)
        if useless_flag:
            result_list.append(clause1)
            result_list.append(clause2)

        return result_list


# resolution
def resolution(KB, alpha):
    # merge the tree
    clauses = Parser.merge_tree(Parser.to_CNF(KB), Parser.to_CNF(Parser.to_negation(alpha)))
    each_clause_list = Parser.get_each_clause(clauses)  # each_clasuse_list is used for record all the clauses of the merged
                                                 # tree of kb and alpha, later used as updated list for next resolution
    new = []  # used for storing solved clause
    counter = 0
    while True:
        each_clause_list = sorted(each_clause_list, key=lambda i: len(i))
        # every pair to do the resolution
        for i in range(len(each_clause_list) - 1):
            for j in range(i + 1, len(each_clause_list)):
                resolvent = resolve(each_clause_list[i], each_clause_list[j])
                for each in resolvent:
                    # if an empty clause is created, return true
                    if each == []:
                        return True
                    # add the resolvent to new
                    new.append(each)
                    new = Parser.remove_dups(new)
        # check if new is included by each_clause_list, if true, return false
        if list_comparison(new, each_clause_list):
            return False
        each_clause_list = Parser.remove_dups(each_clause_list + new)  # update and add new to each_clause_list for next iteration


# return final result
def result(KB, alpha):
    # if resolution(kb, alpha) returns true, then KB entails alpha
    if resolution(KB, alpha):
        return True
    # if kb does not entails alpha, check weather kb can entails the negation of alpha, if so, return false, otherwise, maybe
    else:
        if resolution(KB, Parser.to_negation(alpha)):
            return False
        else:
            return 'Maybe'


# to see if there is a tautology in a clause, take in a clause, output a boolean
def check_tautology(clause):
    flag = False
    for i in range(len(clause) - 1):
        for j in range(i + 1, len(clause)):
            if clause[i] == '!' + clause[j] or clause[j] == '!' + clause[i]:
                flag = True
                break
    return flag


# take out all the clause that includes a pure literal or has a tautology within a clause
def elimination(clauses):
    pure_list = find_pure_literal(clauses)
    new_clause = []
    for each in clauses:
        if (not check_purity(each, pure_list)) and (not check_tautology(each)):
            new_clause.append(each)
    return new_clause


# output a list that contains all distinct pure symble
def find_pure_literal(clauses):
    symbol = [] #get all symbols into a list
    for each_clause in clauses:
        for index in range(len(each_clause)):
            if each_clause[index] not in symbol:
                symbol.append(each_clause[index])
    pure_literal = copy.deepcopy(symbol)
    # remove every symbol that has a complimentary symbol by pair
    for i in range(len(symbol)-1):
        for j in range(i+1,len(symbol)):
            if symbol[i] == '!' + symbol[j] or symbol[j] == '!' + symbol[i]:
                pure_literal.remove(symbol[i])
                pure_literal.remove(symbol[j])
    return pure_literal


# by using a list of pure symbol, mark false to a clause if it contains a pure symbol
def check_purity(clause, pure_list):
    flag = False
    for each in clause:
        if each in pure_list:
            flag = True
            break
    return flag