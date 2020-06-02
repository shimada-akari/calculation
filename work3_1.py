def readNumber(line, index):
  number = 0
  while index < len(line) and line[index].isdigit():
    number = number * 10 + int(line[index])
    index += 1
  if index < len(line) and line[index] == '.':
    index += 1
    keta = 0.1
    while index < len(line) and line[index].isdigit():
      number += int(line[index]) * keta
      keta /= 10
      index += 1
  token = {'type': 'NUMBER', 'number': number}
  return token, index


def readPlus(line, index):
  token = {'type': 'PLUS'}
  return token, index + 1


def readMinus(line, index):
  token = {'type': 'MINUS'}
  return token, index + 1

def readMultiplied(line, index):
  token = {'type': 'MULTIPLIED'}
  return token, index + 1

def readDivided(line, index):
  token = {'type': 'DIVIDED'}
  return token, index + 1

def readBeginBracket(line, index):
  token = {'type': 'BEGIN_BRACKET'}
  return token, index + 1

def readEndBracket(line, index):
  token = {'type': 'END_BRACKET'}
  return token, index + 1


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index)
        elif line[index] == '+':
            (token, index) = readPlus(line, index)
        elif line[index] == '-':
            (token, index) = readMinus(line, index)
        elif line[index] == '*':
            (token, index) = readMultiplied(line, index)
        elif line[index] == '/':
            (token, index) = readDivided(line, index)
        elif line[index] == '(':
            (token, index) = readBeginBracket(line, index)
        elif line[index] == ')':
            (token, index) = readEndBracket(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)

        if line[index - 1] == '(':
            tokens.append({'type': 'PLUS'})
            
    return tokens

def mul_div(tokens, index, p_m_tokens, p_m_index):

    if tokens[index]['type'] == 'MULTIPLIED': #　*なら index - 1 の要素と index + 1 の要素をかける。
        number = p_m_tokens[p_m_index - 1]['number'] * tokens[index + 1]['number']
    
    elif tokens[index]['type'] == 'DIVIDED':
        if tokens[index + 1]['number']:
            number = p_m_tokens[p_m_index - 1]['number'] / tokens[index + 1]['number']

        else:
            print("ERROR!  division by zero")
            exit(1)
            

    new_tokens = {'type': 'NUMBER', 'number': number}
   
    return new_tokens

def 

def make_p_m_tokens(tokens): #掛け算割り算を計算し、足し算引き算のみを返す
    p_m_tokens = [] #掛け算と割り算を計算し、足し算と引き算のみにした辞書
    p_m_index = 0
    index = 0

    while index < len(tokens): 
        # print(tokens[index], index) #確認用
        if tokens[index]['type'] == 'MULTIPLIED' or tokens[index]['type'] == 'DIVIDED':
            new_tokens = mul_div(tokens, index, p_m_tokens, p_m_index)
            p_m_tokens[p_m_index - 1] = new_tokens #p_m_indexの最後の要素を計算済みの要素に置き換え
            index += 2 #　*or/の直後の数字は計算済みなので、tokensの要素は1つ飛ばす

        elif tokens[index]['type'] == 'PLUS' or tokens[index]['type'] == 'MINUS' or tokens[index]['type'] == 'NUMBER':
            p_m_tokens.append(tokens[index]) #掛け算、割り算以外のものはそのまま追加
            p_m_index += 1
            index += 1
           
        else:
            print('Invalid syntax')
            exit(1)
        # print(index) #確認用

    return p_m_tokens #足し算引き算のみのtokens

def m_l_culcuration(p_m_tokens): #tokens内の足し算引き算を計算(足し算と引き算のみになったtokensが引数)

    index = 0
    answer = 0
    while index < len(p_m_tokens):
        #print(p_m_tokens[index]) #確認用
        if p_m_tokens[index]['type'] == 'NUMBER':
            if p_m_tokens[index - 1]['type'] == 'PLUS':
                answer += p_m_tokens[index]['number']
            elif p_m_tokens[index - 1]['type'] == 'MINUS':
                answer -= p_m_tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer

def bracket_tokens(stack):
    index = len(stack) - 1
    end_bracket_index = len(stack)

    while stack[index]['type'] != 'BEGIN_BRACKET':
        index -= 1

    begin_bracket_index = index
    tokens = stack[begin_bracket_index + 1 : end_bracket_index] #括弧内のtokens （括弧は含まない）

    # print("bracket_tokens") #確認用
    # print(tokens)

    p_m_tokens = make_p_m_tokens(tokens) # -> p_m_tokens : 足し算引き算のみのtokens
    tmp_answer = m_l_culcuration(p_m_tokens) #tmp_answer : 括弧内の計算結果

    # print(tmp_answer)#確認用

    add_tokens = {'type': 'NUMBER', 'number': tmp_answer}
    stack = stack[:begin_bracket_index]
    stack.append(add_tokens)

    return stack

def evaluate(tokens):

    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    tokens.insert(0, {'type': 'BEGIN_BRACKET'})
    tokens.append({'type': 'END_BRACKET'})

    index = 0
    no_bracket_tokens = []
    stack = []
    
    while index < len(tokens): 
        if tokens[index]['type'] == 'END_BRACKET':
            stack = bracket_tokens(stack) #bracket_tokensにstack -> 括弧内を計算した、tokens
        else:
            stack.append(tokens[index])
        index += 1

    # print(stack)
    return stack[0]['number']

def test(line):
    tokens = tokenize(line)
    
    actualAnswer = evaluate(tokens)
    expectedAnswer = eval(line)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expectedAnswer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))


# Add more tests to this function :)
def runTest():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")
    print("==== Test finished! ====\n")

    test("9*3")
    test("6.5*7.2")

    test("12/4")
    test("18.5/0.5")

    test("-7+5")
    test("-8/4")
    test("10.0/2+9/3.0")
    test("2*7-20/10")
        
    test("-2.0*6+4*3.0-6.2/0.2")
    test("-2.0*6+4*3.0*6.2/0.2")

    test("0")

    test("(1+2)*(4+5)")
    test("(1+2)*(4+5)*(7+8)")
    test("(-3.0+2)*2*3")
    test("2*3/(-3.0+1)")
    test("2*3/(-3.0+1)*(7-3)")
    test("2*3/(-3.0+1)*(7-3)+4-3.0")
    test("5+2*3/(-3.0+1)*(7-3)+4-3.0")
    test("(1+5)")
    test("-3+(1+5)")
    test("-3+(9*0)+2.0")
    
    test("-(1+5)")
    test("9/0")


runTest()

while True:
  print('> ', end="")
  line = input()
  tokens = tokenize(line)
  answer = evaluate(tokens)
  print("answer = %f\n" % answer)



