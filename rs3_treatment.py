import io
import chardet
import re
from lxml import etree

class rs3_treatment:

    def __init__(self, path):
        self.tree = etree.parse(path)

    def formatText(self, texto):
        #Retira todas as quebras de linha do texto
        new_txt = texto.replace("\n","")

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


        return aux_texto

    def change4sorted(self,numbers):
        num = []
        string = ""

        #print(numbers)

        for let in numbers:
            if let == ",":
                num.append(int(string))
                #print(string)
                string = ""
            else:
                string = string + let
    
        num.append(int(string))

        num.sort()

        ans = "["

        for i in num:
            ans = ans + str(i)
            ans = ans + ","

        ans = ans[:-1]
        ans = ans + "]"

        return ans

    def sort_signals(self):
        signals = self.tree.xpath("//signal")

        #Percorremos as tags signals, extraindo o atributo 'tokens'
        for el in signals:
            if el.attrib['tokens'] == '':
                sort_num = ''
            else:
                sort_num = self.change4sorted(el.attrib['tokens'])
            
        #Troca o valor do atributo que está na forma '1,3,2,4', pela versão ordenado, entre colchetes []
    
    def altera_segments(self):
        segments = self.tree.xpath("//segment")

        #Percorremos as tags, e formatamos o conteúdo das tags
        for el in segments:
            text = el.text
            el.text = self.formatText(text)
    
    def write_new(self,name):
        self.tree.write(name,pretty_print=True,encoding="UTF-8")