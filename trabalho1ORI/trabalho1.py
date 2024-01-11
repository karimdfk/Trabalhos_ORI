import nltk

nltk.download("stopwords")
nltk.download("rslp")
nltk.download("mac_morpho")

##caminho base = base_samba/base.txt
caminhoBase = input("Digite o caminho base: ")
##caminho consulta = base_samba/consulta.txt
caminhoConsulta = input("Digite o caminho da consulta: ")


with open(caminhoBase, "r") as arquivo: #abrindo o caminho base passado pelo usuário e convertendo para lista
    lista_de_caminhos = arquivo.readlines()
    
lista_limpa = []

for linha in lista_de_caminhos: #removendo o \n ao final de cada linha
    lista_limpa.append(linha.strip("\n"))


stopwords = nltk.corpus.stopwords.words("portuguese") #definindo as stopwords em portugues
#adicionando algumas stopwords não presentes na função stopwords.words
stopwords.append('daqui')
stopwords.append('embora')
stopwords.append('porque')
stopwords.append('enquanto')
stopwords.append('pois')
stopwords.append('pra')
stopwords.append('sobre')



#definindo variaveis auxiliares
palavras_importantes = []
lista_ajuda = []
i = 1
j=0

extrator = nltk.stem.RSLPStemmer() #gerando extrator de radicais

for item in lista_limpa:
    with open(item, "r") as textos:
        conteudo_samba = ''.join(textos.readlines()) #pega o conteúdo de cada arquivo e o transforma em string
        tokens_texto = nltk.word_tokenize(conteudo_samba, language='portuguese' )  #separa em tokens de palavras
        n = 1
        palavra_aux = None
        palavras_importantes2 = []
        
        for palavra in sorted(tokens_texto):
            if palavra not in stopwords: #remove stopwords
                palavra = extrator.stem(palavra.lower()) #extrai os radicais e torna tudo minusculo
                if palavra.isalnum():#remove caracteres não alfabeticos ou numericos
                    palavras_importantes.append(palavra)
                    palavras_importantes2.append(palavra)
                
        
        for palavra in sorted(palavras_importantes2):
            if palavra != palavra_aux:
                n = 1
                lista_ajuda.append((palavra, i, n))#salva cada palavra com o documento ao qual ela pertence e suas aparicoes
                palavra_aux = palavra
                j += 1   
            else:
                n += 1
                lista_ajuda[j-1] = (palavra, i, n)#usado quando uma palavra é repitida        
    i+=1

lista_sem_repeticao = sorted(list(set(palavras_importantes)))#cria uma lista com todas as palavras de todos os textos sem repetição

indice_invertido = '' 
indice_invertido_lista = [] 

for item in lista_sem_repeticao: #analisa todas as palavras dos documentos
    frase = ''
    
    for tupla in lista_ajuda: 
        if item == tupla[0]: #Se a palavra esta presente na minha tupla, adiciona o numero do documento e quantas vezes aparece
            parte = str(tupla[1]) + ',' + str(tupla[2]) + ' '
            frase += parte        
    
    #formatações da string para o formato solicitado
    linha_indice_invertido = item + ': ' + frase
    indice_invertido += linha_indice_invertido + "\n"
    indice_invertido_lista.append(linha_indice_invertido)
    

with open("indice.txt", "w") as escrita: #cria o arquivo indice.txt e escreve o indice invertido
	escrita.write(str(indice_invertido))
        

with open(caminhoConsulta, "r") as arquivo: #pega a consulta e guarda em variavel
    consulta = ''.join(arquivo.readline())
    
tokens_consulta = nltk.word_tokenize(consulta, language='portuguese' )  #separa em tokens de palavras

lista_consulta = []
tem_not = False
lista_operadores = []
j = 0

for parte in tokens_consulta:#Este for tem como finalidade retornar as palavras da consulta, com 1 caso não estejam acompanhados de not e 0 caso contrário
    parte = extrator.stem(parte.lower())
    
    if parte.isalpha():
        lista_consulta.append((parte, 1))
        j+=1
        if tem_not:
            lista_consulta[j-1] = (parte, 0)
            tem_not = False
    elif parte == "!":
        tem_not = not(tem_not)
    elif parte =="&" or "|": #Guarda os operadores em ordem para uso posterior
        lista_operadores.append(parte)
        

lista_de_respostas = []

n=0
for parte in lista_consulta:#analisa as tuplas (nome, T ou F)
    n+=1
    x=0
    ultimo = 1
    lista_aux = []
    lista_aux_sem_repeticao = []
    for item in lista_ajuda: #Percorre todos as tuplas (nome, documento em que aparece, numero de aparições)
        if parte[0] == item[0] and parte[1] == 1: #Caso em que a consulta solicita um True para o termo e ele aparece no documento
            lista_aux.append((parte[0], item[1]))
            x=1
        if parte[0] == item[0] and parte[1] == 0: #Controle caso a consulta solicite falso mas o termo apareça no documento
            x=1 
        if parte[0] != item[0] and x == 0 and item[1] != ultimo and parte[1] == 0: #Caso em que a consulta solicita False e o termo não aparece no documento
            lista_aux.append((parte[0], ultimo)) 
        if item[1] != ultimo: #Controle de mudança de documento
            x = 0
            
        ultimo = item[1]
    
    repete = None
    
    for res in lista_aux: #removendo repetições na resposta de cada documento
        if res[1] != repete:
            lista_aux_sem_repeticao.append(res)
            repete = res[1]
            
               
    lista_de_respostas.append(lista_aux_sem_repeticao) #Juntando respostas de cada documento

n=0
i=0
resposta = []
for i in range(len(lista_de_respostas)):
    if i == 0:
        for res in lista_de_respostas[i]:
            resposta.append(res[1])
    elif i != 0:
        if lista_operadores[n] == '&':
            aux = resposta
            resposta = []
            for res in aux:
                for res2 in lista_de_respostas[i]:
                    if res == res2[1]:
                        resposta.append(res)
            n+=1
        elif lista_operadores[n] == '|':
            for res in resposta:
                for res2 in lista_de_respostas[i]:
                    if res != res2[1]:
                        resposta.append(res2[1])
            n+=1
            resposta = sorted(resposta)
    i+=1

i=1
lista_nomes = []
for nome in lista_limpa:
    for numero in resposta:
        if numero == i:
            lista_nomes.append(nome)
    i+=1
  
            
string_resposta = str(len(resposta)) 
for nome in lista_nomes:
    string_resposta = string_resposta + '\n' + str(nome)
 
        
with open("resposta.txt", "w") as escrita: #cria o arquivo indice.txt e escreve o indice invertido
	escrita.write(string_resposta)


print(stopwords)