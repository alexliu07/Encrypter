import sys,base64,random,hashlib
#获取参数
mode = sys.argv[1]
text = sys.argv[2]
code = sys.argv[3]
#模式为加密
if mode == 'encrypt':
    #密码加密
    code_md5 = hashlib.md5(code.encode()).hexdigest()
    while True:
        #移位
        randomnum = random.randint(0,9)
        code_en = []
        status = 0
        for i in code_md5:
            if ord(i)+randomnum > 126 or ord(i)+randomnum < 33:
                status = 1
            code_en.append(chr(ord(i)+randomnum))
        if status == 1:
            continue
        code_en = str(randomnum)+''.join(code_en)
        if '<' in code_en or '>' in code_en or '\\' in code_en or '^' in code_en:
            continue
        else:
            break 
    #加密内容
    content = base64.b64encode(text.encode(encoding='utf-8')).decode(encoding='utf-8')
    #移位
    while True:
        randomnum = random.randint(0,9)
        content_en = []
        status = 0
        for i in content:
            if ord(i)+randomnum > 126 or ord(i)+randomnum < 33:
                status = 1
            content_en.append(chr(ord(i)+randomnum))
        if status == 1:
            continue
        content_en = str(randomnum)+''.join(content_en)
        if '<' in content_en or '>' in content_en or '\\' in content_en or '^' in content_en:
            continue
        else:
            break
    #输出
    print('加密完成，加密后的字符串为：\n'+code_en+content_en)
elif mode == 'decrypt':
    #加密的内容
    numb = int(text[0])
    file_code = text[1:33]
    #获取md5
    code_md5 = []
    for i in file_code:
        code_md5.append(chr(ord(i)-numb))
    code_md5 = ''.join(code_md5)
    #验证文件密钥
    if hashlib.md5(code.encode()).hexdigest() == code_md5:
        #解密移位
        b64t = []
        for i in text[34:]:
            b64t.append(chr(ord(i)-int(text[33])))
        b64t = ''.join(b64t)
        #解密内容
        file_content = base64.b64decode(b64t.encode()).decode()
        print('解密完成，内容为：\n'+file_content)
    else:
        print('密码错误')