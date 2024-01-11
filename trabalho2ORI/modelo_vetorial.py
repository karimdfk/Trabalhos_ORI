from math import log10
from math import sqrt
import nltk
import sys

nltk.download("stopwords")
nltk.download("rslp")
nltk.download("mac_morpho")

print('sys.argv: ', sys.argv)

##caminho base = base1/base.txt
if len(sys.argv) < 2:
    caminhoBase = input("Digite o caminho base: ")
else:
    caminhoBase = sys.argv[1]
##caminho consulta = base1/consulta.txt
if len(sys.argv) < 3:
    caminhoConsulta = input("Digite o caminho da consulta: ")
else:
    caminhoConsulta = sys.argv[2]




with open(caminhoBase, "r") as arquivo: #abrindo o caminho base passado pelo usuário e convertendo para lista
    lista_de_caminhos = arquivo.readlines()
    
lista_limpa = []
numero_docs = 0 

for linha in lista_de_caminhos: #removendo o \n ao final de cada linha e contando o número de documentos
    lista_limpa.append(linha.strip("\n"))
    numero_docs += 1


stopwords = nltk.corpus.stopwords.words("portuguese") #definindo as stopwords em portugues


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


IDF = []

for palavra in lista_sem_repeticao:#Calculo do IDF
    aparicoes = 0
    for tupla in lista_ajuda:
        if palavra == tupla[0]:
            aparicoes+=1
    IDF.append((palavra, log10(numero_docs/aparicoes)))  


TF_lista = [] 
cont = 1

while(cont <= numero_docs):
    TF_individual = []
    for palavra in lista_sem_repeticao: #analisa todas as palavras dos documentos
        for tupla in lista_ajuda: 
            if palavra == tupla[0] and cont == tupla[1]: #Se a palavra esta presente na minha tupla e o numero do documento é igual ao cont
                TF_individual.append((palavra, (1+log10(tupla[2])))) #insere a palavra e seu TF
        
    TF_lista.append((TF_individual)) #insere o numero do documento e sua lista de TF para cada palavra
    cont+=1

TF_lista_ordenada = []  # Lista para armazenar as listas de tuplas ordenadas

for tf in TF_lista:
    tf_atualizado = []  # Lista temporária para armazenar as tuplas ordenadas
    for palavra in lista_sem_repeticao:
        encontrada = False  # Variável de controle para verificar se a palavra foi encontrada
        for tupla in tf:
            if palavra == tupla[0]:
                encontrada = True
                tf_atualizado.append(tupla)  # Adiciona a tupla encontrada
                break  # Sai do loop interno se a palavra for encontrada em alguma tupla
        if not encontrada:
            tf_atualizado.append((palavra, 0))  # Adiciona a palavra com valor 0 se não foi encontrada em nenhuma tupla
    tf_ordenado = sorted(tf_atualizado, key=lambda x: x[0])  # Ordena a lista de tuplas pelo primeiro elemento de cada tupla
    TF_lista_ordenada.append(tf_ordenado)  # Adiciona a lista ordenada à lista principal



vetor_de_pesos = []
cont=0

for vetorTF in TF_lista_ordenada:  #Estes for obtem o vetor de pesos dos documentos
    cont+=1
    pesos = [] 
    for itemTF in vetorTF: 
        for itemIDF in IDF:
            if itemTF[0] == itemIDF[0] and itemIDF[1]!=0:
                pesos.append((itemTF[0], (itemIDF[1]*itemTF[1])))
    vetor_de_pesos.append(pesos)
    
str_pesos = ''
cont = 0


for vetor in vetor_de_pesos:
    str_ajuda = "" + lista_limpa[cont]+':'
    for item in vetor:
        str_ajuda = str_ajuda + " " + item[0] + "," + str(item[1])
    str_ajuda = str_ajuda + "\n" 
    str_pesos = str_pesos + str_ajuda          
    cont+=1 


with open("pesos.txt", "w") as escrita: #cria o arquivo pesos.txt e escreve os vetores de pesos de cada arquivo
	escrita.write(str_pesos)

vetor_de_pesos = []
cont=0

for vetorTF in TF_lista_ordenada:  #Estes for obtem o vetor de pesos dos documentos
    cont+=1
    pesos = [] 
    for itemTF in vetorTF: 
        for itemIDF in IDF:
            if itemTF[0] == itemIDF[0]:
                pesos.append((itemTF[0], (itemIDF[1]*itemTF[1])))
    vetor_de_pesos.append(pesos) 
         



with open(caminhoConsulta, "r") as arquivo: #pega a consulta e guarda em variavel
    lista_consulta = arquivo.readlines()
    
consulta = ''
for linha in lista_consulta: #removendo o & de cada linha
    consulta = consulta + linha.replace("&","")
    
tokens_consulta = nltk.word_tokenize(consulta, language='portuguese' )  #separa em tokens de palavras

pesos_consluta1 = [] 
tokens_consulta2 = []

for palavra in tokens_consulta: #analisa todas as palavras da consulta
    palavra = extrator.stem(palavra.lower()) #extrai os radicais e torna tudo minusculo
    tokens_consulta2.append(palavra)
    for itemIDF in IDF:#Todos os pesos IDF
        if palavra == itemIDF[0] :
            pesos_consluta1.append((palavra, (itemIDF[1]*(1+log10(1)))))
            

pesos_consluta1 = sorted(pesos_consluta1)

cont = 0
pesos_consluta = []
for palavra in lista_sem_repeticao:
    if palavra not in tokens_consulta2:
        pesos_consluta.append((palavra, 0))
    else:
        pesos_consluta.append(pesos_consluta1[cont])
        cont+=1
  
dicionario_similaridade = {}
cont = 1

for documento in vetor_de_pesos:#Cria um dicionário com pares de pesos (peso doc, peso consulta)
    vetor_ajuda = []
    for item in documento:
        for consulta in sorted(pesos_consluta):
            if consulta[0] == item[0]:
                vetor_ajuda.append((consulta[1],item[1]))
    if vetor_ajuda != []:
        dicionario_similaridade[cont] = vetor_ajuda
    cont+=1

resposta = []   
qtd_resposta = 0

for indice, item in dicionario_similaridade.items():#Calcula similaridades
    soma = 0
    soma1 = 0
    soma2 = 0
    for peso in item:
        mult = peso[0]*peso[1]
        soma1 = soma1 + peso[0]**2
        soma2 = soma2 + peso[1]**2
        soma = soma + mult 
    dividendo = soma
    divisor = sqrt(soma1)*sqrt(soma2)
    if (dividendo/divisor) != 0:
        resposta.append((indice, (dividendo/divisor)))
        qtd_resposta+=1
  
resposta_decrescente = sorted(resposta, key=lambda x: x[1], reverse=True)
      
str_resposta = str(qtd_resposta) + "\n"

for res in resposta_decrescente:
    indice = res[0]
    cont = 0
    for doc in lista_limpa:
        cont +=1
        if cont == indice:
            str_resposta = str_resposta + doc + " " + str(res[1]) + "\n"
        
        
with open("resposta.txt", "w") as escrita: #cria o arquivo resposta.txt e escreve a resposta
	escrita.write(str_resposta)
