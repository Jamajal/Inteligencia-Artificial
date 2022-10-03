# Task: Implement an abduction method

def abduction(kb, obs):
    explanation = []
    logical_consequence = bottom_up(kb)
    rules = []

    for obs in obs:
        rules += kb["rules"][obs]

    for rule in rules:
        is_explanation = True
        rule_atoms = []
        for atom in rule:
            rule_atoms.append(atom)

            if not (atom in logical_consequence or atom in kb["assumables"]):
                is_explanation = False
                rule_atoms = []
                break

        if is_explanation and not (rule in explanation):
            explanation += [rule]

    return explanation

def bottom_up(kb):
    C = []

    if 'askables' in kb:
        for a in kb['askables']:
            if a in kb["assumables"] or ask(a):
                C.append(a)

    if 'assumables' in kb:
        for a in kb['assumables']:
            if not a in C:
                C.append(a)

    new_consequence = True

    while new_consequence:
        new_consequence = False

        for head in kb['rules']:
            if head not in C:  # Very innefient
                for body in kb['rules'][head]:
                    if not set(body).difference(set(C)):  # Very innefient
                        C.append(head)
                        new_consequence = True

    return C


def ask(askable):
    ans = input(f'Is {askable} true ? ')
    return True if ans.lower() in ['sim', 's', 'yes', 'y'] else False


if __name__ == "__main__":
    kb = {'rules': {'bronchitis': [['influenza'], ['smokes']],
                    'coughing': [['bronchitis']],
                    'wheezing': [['bronchitis']],
                    'fever': [['influenza', 'infection']],
                    'sore_throat': [['influenza']],
                    'false': [['smokes', 'nonsmokers']]},
          'askables': [],
          'assumables': ['smokes', 'nonsmokers', 'influenza', 'infection']}

    observation = ['wheezing', 'fever', 'sore_throat']
    print(f"Explanation to {observation}: {abduction(kb, observation)}")
