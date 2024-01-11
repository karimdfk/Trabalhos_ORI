from math import log10
from math import sqrt
import nltk
import sys

nltk.download("rslp")
nltk.download("mac_morpho")

print('sys.argv: ', sys.argv)

##caminho base = entrada.txt
if len(sys.argv) < 2:
    caminhoBase = input("Digite o caminho base: ")
else:
    caminhoBase = sys.argv[1]
    

with open(caminhoBase, "r") as arquivo: #abrindo o caminho base passado pelo usuário e convertendo para lista
    lista_de_caminhos = arquivo.readlines()
    
lista_limpa = []

for linha in lista_de_caminhos: #removendo o \n ao final de cada linha
    lista_limpa.append(linha.strip("\n"))

qtd_consultas = int(lista_limpa[0])
i=0
lista_resp_ideais = []
lista_resp_sistema = []

for item in lista_limpa: #separa as respostas ideais e as respostas do sistema em 2 listas
    if i > 0 and i<=qtd_consultas:
        lista_resp_ideais.append(nltk.word_tokenize(item, language='portuguese'))
    if i > qtd_consultas:
        lista_resp_sistema.append(nltk.word_tokenize(item, language='portuguese'))
    i+=1 

i=0
precisao = []
revocacao = []
while(i < qtd_consultas): #obtendo as precisoes e revocacoes dos conjuntos de respostas
    cont = 0
    qtd_iguais = 0
    precisao_individual = []
    revocacao_individual = []
    for item_sistema in lista_resp_sistema[i]:
        cont+=1
        for item_ideal in lista_resp_ideais[i]:
            if item_sistema == item_ideal:
                qtd_iguais+=1
                precisao_individual.append((qtd_iguais/cont))
                revocacao_individual.append((qtd_iguais/len(lista_resp_ideais[i])))
    precisao.append(precisao_individual)
    revocacao.append(revocacao_individual)
    i+=1
 
i=0
while(i < qtd_consultas):
    x=0
    for item_precisao in precisao[i]: 
        aux=0
        for j in range(len(precisao[i])): 
            aux = precisao[i][j]
            if item_precisao <= aux and j>x:
                del precisao[i][x]
                del revocacao[i][x]   
                break       
        x+=1
    i+=1

i=0
resposta = []
resposta_formatada = []
resposta_final = ''
while(i < qtd_consultas):
    item_precisao = precisao[i]
    item_revocacao = revocacao[i]
    n=0
    lista_resposta = []
    lista_resposta_formatada = []
    str_resposta = ''
    j=0
    while j < 11:
        if n < len(item_revocacao) and (j/10)<=item_revocacao[n]:
            lista_resposta.append(item_precisao[n])
            lista_resposta_formatada.append(item_precisao[n]*100)
            str_resposta = str_resposta + str(item_precisao[n]) + ' '
        else:
            if n<len(item_revocacao) -1:
                n+=1
                j-=1
            else:
                lista_resposta.append(0)
                lista_resposta_formatada.append(0)
                str_resposta = str_resposta + '0 ' 
        j+=1
    i+=1
    resposta.append(lista_resposta)
    resposta_formatada.append(lista_resposta_formatada)
    resposta_final = resposta_final + str_resposta + '\n'

soma = []
i=0
for lista in resposta:
    j=0
    for item in lista:
        if i==0:
            soma.append(item)
        else:
            soma[j] = soma[j] + item
            j+=1
    i+=1

media = ''
lista_media = []
for item in soma:
    media = media + str(round(item/qtd_consultas, 2)) + ' '
    lista_media.append((item/qtd_consultas*100))
   
        
with open("media.txt", "w") as escrita: #cria o arquivo media.txt e escreve a resposta
	escrita.write(media)
 
import matplotlib.pyplot as plt

x = [0,10,20,30,40,50,60,70,80,90,100]
ymedia = lista_media

for item in resposta_formatada:
    plt.plot(x, item, '-o')  # a opção '-o' é para colocar um círculo sobre os pontos e liga-los por segmentos de reta
    plt.show()


plt.plot(x, ymedia, '-o')  # a opção '-o' é para colocar um círculo sobre os pontos e liga-los por segmentos de reta
plt.show()
