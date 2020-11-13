class Var:
    """符号对象"""

    def __init__(self, symbol, is_nonterm: bool):
        self.symbol = symbol
        self.is_nonterm = is_nonterm

    def __str__(self):
        return self.symbol

    def __hash__(self):
        return hash(self.symbol)

    def __eq__(self, other):
        return self.symbol == other.symbol


# 产生式中必会出现的常量
EPSILON = Var('ε', is_nonterm=False)
START = Var('S', is_nonterm=True)
EXT_START = Var('S0', is_nonterm=True)


class Product:
    """产生式对象"""

    def __init__(self, left_symbol: Var, right_symbol: list):
        self.left = left_symbol
        self.right = right_symbol

    def __str__(self):
        s = str(self.left) + '→'
        parts = []
        for part in self.right:
            p = ''
            for var in part:
                p = p + str(var)
            parts.append(p)
        s = s + '|'.join(parts)
        return s


class CFG:
    """上下文无关文法对象"""

    def __init__(self, nonterm: list, term: list):
        self.start = START
        self.nonterm = {START}.union(set([Var(nt, is_nonterm=True) for nt in nonterm]))
        self.term = set([Var(t, is_nonterm=False) for t in term])
        self.products = []
        """需要将语法中已经用到的非终结符和终结符从可分配表中去掉，防止后面分配新符号时发生冲突"""
        """这里初始值均是一开始已经给出的部分，后面扩展的时候再对两个集合进行改动"""
        """非终结符的可分配符号，注意：不含固定用作起始符号的S"""
        self.nonterminal_cand = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
                                 'R', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.nonterminal_cand.reverse()  # 进行反转，方便后续取用符号
        for var in nonterm:
            self.nonterminal_cand.remove(var)

    def __str__(self):
        return 'Non-Terminals:' + ','.join([str(var) for var in self.nonterm]) + '\nTerminals:' + ','.join(
            [str(var) for var in self.term]) + '\nStart:' + str(self.start) + '\nProducts:\n\t' + '\n\t'.join(
            [str(product) for product in self.products])

    def str2product(self, deriv: str):
        """给定输入的产生式字符串表示，转换并生成产生式对象"""

        def exists(var_set: set, var: str):
            for v in var_set:
                if v.symbol == var:
                    return True
            return False

        comp = deriv.strip().split('→')
        derived = comp[1].split('|')
        left_part = Var(comp[0].strip(), is_nonterm=True)
        right_part = []
        for part in derived:
            d = []
            part = part.strip()
            for i in range(0, len(part)):
                var = part[i]
                if var == 'ε':
                    d.append(EPSILON)
                elif var == 'S':
                    d.append(START)
                else:
                    d.append(Var(var, is_nonterm=exists(self.nonterm, var)))
            right_part.append(d)
        self.products.append(Product(left_symbol=left_part, right_symbol=right_part))

    def cfg2cnf(self):
        """将上下文无关文法的产生式全部转换为乔姆斯基范式"""

        """step1:添加扩展的起始符号S0作为新的起始符号"""
        self.products.append(Product(left_symbol=EXT_START, right_symbol=[[START]]))

        """step2:循环去掉生成epsilon产生式，直至不存在epsilon产生式"""

        def find_epsilon() -> Var:
            """查找右部存在epsilon的生成式，找到则删除epsilon并返回左端符号"""
            for product in self.products:
                for rpart in product.right:
                    if EPSILON in rpart:
                        rpart.remove(EPSILON)
                        return product.left
            return None

        while True:
            nullable = find_epsilon()
            if nullable is None:
                break
            for product in self.products:
                # 遍历全部的产生式
                new_right_parts = []
                for rpart in product.right:
                    # 对每个产生式的右部进行检查
                    if nullable in rpart:
                        """
                        如果右部的候选式中含有当前指定的左部，则复制这个候选式并把指定左部用epsilon替换，并加入到候选式列表中
                        可能指定的左部（单一非终结符）在右部出现多次，这时候每个位置都有可能取空值或不取空值，但不能都不取空值
                        此操作会增加(2^n)-1个候选式，其中n为非终结符的出现次数
                        """
                        candidates_of_right_part = []
                        stack_of_var = []

                        def recur_null(indices, limit):
                            """递归产生新的候选式，每个可取空的非终结符都会分别赋值为空或非空，以组合成不同情况"""
                            while indices < limit and rpart[indices] != nullable:
                                # 如果当前符号不是要找的可取空的符号，就直接入栈并且继续向后
                                # 这一步放在递归终止条件的前面，是为了防止最后一个符号不是指定符号的情况
                                stack_of_var.append(rpart[indices])
                                indices += 1
                            if indices >= limit:
                                # 到达结尾，将已赋值完成的各个符号拼成候选式并记录下来
                                candidates_of_right_part.append(list(stack_of_var))
                                return
                            # 以下两次递归操作，一次赋值一次为空值
                            stack_of_var.append(nullable)
                            recur_null(indices + 1, limit)
                            while len(stack_of_var) > 0 and stack_of_var[-1] != nullable:
                                # 所有非指定符号出栈
                                stack_of_var.pop()
                            if stack_of_var[-1]:
                                # 指定符号出栈
                                stack_of_var.pop()
                            recur_null(indices + 1, limit)

                        recur_null(0, len(rpart))
                        # 注意，需要去掉各种组合中和原来一样的那种，这个情况会重复
                        if len(candidates_of_right_part) == 0:
                            new_right_parts.append(EPSILON)
                        else:
                            candidates_of_right_part.remove(rpart)
                            for cand in candidates_of_right_part:
                                new_right_parts.append(cand if cand != [] else [EPSILON])
                for part in new_right_parts:
                    if part not in product.right:
                        product.right.append(part)

        """step3:循环去掉左部生成左部的产生式（即单一规则）"""

        def find_left(var: Var) -> Product:
            for product in self.products:
                if product.left == var:
                    return product
            return None

        def find_single_nonterm() -> (Var, Product):
            for product in self.products:
                for rpart in product.right:
                    if len(rpart) == 1 and rpart[0].is_nonterm:
                        nt = rpart[0]
                        product.right.remove(rpart)
                        if nt == product.left:
                            # 如果和左部一样，直接删除
                            continue
                        return nt, product
            return None, None

        # 先处理左部为扩展初始符号S0的产生式，右部在此步骤执行时必定只有S，直接用S的右部替换S0的右部中的S即可，在此步的后续操作中不再改变
        s0 = find_left(EXT_START)
        s0.right = list(find_left(START).right)

        # 再对剩下的进行循环处理，如果右部有单一非终结符，则用相应的非终结符做左部的产生式替换这个非终结符，如果和左部一样就直接删除
        while True:
            single_var, target_prod = find_single_nonterm()
            if single_var is None:
                break
            for cand in find_left(single_var).right:
                if cand not in target_prod.right:
                    target_prod.right.append(cand)

        """step4:将所有右部的非单一终结符用非终结符替换，并添加相应的新产生式"""
        replaced = dict()  # 记录扫描过程中已被替换的终结符，及替换时使用的对应非终结符
        for product in self.products:
            for i in range(0, len(product.right)):
                if len(product.right[i]) == 1:
                    # 这时右部仍为长度是1的情形是仅有一个终结符或者初始符号S，无需处理
                    continue
                for j in range(0, len(product.right[i])):
                    if not product.right[i][j].is_nonterm:
                        # 当右部长度大于1且有终结符时，应该进行替换
                        try:
                            product.right[i][j] = replaced[product.right[i][j]]
                        except KeyError:
                            new_left = Var(self.nonterminal_cand.pop(), is_nonterm=True)
                            new_right = [[product.right[i][j]]]
                            self.products.append(Product(left_symbol=new_left, right_symbol=new_right))
                            replaced[product.right[i][j]] = new_left
                            product.right[i][j] = new_left

        """step5:将所有右部超过两个非终结符的化为两个非终结符，并添加相应产生式"""
        """
        策略为“折叠化简”，例如：
        A→BCDE化为：A→GE, F→BC, G→FD
        """
        simplified = {}
        for product in self.products:
            for i in range(0, len(product.right)):
                if len(product.right[i]) < 3:
                    continue
                while len(product.right[i]) > 2:
                    va = product.right[i][0]
                    vb = product.right[i][1]
                    try:
                        product.right[i][0] = Var(simplified[str(va) + str(vb)], is_nonterm=True)
                    except KeyError:
                        new_left = Var(self.nonterminal_cand.pop(), is_nonterm=True)
                        self.products.append(Product(left_symbol=new_left, right_symbol=[[va, vb]]))
                        product.right[i][0] = new_left
                    product.right[i].remove(vb)

        """step6:清理掉所有的空候选式"""
        for product in self.products:
            for rpart in product.right:
                if not rpart:
                    product.right.remove([])
