"""
题目2：正则表达式转NFA
"""
import copy

EPSILON = 'ϵ'


class state(object):
    __state_no: int = 0  # 建议的类型，初始为0

    def __init__(self):
        state.__state_no = state.__state_no + 1  # 每有一个新的状态就加1
        self.name: str = str(state.__state_no)  # 与下面对应，直接会输出名字
        self.func = {}

    def __str__(self):
        return '(state-' + str(self.name) + ')'

    def append(self, alphabet: str, succ):  # 添加转移函数
        try:
            self.func[alphabet].append(succ)  # 添加succ
        except KeyError:  # 如果字典中没有key就创建一个
            self.func[alphabet] = [succ]

    def eps_closure(self) -> set:
        global EPSILON
        current: set = {self}
        new_set: set = {self}
        # 如果没有通过epsilon转移的函数，则返回它自身
        try:
            self.func[EPSILON]
        except KeyError:
            return {self}
        # 不断向后扩展，直至这个集合不再变化
        # 不可采用递归方法，假设两个状态相互通过epsilon转移，则会导致死循环
        while True:
            for st in current:
                try:
                    new_set = new_set.union(st.func[EPSILON])
                except KeyError:
                    pass
            new_set.union(current)
            if len(new_set.difference(current)) == 0:
                break
            current = new_set
        return new_set


class nfa(object):
    def __init__(self, all_states: set, alpha: set, start_state: state, final_states: set):
        self.all_states = all_states
        self.alpha = alpha
        self.start_state = start_state
        self.final_states = final_states

    def printf(self):
        """
        向控制台输出该NFA的信息，包括字母表，初态，终态和转移函数信息
        """
        print('Alphabet = {' + ','.join([a for a in self.alpha]) + '}')
        print('Start State = ' + str(self.start_state))
        print('Final States = {' + ','.join([str(fs) for fs in self.final_states]) + '}')
        print('Transfer Functions:')
        for s in self.all_states:
            for f in s.func:  # f是转移的trigger
                fun = s.func.get(f)
                if fun is not None:  # 即有转移的目标
                    print('\t' + str(s) + '|---' + str(f) + '--->' + ','.join([str(e) for e in fun]))
        print('\n')

    @staticmethod
    def concat(a1, a2):
        global EPSILON
        if a1 is None:
            return a2
        if a2 is None:
            return a1
        """
        依据课本P36关于正则表达式连接运算的证明

        新NFA的：
        1.全部状态为原来两个NFA的状态的并集
        2.字母表为原来两个NFA的字母表并集（一般字母表二者是一样的）
        3.起始状态为前者的起始状态
        4.接受状态为后者的接受状态
        5.转换函数为原来两个NFA的转换函数的并集，此外还有从前者每一个接受状态到后者起始状态的转换
        """
        n_alpha: set = a1.alpha.union(a2.alpha).union(EPSILON)
        n_start_state: state = a1.start_state
        n_final_states: set = a2.final_states
        for s in a1.final_states:#连接a2的初态和a1的终态
            s.append(alphabet=EPSILON, succ=a2.start_state)
        n_all_states: set = a1.all_states.union(a2.all_states)  # 应当先连接a1的终态和a2的初态，先进行union操作会使这部分连接无法更新到所需的新NFA中
        return nfa(all_states=n_all_states, alpha=n_alpha, start_state=n_start_state, final_states=n_final_states)

    @staticmethod
    def concat_multiple(nfa_stack: list):
        # 多个NFA的顺序连接，自参数栈顶开始
        if len(nfa_stack) < 1:
            raise ValueError
        automata = nfa_stack.pop()
        while len(nfa_stack) > 0:
            automata = nfa.concat(automata, nfa_stack.pop())
        return automata

    @staticmethod
    def union(a1, a2):
        global EPSILON
        if a1 is None:
            return a2
        if a2 is None:
            return a1
        """
        依据课本P35关于正则表达式并运算的证明
        新NFA的：
        1.全部状态为原来两个NFA的状态的并集，以及一个新的作为起始状态的状态
        2.字母表为原来两个NFA的字母表并集（一般字母表二者是一样的）
        3.起始状态为新生成的状态
        4.接受状态为二者接受状态的并集
        5.转换函数为原来两个NFA的转换函数的并集，此外还有从新起始状态到原来二者各自起始状态的转换
        """
        n_start_state: state = state()
        n_all_states: set = {n_start_state}.union(a1.all_states).union(a2.all_states)
        n_alpha: set = a1.alpha.union(a2.alpha).union(EPSILON)
        n_final_states: set = a1.final_states.union(a2.final_states)
        n_start_state.append(alphabet=EPSILON, succ=a1.start_state)
        n_start_state.append(alphabet=EPSILON, succ=a2.start_state)
        return nfa(all_states=n_all_states, alpha=n_alpha, start_state=n_start_state, final_states=n_final_states)

    @staticmethod
    def union_multiple(nfa_stack: list):
        # 多个NFA的顺序并操作，自参数栈顶开始
        if len(nfa_stack) < 1:
            raise ValueError
        automata = nfa_stack.pop()
        while len(nfa_stack) > 0:
            automata = nfa.union(automata, nfa_stack.pop())
        return automata

    @staticmethod
    def closure(automata):
        global EPSILON
        """
        依据课本P37关于正则表达式闭包运算的证明
        新NFA的：
        1.全部状态为原来两个NFA的状态的并集，以及一个新的作为起始状态的状态，并且这个状态亦是一个接受状态
        2.字母表保持不变（如果原来没有ϵ则加入进去）
        3.起始状态为新生成的状态
        4.接受状态为原来接受状态外加新生成的状态
        5.转换函数为原来的转换函数集以及更新后的所有接受状态到原来起始状态的转换
        """
        old_start_state: state = automata.start_state
        n_start_state: state = state()
        n_all_states: set = {n_start_state}.union(automata.all_states)
        n_alpha: set = automata.alpha.union(EPSILON)
        n_final_states: set = automata.final_states.union({n_start_state})
        for s in n_final_states:
            s.append(alphabet=EPSILON, succ=old_start_state)
        return nfa(all_states=n_all_states, alpha=n_alpha, start_state=n_start_state, final_states=n_final_states)

    @staticmethod
    def get_alpha(alpha: str):
        # 获取仅接受一个字母或epsilon的NFA
        if len(alpha) != 1:
            raise ValueError
        global EPSILON
        if alpha == EPSILON:
            uni_s: state = state()
            return nfa(all_states={uni_s}, alpha=set(EPSILON), start_state=uni_s, final_states={uni_s})
        else:
            s = state()
            e = state()
            s.append(alphabet=alpha, succ=e)
            return nfa(all_states={s, e}, alpha={alpha}, start_state=s, final_states={e})

    # def match(self, string: str) -> bool:
    #     current_states: set = {self.start_state}
    #
    #     def has_final(sets: set, final: set) -> bool:
    #         for st in sets:
    #             if st in final:
    #                 return True
    #         return False
    #
    #     for ch in string:
    #         new_states: set = set([])
    #         # 对当前状态集里的每一个状态,对从此状态出发的所有转移进行遍历
    #         # 如果某个状态的转移所接受的字母是当前字符，就把后继状态加入到新的状态集里面
    #         for st in current_states:
    #             # 先扩展当前状态的epsilon闭包。如果转换成DFA，闭包内的状态和当前状态实际上是DFA中的同一个状态
    #             new_states = new_states.union(st.eps_closure())
    #         current_states = copy.deepcopy(new_states)
    #         new_states.clear()
    #         succ: bool = False  # 标记，如果当前状态集里的状态均不接受当前字符，则匹配失败
    #         for st in current_states:
    #             for key in st.func:
    #                 if key == ch:
    #                     succ = True
    #                     for sss in st.func[key]:
    #                         new_states = new_states.union(sss.eps_closure())
    #         if not succ:
    #             return False
    #         current_states = copy.deepcopy(new_states)
    #     # 检查，如果当前状态集里包含终态，则识别成功，输入串符合指定的正则语言
    #     if has_final(current_states, self.final_states):
    #         return True
    #     return False


