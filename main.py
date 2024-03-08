# python code obfuscation
import base64

def obf(code):
    encoded_code=base64.b64encode(code.encode()).decode()
    return f"exec(base64.b64decode(('{encoded_code}')).decode())"

def formatting_code(code):
    return f"""import base64
    
if __name__=="__main__":
    {code}"""

def main(filename=None,repeat=10):
    try:
        source_code=open(filename,"r").read()
    except:
        source_code="""print("Test message");
print("File not selected")"""
    for _ in range(repeat):
        source_code=obf(source_code)
    source_code=formatting_code(source_code)
    print(source_code)
    
if __name__=="__main__":
    main()
