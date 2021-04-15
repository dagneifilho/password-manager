import cryptography.fernet
import string
import random
import time
import hashlib
k=b'wFrKDCor9KYB7Xvk9l0-he_HmcO1yPye_LVSyVpYj-I='

def encrypt(password):
    f=cryptography.fernet.Fernet(k)
    password=bytes(password,'utf-8')
    token=f.encrypt(password)
    token=str(token)
    return token

def decrypt(token):
    f=cryptography.fernet.Fernet(k)
    token=token[2:len(token)-1]
    token=bytes(token,'utf-8')
    password=str(f.decrypt(token))
    password=password[2:len(password)-1]
    return password

def mkpassword(n):

    chars=string.ascii_letters+string.digits+'@#&*%!'
    password=str()
    for c in range (0,n):
        password+=random.choice(chars)
    return password

def store_pass(servico,hash):

    arquivo=open('database.txt','a')
    escrever= [servico,',',hash+' ']
    arquivo.writelines(escrever)
    arquivo.close()

def find_pass(servico):
    arquivo=open('database.txt','r')
    lista_dados=[]
    for linha in arquivo:
        linha=linha.split(' ')
        for comb in linha:
            comb=comb.split(',')
            lista_dados.append(comb)

    del(lista_dados[len(lista_dados)-1])
    dicionario=dict(lista_dados)

    hash=dicionario[servico]
    return hash
    arquivo.close()

def verify_pass():

    arquivo=open('database.txt','r')
    servicos=[]
    for linha in arquivo:
        linha = linha.split(' ')
        for comb in linha :
            comb=comb.split(',')
            s=comb[0]
            servicos.append(s)
    return servicos
    arquivo.close()
def change_pass(servico,hash):
    arquivo=open('database.txt','r')
    servicos=[]
    hashs=[]
    for linha in arquivo:
        linha = linha.split(' ')
        del(linha[len(linha)-1])

        for comb in linha :
            comb=comb.split(',')
            s=comb[0]
            hs=comb[1]
            servicos.append(s)
            hashs.append(hs)
    arquivo.close()
    arquivo=open('database.txt','w')
    i=0
    for s in servicos:
        if s==servico:
            escrever=[s+','+hash+' ']
        else:
            escrever=[s+','+hashs[i]+' ']
        i+=1
        arquivo.writelines(escrever)
    arquivo.close()
senhaprog='067fc9c8d8d15b80ca775a1d9433cb48'

senha=input('Digite a senha: ')
crypt=hashlib.md5()
crypt.update(bytes(senha,'utf-8'))
senha=crypt.hexdigest()
while senha!=senhaprog:
    senha=input('Digite sua senha: ')
while True:
    acao=input('O que você desja fazer?'
               '\nPara procurar uma senha, digite "p"'
               '\nPara adicionar uma senha, digite "a"'
               '\nPara ver senhas salvas, digite "s"'
               '\nPara alterar alguma senha, digite "c"'
               '\nPara fechar, digite "f"')
    if acao=='f':
        print('Finalizado!')
        break
    if acao=='p':
        token=find_pass(input('Voce precisa a senha de qual servico? '))
        password=decrypt(token)
        print('---------------------------')
        print(f'A senha que voce buscou é:')
        print(password)
        print('---------------------------')
        time.sleep(3)
    if acao=='s':
        servicos=verify_pass()
        print('---------------------------')
        print('Você tem as seguintes senhas salvas: ')
        for servico in servicos:
            print(servico)
        print('---------------------------')
        time.sleep(3)
    if acao=='a':
        senha2=mkpassword(int(input('Você quer a sua senha com quantos caracteres? ')))
        token=encrypt(senha2)
        servico = input('Onde essa senha será usada? ')
        servicos=verify_pass()
        if servico in servicos:
            print('Uma senha já foi cadastrada para este servico')
            confirm=input('Deseja ver a senha cadastrada? (s/n) ')
            if confirm =='s':
                token=find_pass(servico)
                password=(decrypt(token))
                print('---------------------------')
                print(f'A senha que voce buscou é:')
                print(password)
                print('---------------------------')

        else:
            print('---------------------------')
            print(f'A senha gerada foi: {senha2}')
            store_pass(servico,token)
            print('Operação realizada com sucesso! ')
            print('---------------------------')
        time.sleep(3)
    if acao=='c':
        print('AO ALTERAR UMA SENHA, É IMPOSSÍVEL RECUPERAR A SENHA ANTIGA!')
        conf=input('DESEJA CONTINUAR? (s/n)')
        if conf =='s':
            conf=input('Para fazer a alteração, digite "alterar": ')
            if conf== 'alterar':
                senhanova=mkpassword(int(input('Quantos caracteres você quer na sua senha nova? ')))
                novotoken=encrypt(senhanova)
                change_pass(input('Você deseja alterar a senha de qual serviço?'),novotoken)
                print('Senha alterada com sucesso!')
                time.sleep(0.8)
                print('---------------------------')
                print(f'Sua nova senha é: {senhanova}')
                print('---------------------------')
                time.sleep(3)