class regex(object):
    def __init__(self, exp: str = EPSILON):
        self.exp = exp

    def compile(self) -> nfa:
        """
        非递归方法，由当前正则表达式对象生成对应的NFA
        由于是直接连接，因此会产生一定量的多余状态
        """
        """
        以下是非递归过程中用到的数据结构
        """
        # 保存识别过程中产生的NFA
        nfa_stack = []
        # 标志栈，元素为二分量的元组。记录识别过程中NFA栈对应位置的括号层级，以及连接标志
        # 格式为：（当前括号层级，当前连接标志）
        # 括号层级：每嵌套一层则层级加大，遇左括号自增，右括号自减
        # 连接标志：由于并运算符|的存在，需要在遇到右括号以及表达式结束时 \
        #           将栈顶若干个括号层级与连接标志均相同的NFA进行连接操作，\
        #           之后再将栈顶若干个括号层级相同的NFA进行并操作，因此需要标记栈内哪些NFA是直接连接的
        flag_stack = []
        # 为了区分不同括号内的并运算数量，这里需要标记下来进入括号时当前的连接标志，退出这一层时以便恢复
        concat_stack = []

        non_alpha: list = ['(', ')', '|', '*']  # 这里记录的是非字母符号
        current_level = 0  # 当前的括号层级
        current_concat_flag = 0  # 识别当前的连接的标记，每次遇到并运算符才发生改变

        # 考虑到正则表达式中出现的字母连接是没有符号表示的，需要判断是否为连接的合适时机
        def reduce_concat():
            nonlocal current_concat_flag, current_level, flag_stack, nfa_stack
            tmp_s = []
            # 弹出所有和当前栈顶concat值及level值均相同的NFA，进行连接操作，然后压入
            while len(flag_stack) > 0 \
                    and flag_stack[-1][0] == current_level \
                    and flag_stack[-1][1] == current_concat_flag:
                tmp_s.append(nfa_stack.pop())
                flag_stack.pop()
            nfa_stack.append(nfa.concat_multiple(tmp_s))
            flag_stack.append((current_level, current_concat_flag))

        def reduce_union():
            nonlocal current_concat_flag, current_level, flag_stack, nfa_stack
            tmp_s = []
            # 弹出所有当前栈顶level值相同的NFA进行并操作，然后压入，再压入该括号之前的concat值以及新的level值
            while len(flag_stack) > 0 and flag_stack[-1][0] == current_level:
                tmp_s.append(nfa_stack.pop())
                flag_stack.pop()
            nfa_stack.append(nfa.union_multiple(tmp_s))

        # 循环处理输入符号
        for ch in self.exp:
            if ch not in non_alpha:
                """
                如果当前输入符号是一个字母（或epsilon），则生成一个NFA并入栈，同时入栈括号层级以及连接标志数
                """
                automaton = nfa.get_alpha(ch)
                nfa_stack.append(automaton)
                flag_stack.append((current_level, current_concat_flag))
                continue
            if ch == '*':
                """
                如果当前输入符号是闭包符号*，则从栈顶取出最后入栈的NFA，对其进行闭包操作后再入栈
                保证仅取出栈顶的NFA即可，可以证明闭包操作仅影响栈顶NFA，因此标记栈无需进行操作
                """
                automaton = nfa_stack.pop()
                automaton = nfa.closure(automaton)
                nfa_stack.append(automaton)
                continue
            if ch == '(':
                """
                如果当前输入符号是左括号（，直接自增括号层级，并入栈当前的连接标志，无需其他操作
                """
                concat_stack.append(current_concat_flag)#
                current_level = current_level + 1
                current_concat_flag = current_concat_flag + 1
                continue
            if ch == '|':
                """
                如果当前输入符号是并运算符|，则需要将目前栈内顶部若干个连接标记数与当前对应值相同的NFA全部取出并进行连接操作
                再改变当前连接标记
                注意：考虑到括号带来的层级改变，需要同时保证括号层级和连接标记均一致
                """
                # 把栈顶所有与当前level和concat值一样的全部弹出并进行连接连接，再压入栈中，相应个数的level和concat也弹出，然后压入一个level和concat值
                reduce_concat()
                # 由于进行了并操作，后续的NFA不应再与栈内的NFA进行连接，使连接标记数自增以示区分
                current_concat_flag = current_concat_flag + 1
                continue
            if ch == ')':
                """
                如果当前的输入符号是右括号）：
                首先：假设当前括号内遇到过并操作符，则需要把连接标志及括号层级都与当前对应两值相同的先弹出，连接后再入栈
                接着：此时栈顶所有括号层级相同的NFA应全部弹出进行并操作，然后将结果入栈
                以上的栈操作均同步进行括号层级栈以及连接标记栈的操作
                """
                # 类似编译器语法分析阶段的归约操作，将栈内本层括号范围内的NFA进行连接或并操作以生成一个NFA
                reduce_concat()
                reduce_union()
                # 恢复concat值为匹配的括号部分之前的值
                current_concat_flag = concat_stack.pop()
                current_level = current_level - 1
                flag_stack.append((current_level, current_concat_flag))
        """
        此时到达了串的结尾，栈内应至少有一个NFA，考虑到有可能是多个正则的并运算，这时候操作应和遇到右括号时操作一致
        操作完成后，如果NFA栈内仅有一个NFA并且其他两个栈为空，则该正则表达式识别成功，NFA栈顶即为生成的最终NFA
        """
        reduce_concat()
        reduce_union()
        # 如果栈内只有一个NFA并且标志栈为空即为翻译成功，结果得到的NFA位于NFA栈顶
        if len(nfa_stack) == 1 and len(flag_stack) == 0:
            return nfa_stack[-1]
        # 其他情况报错，说明输入的表达式不是正则表达式
        else:
            raise ValueError('exp is not a regular expression')


if __name__ == '__main__':
    # r: str = r'(ab*a|ab(a)*)(a|b*)'
    r=""
    with open("re",'r') as f:
        r=f.readline()
    print(r)
    pattern = regex(r)
    a = pattern.compile()
    print('NFA corresponding to given regular expression "' + r + '" is:')
    a.printf()
    # while True:
    #     s = input('input string to match (press enter to exit):')
    #     if len(s) < 1:
    #         break
    #     if a.match(s):
    #         print('PASS!')
    #     else:
    #         print('INVALID!')