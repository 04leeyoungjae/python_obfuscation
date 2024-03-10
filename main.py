# python code obfuscation
import base64
from random import randint

def experiment(probability):
    r"""
    @breif : (probabilty %)의 확률로 1 반환
    @param : 몇 퍼센트의 확률로 1을 반환할지 설정
    @return : 1 또는 0 (bool)
    """
    experiment=randint(1,100)
    if probability<=experiment:
        return 1
    else:
        return 0

def obf_byte(code):
    r"""
    @breif : 코드를 \x유니코드 형태로 암호화
    @param : 난독화할 코드
    @return : exec(바이트코드) 형태의 문자열(단독으로도 실행가능)
    """
    ret = ""
    for byte in code:
        ret += f"\\x{ord(byte):02x}"
    return f"exec('{ret}')"

def obf_base64(code):
    r"""
    @breif : 코드를 base64로 암호화
    @param : 암호화할 코드
    @return : base64로 암호화된 완전한 파이썬 코드(단독으로도 실행가능)
    """
    encoded_code=base64.b64encode(code.encode()).decode()
    return f"exec(__import__('base64').b64decode(('{encoded_code}')))"

def obf(code):
    r"""
    @breif : 코드를 확률에 따라 암호화하여 복호화가 까다롭게 하는 코드
    @param : 암호화할 코드
    @return : 최종적으로 암호화가 완료된 코드
    """
    if experiment(50):
        code=obf_base64(code)
    if experiment(30):
        code=obf_byte(code)
    return code

def formatting_code(code):
    r"""
    @brief : 코드 예쁘게 포장해주는 함수
    @param : 암호화가 완료된 코드
    @return : 포매팅이 완료된 최종 코드
    """
    return f"""if __name__=="__main__":
    {code}"""

def main(filename=None,repeat=5):
    try:
        source_code=open(filename,"r",encoding="utf-8").read()
    except:
        source_code="""print("Hello, World!")"""
    for _ in range(repeat):
        source_code=obf(source_code)
    source_code=formatting_code(source_code)
    print(source_code)
    exec(source_code)

if __name__=="__main__":
    main()
