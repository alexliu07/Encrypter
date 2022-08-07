import sys,base64,random,hashlib,os
#获取参数
mode = sys.argv[1]
file = sys.argv[2].replace('\\','/').replace('"','')
code = sys.argv[3]
#获取文件夹及文件名
fpath = os.path.split(file)[0]
fname = os.path.splitext(os.path.split(file)[1])[0]
#模式为加密
if mode == 'encrypt':
    #读取文件
    source = open(file,'rb')
    #加密文件
    source_byte = base64.b64encode(source.read()).decode()
    source.close()
    while True:
        #移位
        randomnum = random.randint(0,9)
        source_byte_en = []
        status = 0
        for i in source_byte:
            if ord(i)+randomnum > 126 or ord(i)+randomnum < 33:
                status = 1
            source_byte_en.append(chr(ord(i)+randomnum))
        if status == 1:
            continue
        source_byte_en = str(randomnum)+''.join(source_byte_en)
        if '<' in source_byte_en or '>' in source_byte_en or '\\' in source_byte_en or '^' in source_byte_en:
            continue
        else:
            break 
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
    #写入目标文件
    write_in = str(code_en+source_byte_en)
    target = open(file+'.encrypted','w+',encoding='utf-8')
    target.write(write_in)
    target.close()
    #删除源文件
    os.remove(file)
    print('加密完成')
elif mode == 'decrypt':
    #读取文件
    source = open(file,'r',encoding='utf-8')
    content = source.read()
    source.close()
    #加密的密钥
    numb = int(content[0])
    file_code = content[1:33]
    #获取md5
    code_md5 = []
    for i in file_code:
        code_md5.append(chr(ord(i)-numb))
    code_md5 = ''.join(code_md5)
    #验证文件密钥
    if hashlib.md5(code.encode()).hexdigest() == code_md5:
        #解密移位
        b64t = []
        for i in content[34:]:
            b64t.append(chr(ord(i)-int(content[33])))
        b64t = ''.join(b64t)
        #解密文件内容
        file_content = base64.b64decode(b64t.encode())
        #写入目标文件
        if not fpath:
            target = open(fname,'wb')
        else:
            target = open(fpath+'/'+fname,'wb')
        target.write(file_content)
        target.close()
        #删除源文件
        os.remove(file)
        print('解密完成')
    else:
        print('密码错误')