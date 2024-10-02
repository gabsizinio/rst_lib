import io
import chardet
import re

class Tokenization:

    def __init__(self, text):
        #Retira todas as quebras de linha do texto
        new_txt = text.replace("\n","")

        #Colocamos nesse array todos os sinais de pontuação que queremos segmentar do texto
        pont = [",",".","“","”","'",'"','[',']','(',')',']','[','{','}','!','?','--','...','``','``',':',';']

        new_pont = []

        #Para cada um dos sinais, colocamos em "new_pont" a string com ele e um espaço de cada lado, então "!" vira " ! "
        for p in pont:
            new_p = " " + p + " "
            new_pont.append(new_p)


        for i in range(len(new_pont)):
            new_txt = new_txt.replace(pont[i],new_pont[i])

        #Retira o traverssão, sem afetar palavras com hífen
        aux_texto = ""

        for i in range(len(new_txt)):
            if i == 0:
                if new_txt[i] == "-":
                    aux_texto = aux_texto + "-"
                    aux_texto = aux_texto + " "
                else:
                    aux_texto = aux_texto + new_txt[i]
            elif i == len(new_txt) - 1:
                if new_txt[i] == "-":
                    aux_texto = aux_texto + " "
                    aux_texto = aux_texto + "-"
                else:
                    aux_texto = aux_texto + new_txt[i]
            else:
                if new_txt[i] == "-" and new_txt[i-1]!=" " and new_txt[i+1]==" ":
                    aux_texto = aux_texto + " "
                    aux_texto = aux_texto + "-"
                else:
                    aux_texto = aux_texto + new_txt[i]
        
        self.text = aux_texto
    
    def tokens(self):
        #aplicamos o split ao texto
        tokens = self.text.split(" ")
        #com isso o vetor tokens terá todas palavras, sinais e textos

        #Por fim, tiramos todos os tokens '' e ' '
        tokens=[j for i,j in enumerate(tokens) if j!='']
        tokens=[j for i,j in enumerate(tokens) if j!=' ']

        return tokens
    
    def indexes_dict(self):
        #Crimaos um índice para cada um dos tokens, com base na ordem deles
        indexes = {}
        ind = 1
        token = self.tokens()

        for ele in token:
            indexes[ind] = ele
            ind+=1
        
        return indexes
