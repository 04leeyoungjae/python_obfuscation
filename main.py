# python code obfuscation
import ast
import astor
import base64
from itertools import combinations_with_replacement
from random import randint,seed,shuffle

def experiment(probability):
    r"""
    @brief : (probabilty %)의 확률로 1 반환
    @param : 몇 퍼센트의 확률로 1을 반환할지 설정
    @return : 1 또는 0 (bool)
    """
    experiment=randint(1,100)
    if probability>=experiment:
        return 1
    else:
        return 0
    
def obf_varname(code):
    def generate_predefined_list(length):
        string = "O0BD8"
        non_numeric_combinations = []
        
        for combination in combinations_with_replacement(string, length):
            if not combination[0].isdigit():
                non_numeric_combinations.append(''.join(combination))
        shuffle(non_numeric_combinations)
        
        return non_numeric_combinations
    
    variables=list()
    reserved_filter=list(dir(__builtins__))
    new_varname=dict()
    index=0
    predefined_list=list(generate_predefined_list(16))  

    def extract_module(node):
        if isinstance(node,ast.Import) or (isinstance(node,ast.ImportFrom) and node.names[0].name!="*"):
            for module in node.names:
                reserved_filter.append(module.name)
        elif isinstance(node,ast.ImportFrom) and node.names[0].name=="*":
            for function in dir(__import__(node.module)):
                reserved_filter.append(function)
                
    def extract_var(node):
        nonlocal index
        if isinstance(node,ast.Name):
            if node.id in reserved_filter or node.id.startswith("__"):
                new_varname[node.id]=node.id
                return
            elif node.id not in new_varname:
                new_varname[node.id]=predefined_list[index]
                index+=1
                variables.append(node.id)
            else:
                pass
            
    def extract_global_var(node):
        nonlocal index
        if isinstance(node,ast.Global):
            global_var=node.names[0]
            if global_var in reserved_filter or global_var.startswith("__"):
                new_varname[global_var]=global_var
            elif global_var not in new_varname:
                new_varname[global_var]=predefined_list[index]
                index+=1
                variables.append(global_var)
            else:
                pass
            
    def extract_fucntion(node):
        nonlocal index
        if isinstance(node,ast.FunctionDef):
            if node.name in reserved_filter or node.name.startswith("__"):
                new_varname[node.name]=node.name
                return
            elif node.name not in new_varname:
                new_varname[node.name]=predefined_list[index]
                index+=1
                variables.append(node.name)
            else:
                pass

    def extract_param(node):
        nonlocal index
        if isinstance(node,ast.FunctionDef):
            for arg in node.args.args:
                if arg.arg in reserved_filter:
                    new_varname[arg.arg]=arg.arg
                    return
                elif arg.arg not in new_varname:
                    new_varname[arg.arg]=predefined_list[index]
                    index+=1
                    variables.append(arg.arg)
                else:
                    pass
            
    def rename(node):
        if isinstance(node,ast.Name):
            node.id=new_varname[node.id]
        elif isinstance(node,ast.Global):
            node.names[0]=new_varname[node.names[0]]
        elif isinstance(node,ast.FunctionDef):
            node.name=new_varname[node.name]
            for arg in node.args.args:
                arg.arg=new_varname[arg.arg]
        else:
            pass
    
    tree=ast.parse(code)
    for node in ast.walk(tree):
        extract_module(node)
        extract_var(node)
        extract_global_var(node)
        extract_fucntion(node)
        extract_param(node)
        rename(node)
    
    return astor.to_source(tree)

def obf_byte(code):
    r"""
    @brief : 코드를 \x유니코드 형태로 암호화
    @param : 난독화할 코드
    @return : exec(바이트코드) 형태의 문자열(단독으로도 실행가능)
    """
    ret = ""
    for byte in code:
        if ord(byte)<=0x7E: #한글깨짐 방지
            ret += f"\\x{ord(byte):02x}"
        else:
            ret += byte
    return f"exec('{ret}')"

def obf_base64(code):
    r"""
    @brief : 코드를 base64로 암호화
    @param : 암호화할 코드
    @return : base64로 암호화된 완전한 파이썬 코드(단독으로도 실행가능)
    """
    encoded_code=base64.b64encode(code.encode()).decode()
    return f"exec(__import__('base64').b64decode(('{encoded_code}')))"

def obf_xor(code="print(1)",key = randint(130,200)):
    r"""
    @brief : 코드를 xor로 암호화
    @param : 암호화할 코드
    @return : key와 code를 xor 연산으로 한 글자모음
    
    # 주의 : obf_xor 시행이 많아지면 syntax에러가 발생할 수도 있음
    """
    def encrypt(code, key):
        encrypted_message = ""
        for char in code:
            encrypted_message += chr(ord(char) ^ key)
        return encrypted_message

    encrypted_message = encrypt(code, key)
    decrypted_message = f"exec((lambda x:\"\".join([chr(ord(char)^{key}) for char in x]))(r\"\"\"{encrypted_message}\"\"\"))"
    return decrypted_message

def obf(code,repeat):
    r"""
    @brief : 코드를 확률에 따라 암호화하여 복호화가 까다롭게 하는 코드
    @param code : 암호화할 코드
    @param repeat : 암호화를 시행할 횟수
    @return : 최종적으로 암호화가 완료된 코드
    """
    code=obf_varname(code)
    for _ in range(repeat):
        if experiment(10):
            code=obf_base64(code)
        if experiment(50):
            code=obf_byte(code)
        if experiment(30): 
            code=obf_xor(code)
    if repeat:
        return formatting_code(code)
    else:
        return code

def formatting_code(code,indent="    "):
    r"""
    @brief : 코드 예쁘게 포장해주는 함수
    @param : 암호화가 완료된 코드
    @return : 포매팅이 완료된 최종 코드
    """
    code="\n".join([indent+line for line in code.split("\n")])
    return f"""if __name__=="__main__":
{code}"""
    
def read_file(filename):
    r"""
    @brief : 파일에서 코드를 읽어오는 함수
    @param filename : 파이썬 코드를 읽어올 파일
    @return : 읽어온 코드와 filename으로 이루어진 튜플
    """
    try:
        source_code=open(filename,"r",encoding="utf-8").read()
    except:
        source_code="""print("Hello, World!")"""
        filename="main.py"
    return source_code,filename

def write_file(filename,code):
    r"""
    @brief : 완성된 코드를 담은 py 파일을 생성하는 함수
    @param filenmae : 소스코드를 읽어왔던 파일
    @param code : 저장할 코드
    @return : 저장성공여부(0:성공 1:실패)
    """
    print(code)
    try:
        with open( (filename.split(".")[0]+"_obfuscation.py"), "w", encoding="utf-8") as f: #filename.py -> filename_obfuscation.py
            f.write(code)
        return 0
    except:
        return 1
    
def main(filename=None,repeat=1):
    code,filename = read_file(filename)
    seed(len(code)) # 같은 결과를 보장하기 위해서
    code=obf(code,repeat)
    if write_file(filename,code):
        print("파일 저장 실패")

if __name__=="__main__":
    main(__file__,repeat=0)
