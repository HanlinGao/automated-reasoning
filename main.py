import Parser
import Model_checking
import DPLL
import Resolution

def print_test():
    print('1.-----------------------------------------------------')
    print("Modus Ponens test")
    print("Knowledge base:")
    print("P => Q")
    print("P")
    print("Query: Q")
    sentence = "P ^ ( P => Q )"
    query = "Q"
    kb1 = Parser.parser("P ^ ( P => Q )")
    alpha1 = Parser.parser("Q")
    print("Ans with model checking:", Model_checking.tt_entails(kb1, alpha1))
    print("Ans with resolution:", Resolution.result(kb1, alpha1))
    print("Ans with DPLL:", DPLL.DPLL_satisfiable(sentence, query), "\n")
    print('2.-------------------------------------------------------')
    print("Wumpus World test")
    print("Knowledge base:")
    print("!P11")
    print("B11 <=> (P12 v P21)")
    print("B21 <=> (P11 v P22 v P31)")
    print("!B11")
    print("B21")
    print("Query: P12")
    kb2 = Parser.parser("! P11 ^ ( B11 <=> ( P12 v P21 ) ) ^ ( B21 <=> ( P11 v P22 v P31 ) ) ^ ! B11 ^ B21")
    alpha2 = Parser.parser("P12")
    sentence = "! P11 ^ ( B11 <=> ( P12 v P21 ) ) ^ ( B21 <=> ( P11 v P22 v P31 ) ) ^ ! B11 ^ B21"
    query = "P12"
    print("Ans with model checking:", Model_checking.tt_entails(kb2, alpha2))
    print("Ans with resolution:", Resolution.result(kb2, alpha2))
    print("Ans with DPLL:", DPLL.DPLL_satisfiable(sentence, query), "\n")
    print('3.------------------------------------------------------')
    print("Horn Clauses test")
    print("Knowledge base:")
    print("Mythical => Immortal")
    print("!Mythical => (!Immortal ^ Mammal)")
    print("(Immortal v Mammal) => Horned")
    print("Horned => Magical")
    print("Query1: Mythical")
    print("Query2: Magical")
    print("Query3: Horned")
    kb3 = Parser.parser(" ( MY => IM ) ^ ( ! MY => ( ! IM ^ MA ) ) ^ ( ( IM v MA ) => HO ) ^ ( HO => MG ) ")
    alpha30 = Parser.parser("MY")
    alpha31 = Parser.parser("MG")
    alpha32 = Parser.parser("HO")

    sentence = " ( MY => IM ) ^ ( ! MY => ( ! IM ^ MA ) ) ^ ( ( IM v MA ) => HO ) ^ ( HO => MG ) "
    query1 = "MY"
    query2 = "MG"
    query3 = "HO"
    print("Ans with model checking:", Model_checking.tt_entails(kb3, alpha30), Model_checking.tt_entails(kb3, alpha31),
          Model_checking.tt_entails(kb3, alpha32))
    print("Ans with resolution:", Resolution.result(kb3, alpha30), Resolution.result(kb3, alpha31),
          Resolution.result(kb3, alpha32))
    print("Ans with DPLL:", DPLL.DPLL_satisfiable(sentence, query1), DPLL.DPLL_satisfiable(sentence, query2),
          DPLL.DPLL_satisfiable(sentence, query3), "\n")
    print('4.1------------------------------------------------------')

    print("The Door of Enlightenment")
    print("Smullyan's Problem")
    print("Knowledge base:")
    print("A <=> X")
    print("B <=> (Y v Z)")
    print("C <=> (A ^ B)")
    print("D <=> (X ^ Y)")
    print("E <=> (X ^ Z)")
    print("F <=> (D v E)")
    print("G <=> (C => F)")
    print("H <=> (G ^ H) => A")
    print("Query1: X")
    print("Query2: Y")
    print("Query3: Z")
    print("Query4: W")
    kb4 = Parser.parser("( A <=> X ) ^ ( B <=> ( Y v Z ) ) ^ ( C <=> ( A ^ B ) ) ^ ( D <=> ( X ^ Y ) ) ^"
                        " ( E <=> ( X ^ Z ) ) ^ ( F <=> ( D v E ) ) ^ ( G <=> ( C => F ) ) ^ ( H <=> ( ( G ^ H ) => A )"
                        " ) ^ ( X v Y v Z v W )")
    alpha40 = Parser.parser("X")
    alpha41 = Parser.parser("Y")
    alpha42 = Parser.parser("Z")
    alpha43 = Parser.parser("W")
    sentence = "( A <=> X ) ^ ( B <=> ( Y v Z ) ) ^ ( C <=> ( A ^ B ) ) ^ ( D <=> ( X ^ Y ) ) ^ ( E <=> ( X ^ Z ) ) " \
               "^ ( F <=> ( D v E ) ) ^ ( G <=> ( C => F ) ) ^ ( H <=> ( ( G ^ H ) => A ) ) " \
               "^ ( X v Y v Z v W )"
    query1 = "X"
    query2 = "Y"
    query3 = "Z"
    query4 = "W"

    print("Ans with model checking:", Model_checking.tt_entails(kb4, alpha40), Model_checking.tt_entails(kb4, alpha41),
          Model_checking.tt_entails(kb4, alpha42), Model_checking.tt_entails(kb4, alpha43))
    # in case of taking too long to check the answer from resolution rule, we print the result directly.
    # since we check the
    print("Ans with resolution:", Resolution.result(kb4, alpha40), Resolution.result(kb4, alpha41),
          Resolution.result(kb4, alpha42), Resolution.result(kb4, alpha43))
    print("Ans with DPLL:", DPLL.DPLL_satisfiable(sentence, query1), DPLL.DPLL_satisfiable(sentence, query2),
          DPLL.DPLL_satisfiable(sentence, query3), DPLL.DPLL_satisfiable(sentence, query4), "\n")
    print('4.2-----------------------------------------------------')

    print("Liu's Problem")
    print("Knowledge base:")
    print("A <=> X")
    print("C <=> (A ^ S)" 'S stands for missing information')
    print("G <=> ( C => T ) ‘T stands for missing information")
    print("H <=> ( ( G ^ H ) => A )")
    print("Query: X")
    kb5 = Parser.parser("( A <=> X ) ^ ( C <=> ( A ^ S ) ) ^ ( G <=> ( C => T ) ) ^ ( H <=> ( ( G ^ H ) => A ) ) "
                 "^ ( X v Y v Z v W )")
    alpha50 = Parser.parser("X")

    sentence = "( A <=> X ) ^ ( C <=> ( A ^ S ) ) ^ ( G <=> ( C => T ) ) ^ ( H <=> ( ( G ^ H ) => A ) ) " \
               "^ ( X v Y v Z v W )"
    query = "X"
    print("Ans with model checking:", Model_checking.tt_entails(kb5, alpha50))
    print("Ans with resolution:", Resolution.result(kb5, alpha50))
    print("Ans with DPLL:", DPLL.DPLL_satisfiable(sentence, query))


print_test()