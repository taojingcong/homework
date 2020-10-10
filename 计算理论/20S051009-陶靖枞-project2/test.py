"""
编码图灵机的字符串，格式如下：
    第一行：总状态数，初始状态id，接受状态id【默认id是从0到状态数之间的整数】
    第二行：输入字符，逗号分隔
    第三行：额外字符，用于tape，会在TM内和输入字符集做并操作
    第四行开始每行一个表示转移函数的序列化串，格式见function类中的定义
"""
tm_code = "17,0,16\n" \
          "a,b,c,d\n" \
          "@, ,x,y,z,w\n" \
          "0,@,,R,1\n" \
          "1,a,,R,2\n" \
          "2,a,,R,2\n" \
          "2,b,,R,3\n" \
          "3,b,,R,3\n" \
          "3,c,,R,4\n" \
          "4,c,,R,4\n" \
          "4,d,,R,5\n" \
          "5,d,,R,5\n" \
          "5, ,,L,6\n" \
          "6,a,,L,6\n" \
          "6,b,,L,6\n" \
          "6,c,,L,6\n" \
          "6,d,,L,6\n" \
          "6,@,,R,7\n" \
          "7,a,x,R,8\n" \
          "7,b,,L,14\n" \
          "8,a,,R,8\n" \
          "8,b,y,R,9\n" \
          "8,c,,L,13\n" \
          "9,b,,R,9\n" \
          "9,c,z,R,10\n" \
          "9,w,,L,12\n" \
          "10, ,,L,16"

from turingmachine import tm, tm_coding_parser

if __name__ == "__main__":
    states, input_alpha, extra_alpha, functions, start_state, accept_state = tm_coding_parser(tm_code)
    machine = tm(state_set=states, input_alpha=input_alpha, extra_alpha=extra_alpha, functions=functions,
                 start_state=start_state, acc_state=accept_state)
    while True:
        string = input("input a string to match:")
        print("ACCEPTED!" if machine.match(string) else "REJECTED!")
