# 																			实验一

## 实验目的

​			Write a program to match IP address with regular expression. It is required to match the legitimate IP address format correctly

## 实验思路

​			the regular expression of ipv4 address in python is (((\d{1,2})|(1\d{1,2})|(2[0-4]\d)|(25[0-5]))\.){3}((\d{1,2})|(1\d{1,2})|(2[0-4]\d)|(25[0-5]))，which we can match with re.match()

## 实验结果

![image-20200918204220192](C:\Users\DASD\AppData\Roaming\Typora\typora-user-images\image-20200918204220192.png)

![image-20200918204250511](C:\Users\DASD\AppData\Roaming\Typora\typora-user-images\image-20200918204250511.png)

​			

​			We can see that when the ip=10.249.40.115, it matches. When the ip =100, it isn't match.











# 																			实验二

## 实验目的

​			Write a program to realize the conversion from regular expression to non deterministic finite automata (NFA)

## 实验思路

​			first we need to know how to express NFA$(Q,\sum,\delta,q_1,F)$,

​			Set two classes, one is state and the other is NFA. State is a single, recording the state transition function. NFA records all States, characters, start and end states.

​			Set a regex class, which mainly contains a compile function to receive the regular expression and return the matching NFA.

​		 	**使用到的数据结构包括：**

​			 nfa_stack saves the NFA generated in the process of identification

​			 flag_stack sign stack，The element is a binary tuple. Record the bracket level at the corresponding position of NFA stack during the identification process, and the connection flag in the format of (current bracket level, current connection flag). Bracket level: each nesting level will increase, and the left bracket will increase and the right bracket will decrease. Connection flag: due to the existence of the union operator |, it is necessary to connect several NFAS with the same connection flag at the top of the stack when the right bracket and the end of the expression are encountered, and then merge several NFAS with the same bracket level at the top of the stack. Therefore, it is necessary to mark which NFAS in the stack are directly connected.

​			concat_stack In order to distinguish the number of union operations in different brackets, it is necessary to mark the current connection flag when entering the bracket, and to recover when exiting this layer

​			non_alpha: list = ['(', ')', '|', '*']    The non alphabetic symbols are recorded here

​			current_level = 0  # Current bracket level

​			current_concat_flag = 0  # The tag that identifies the current connection. The join operator changes each time it encounters it

​			**在循环处理输入符号的时候**

- ​	 If the current input symbol is a letter (or epsilon), an NFA is generated to merge into the stack, and the bracket level and the number of connection flags are put on the stack

- ​    If the current input symbol is a closure symbol *, the last NFA is taken from the top of the stack, and then the NFA is put into the stack after the closure operation to ensure that only the NFA at the top of the stack is removed. It can be proved that the closure operation only affects the NFA at the top of the stack, so there is no need to mark the stack

- ​     If the current input symbol is the left bracket (, the bracket level will be increased directly, and the current connection flag of the stack will be merged. No other operation is required

- ​      If the current input symbol is a union operator |, all NFAS with the same number of connection marks at the top of the stack and the current corresponding value need to be taken out and connected before changing the current connection mark

- ​      If the current input symbol is a right bracket ）：
  ​      first：Assuming that a join operator has been encountered in the current bracket, you need to pop up the connection flag and bracket level that are the same as the current corresponding two values, and then put them on the stack after connecting

  ​      then：At this time, all NFAS with the same bracket level at the top of the stack should be popped up and operated, and then the result will be put on the stack
  ​     The above stack operations are synchronized with bracket level stack and connection mark stack

- ​       If the end of the string is reached, there should be at least one NFA in the stack. Considering that there may be multiple regular union operations, the operation should be the same as when the right bracket is encountered
  ​       After the operation is completed, if there is only one NFA in the NFA stack and the other two stacks are empty, the regular expression recognition is successful, and the top of the NFA stack is the final NFA generated

## 实验结果			

![image-20200918201259437](C:\Users\DASD\AppData\Roaming\Typora\typora-user-images\image-20200918201259437.png)

As shown in the figure, read the regular formula (AB * a | AB (a) *) (a | b *) from the file re, and call the complie function to parse to get NFA