import Parser
import copy


def find_pure_symbols(symbols, clauses, model):
    # symbols(no negation), clauses(with negation), model(incomplete, some symbols haven't been assigned yet)

    # assign truth value in model to symbols, if any true, eliminate this clause
    new_clauses = []
    for each_clause in clauses:
        eliminate_flag = False  # if this clause should be eliminate, set the flag to be True
        for each_element in each_clause:
            if '!' in each_element:
                key = each_element[1:]
                if key in model:
                    # if model[key] == False, then !key will be True, eliminate this clause
                    if not model[key]:
                        eliminate_flag = True
                        break

                    # if model[key] == True, truth depends on other elements in this clause
            else:
                if each_element in model:
                    # if model[key] == False, truth depends on other elements in this clause
                    if not model[each_element]:
                        continue
                    # if model[key] == True, eliminate this clause
                    else:
                        eliminate_flag = True
                        break
        # check the flag
        if not eliminate_flag:
            new_clauses.append(each_clause)

    # traverse the clauses, check whether there are any pure symbols
    flag_dict = dict()
    for each_clause in new_clauses:
        for each_element in each_clause:
            if each_element in flag_dict:
                pass
            else:
                # check whether the negation of the element have not occurred
                if '!' in each_element:
                    key = each_element[1:]
                    if key in flag_dict:
                        flag_dict[key] = 'impure'
                    else:
                        flag_dict[each_element] = 'pure'
                else:
                    key = '!' + each_element
                    if key in flag_dict:
                        flag_dict[key] = 'impure'
                    else:
                        flag_dict[each_element] = 'pure'

    # get a pure symbol
    for each in flag_dict:
        if flag_dict[each] == 'pure':
            if '!' in each:
                if each[1:] in symbols:
                    return each[1:], False
            else:
                if each in symbols:
                    return each, True

    return 'null', None


def find_unit_clause(symbols, clauses, model):
    # eliminate the clauses according to model
    truth_symbol = 'null'
    # assign truth value in model to symbols, if only one true in one clause, make it an unit clause
    for each_clause in clauses:
        true_unknown = 0
        for each_element in each_clause:
            if '!' in each_element:
                key = each_element[1:]
                if key in model:
                    # if model[key] == False, then !key will be True
                    if not model[key]:
                        truth_symbol = each_element
                        true_unknown += 1
                    # if model[key] == True, truth depends on other elements in this clause
                else:
                    truth_symbol = each_element
                    true_unknown += 1

            else:
                if each_element in model:
                    # if model[key] == False, truth depends on other elements in this clause
                    if not model[each_element]:
                        continue
                    # if model[key] == True
                    else:
                        truth_symbol = each_element
                        true_unknown += 1
                else:
                    truth_symbol = each_element
                    true_unknown += 1

        # check the true or unknown numbers in one clause
        if true_unknown == 1:
            if '!' in truth_symbol:
                if truth_symbol[1:] in symbols:
                    return truth_symbol[1:], False
            else:
                if truth_symbol in symbols:
                    return truth_symbol, True
    return 'null', None


def DPLL(clauses, symbols, model):
    # check truth situations of all clauses in the model
    all_true_flag = True
    some_false = False

    for each_clause in clauses:
        clause_false = True
        clause_true = False
        for each_ele in each_clause:
            if '!' in each_ele:
                key = each_ele[1:]
                if key in model:
                    # if !P is False, the truth of the clause depends on other elements
                    if model[key]:
                        continue
                    # if !P is True, check next clause
                    else:
                        clause_true = True
                        clause_false = False
                        break
                else:
                    # one element is unknown, but it is not enough to conclude the clause it's unknown, only not false
                    clause_false = False

            else:
                if each_ele in model:
                    # if P is True, check next clause
                    if model[each_ele]:
                        clause_true = True
                        clause_false = False
                        break

                    # if P is False, the truth of the clause depends on other elements
                else:
                    clause_false = False

        # if clause is false
        if clause_false:
            some_false = True
            all_true_flag = False
            break
        # if clause is not true(meaning unknown)
        else:
            if not clause_true:
                all_true_flag = False
                break

    # if all clauses are true, return true
    if all_true_flag:
        return True

    else:
        # if some clauses is false, return false
        if some_false:
            return False

        else:
            symbol, value = find_pure_symbols(symbols, clauses, model)
            if symbol != 'null':
                symbols.remove(symbol)
                model[symbol] = value
                return DPLL(clauses, symbols, model)

            symbol, value = find_unit_clause(symbols, clauses, model)
            if symbol != 'null':
                symbols.remove(symbol)
                model[symbol] = value
                return DPLL(clauses, symbols, model)

            symbol = symbols.pop()

            rest1 = copy.deepcopy(symbols)
            rest2 = copy.deepcopy(symbols)

            model1 = copy.deepcopy(model)
            model2 = copy.deepcopy(model)

            model1[symbol] = True
            model2[symbol] = False
            return DPLL(clauses, rest1, model1) or DPLL(clauses, rest2, model2)


def DPLL_satisfiable(sentence, query):
    kb = Parser.parser(sentence)
    query = Parser.parser(query)

    # check kb |= query, that is, check whether kb ^ !(query) is unsatisfiable
    ori_tree = Parser.merge_tree(kb, Parser.to_negation(query))

    symbols = []
    Parser.get_symbol(ori_tree, symbols)   # a list of the proposition symbols in s

    cnf_tree = Parser.to_CNF(ori_tree)
    # the set of clauses in the CNF representation of s
    clauses = Parser.remove_dups(Parser.get_each_clause(cnf_tree))
    model = dict()

    final_result = DPLL(clauses, symbols, model)
    # if kb ^ !(query) is unsatisfiable, kb entails query
    if not final_result:
        return True

    # kb cannot entail query
    else:
        # check kb |= !(query), that is, check whether kb ^ query is unsatisfiable
        ori_tree = Parser.merge_tree(kb, query)

        symbols = []
        Parser.get_symbol(ori_tree, symbols)  # a list of the proposition symbols in s

        cnf_tree = Parser.to_CNF(ori_tree)
        # the set of clauses in the CNF representation of s
        clauses = Parser.remove_dups(Parser.get_each_clause(cnf_tree))
        model = dict()

        final_result = DPLL(clauses, symbols, model)

        # if kb ^ query is unsatisfiable, kb entails !query
        if not final_result:
            return False
        else:
            return 'Maybe'