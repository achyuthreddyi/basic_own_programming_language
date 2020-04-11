# constants
DIGITS = '0123456789'
#  error class
class Error:

    def __init__(self,pos_start,pos_end,error_name,details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error} : {self.details}'
        result += f'File{self.pos_start.fn},line {self.pos_start.ln + 1}'
        return result

#  subclass for creating the illegal characters in errror class
class illegalCharError(Error):
    def __init__(self,pos_start,pos_end, details):
        super().__init__(pos_start,pos_end,'Illegal character',details)



# position
class Position :
    def __init__(self,idx,ln,cl, fn,ftxt):
        self.idx = idx
        self.ln = ln
        self.cl = cl
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char):
        self.idx +=1
        self.cl +=1                

        if current_char == '\n':
            self.ln  += 1
            self.cl  = 0
        return self

    def copy(self):
        return Position (self.idx, self.ln,self.cl, self.fn, self.ftxt)

#  TOKEN TYPES

TT_INT = 'TT_INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL =  'MUL'
TT_DIV =  'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'

class Token :
    def __init__(self, type_ , value = None):
        self.type = type_
        self.value = value
    
    def __repr__(self):
        if self.value : return f'{self.type} : {self.value}' 
        return f'{self.type}'

#  lexer

class Lexer:
    def __init__(self,fn,text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1,0,-1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos< len(self.text) else None

    def make_tokens(self):
        tokens = []
        while self.current_char !=None:
            if self.current_char in '\t': 
                self.advance()

            elif self.current_char in DIGITS:
                tokens.append(self.makenumber())
                self.advance()

            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()

            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()

            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
                
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()

            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()

            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            elif self.current_char == ' ':
                self.advance()

            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [],illegalCharError(pos_start,self.pos,"'" + char +"'")


        return tokens, None

    #  since number has more than one digit 
    def makenumber(self):
        num_str = ''
        dot_count = 0 

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1 : break
                dot_count += 1
                num_str += '.'
            else: 
                num_str += self.current_char
            self.advance()

        if dot_count ==0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT,float(num_str))
#  run 

def run(fn,text):
    lexer = Lexer(fn,text)
    tokens ,error = lexer.make_tokens()

    return tokens, error       







