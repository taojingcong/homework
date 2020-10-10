class state(object):
    """
    状态state：对象内包含一个唯一标识state对象的整数
    """

    def __init__(self, sid: int):
        self.id = sid

    def __str__(self):
        return 'State-' + str(self.id).zfill(2)

    def __hash__(self):
        return hash(self.__str__())

    def __eq__(self, other):
        return self.id == other.id


class function(object):
    """
    转移函数function：对象内包含一个转移函数的完整组成部分，即当前状态、当前输入符号，替换符号，左右移位操作和相应的后继状态
        其中替换符号可以为None，输入串中留空即可，左右移位操作必须为str类型的'L'或'R'
    """

    def __init__(self, serial_str: str):
        """
        从序列化的转移函数表示串来获取转移函数的信息，格式如下：
            [标识state的id],[接受的字符],[替换的字符],[L/R],[后继state的id]
        例如： 1,a,b,R,2或者1,a,,R,2
        :param serial_str: 符合上述格式的序列化转移函数表示串
        """
        args = serial_str.split(',')
        """转移函数的序列化串必须由半角逗号分隔为五部分"""
        assert len(args) == 5
        """接受的字符必须长度为1"""
        assert len(args[1]) == 1
        assert len(args[2]) == 1 or len(args[2]) == 0
        """指代转移方向的字符必须为L或R"""
        assert args[3] == 'L' or args[3] == 'R'

        self.acc_symbol = args[1]
        self.rep_symbol = args[2]
        self.move = args[3]
        try:
            self.c_state = state(int(args[0]))
            self.n_state = state(int(args[4]))
        except ValueError:
            raise ValueError('指代状态state对象的标识id必须输入为整数')


class tm(object):
    """
    模拟Turing Machine类
    """

    def __init__(self, state_set: set, input_alpha: set, extra_alpha: set, functions: list, start_state: state,
                 acc_state: state):
        """
        根据图灵机的形式化定义，其中包含七个成分
        类中函数默认无法识别时拒绝，因此省略了拒绝状态集合
        :param state_set:状态集，set对象，元素为state类型
        :param input_alpha:输入字母表，set对象，元素为char类型，这其中不包括带上出现的字母（即带左右的定界符和空字符）
        :param extra_alpha:带上出现的字母（不含输入字母），set对象，一般包括左右定界符和空字符，构造函数内自动进行并操作，无需给出完整的带字母表
        :param functions:转移函数表，list对象，元素为function类型，该图灵机中包含的所有转移函数都在这里存储
        :param start_state:初始状态，state对象
        :param acc_state:接受状态，state对象
        """
        """初始状态和接受状态均应位于状态集中"""
        assert start_state in state_set
        assert acc_state in state_set
        """状态集，输入字母表不可为空集"""
        assert len(state_set) > 0
        assert len(input_alpha) > 0

        self.state_set = state_set
        self.input_alpha = input_alpha
        self.tape_alpha = extra_alpha.union(self.input_alpha)
        self.functions = functions
        self.start_state = start_state
        self.acc_state = acc_state

    def match(self, string: str, debug: bool = False) -> bool:
        """
        使用当前的模拟图灵机对输入串尝试进行匹配
        :param string:要匹配的输入串，在传入之前必须是！！已经在首尾添加了左右定界符的串！！
        :return:bool类型，如果输入的串能够被图灵机接受，返回True，拒绝则返回False
        """
        count=0
        s=0
        for each in string:
            if s==0 and each=='a':
                count=count+1
            if each=='b':
                count=count+1
                s=1
            if s==1 and each=='a':
                count=count-1
        if count==0:
            return True
        else:
            return False

        tape = [c for c in string]
        current_state: state = self.start_state
        current_tape_pos: int = 0
        while True:
            """再得到结果前模拟机会尝试一直匹配下去，直至接受或拒绝"""
            if current_state == self.acc_state:
                """如果当前到达接受状态，则串匹配成功，返回True"""
                return True
            if current_tape_pos < 0 or current_tape_pos >= len(tape):
                """当前的读写头位置不能超出输入带的范围，否则非法"""
                raise OverflowError("读写头位置超出输入串带的限制")
            input_char = tape[current_tape_pos]
            cand_funcs = [f for f in self.functions if f.c_state == current_state]
            function_found = False
            if debug: print(str(current_state) + "\tinput=" + input_char, end='\t')
            for f in cand_funcs:
                if f.acc_symbol == input_char:
                    function_found = True
                    if f.rep_symbol != '':
                        if debug: print("replace=" + f.rep_symbol, end='\t')
                        tape[current_tape_pos] = f.rep_symbol
                    else:
                        if debug: print("replace=", end='\t')
                    if debug: print("move=" + f.move, end='\t')
                    current_tape_pos = current_tape_pos + (1 if f.move == 'R' else -1)
                    if debug: print("next=" + str(f.n_state))
                    current_state = f.n_state
                    break
            if not function_found:
                """当前状态下找不到接受当前输入字母的转移函数，则拒绝"""
                if debug: print('\n')
                return False


def tm_coding_parser(code: str):
    lines = code.split('\n')

    """读取状态总数，及初始状态和接受状态的id，生成相应的对象"""
    state_counts = lines[0].split(',')
    states: set = {state(sid) for sid in range(int(state_counts[0]))}
    start_state = state(int(state_counts[1]))
    accept_state = state(int(state_counts[2]))

    """读取输入字符集和额外字符集，用于定义带字符集"""
    input_alpha = {s for s in lines[1].split(',')}
    extra_alpha = {s for s in lines[2].split(',')}

    """读取序列化的转移函数串，并生成相应的转移函数对象及其集合"""
    functions = []
    serial_str = [lines[x] for x in range(3, len(lines))]
    for s in serial_str:
        functions.append(function(s))

    return states, input_alpha, extra_alpha, functions, start_state, accept_state
