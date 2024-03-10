# python code obfuscation
import base64
from random import randint,seed

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

def obf_byte(code):
    r"""
    @brief : 코드를 \x유니코드 형태로 암호화
    @param : 난독화할 코드
    @return : exec(바이트코드) 형태의 문자열(단독으로도 실행가능)
    """
    ret = ""
    for byte in code:
        ret += f"\\x{ord(byte):02x}"
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
    code=obf_byte(code) # 한글호환성을 위해 최초1회 바이트로 바꿈
    for _ in range(repeat):
        if experiment(50):
            code=obf_base64(code)
        if experiment(50):
            code=obf_byte(code)
        if experiment(30):
            code=obf_xor(code)
    return formatting_code(code)

def formatting_code(code):
    r"""
    @brief : 코드 예쁘게 포장해주는 함수
    @param : 암호화가 완료된 코드
    @return : 포매팅이 완료된 최종 코드
    """
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
    
def main(filename=None,repeat=5):
    code,filename = read_file(filename)
    seed(len(code)) # 같은 결과를 보장하기 위해서
    code=obf(code,repeat)
    if write_file(filename,code):
        print("파일 저장 실패")

if __name__=="__main__":
    main("mini_ctf/main.py")
