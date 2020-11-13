from chomsky_nf import CFG, Product, Var

testcase = [
    {
        # testcase 1 from example 2.10 of textbook
        'nonterm': ['A', 'B'],
        'term': ['a', 'b'],
        'products': [
            'S → ASA|aB',
            'A → B|S',
            'B → b|ε'
        ]
    },
    {
        # testcase 2 from Internet
        'nonterm': ['A', 'B'],
        'term': ['a', 'b'],
        'products': [
            'S → ASB',
            'A → aAS|a|ε',
            'B → SbS|A|bb'
        ]
    }
]

if __name__ == '__main__':
    for i in range(0, len(testcase)):
        print('\n\nTestCase ' + str(i + 1) + ':')
        cfg = CFG(nonterm=testcase[i]['nonterm'], term=testcase[i]['term'])
        for string in testcase[i]['products']:
            cfg.str2product(string)
        cfg.cfg2cnf()
        print(str(cfg))
