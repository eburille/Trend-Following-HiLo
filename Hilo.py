import csv

#def_status returns the new status of the strategy
def def_status(media_hi, media_lo, cotacao, status):
    if status == '' and cotacao > media_hi:
        return 'compra'
    elif status == '' and cotacao < media_lo:
        return 'venda'

    elif status == 'compra' and cotacao < media_lo:
        return 'venda'
    elif status == 'venda' and cotacao > media_hi:
        return 'compra'
    else: return status

#def_entrada returns the value of the stock in the first operation
def def_entrada(cotacao, status, check_status, entrada):
    if status != '' and check_status == '':
        return cotacao
    else: return entrada

#multiplic is used to control the rentability of an operation
def multiplic(entrada, saida, status):
    if status == 'compra':
        rentab = (saida-entrada)/entrada
        return (rentab + 1)
    elif status == 'venda':
        rentab = (-(saida - entrada)) / entrada
        return (rentab + 1)

#This class is used to save the returns of the strategy
class Retorno():
    multplic = 0
    patrimonio = 1

    def atual(self):
        self.patrimonio = self.patrimonio * self.multplic

    def __init__(self, periodo):
        self.periodo = periodo
        pass

#This Class is used to control de Hi-Lo indicator 
class HiLo():
    cotacoes_hi = []
    cotacoes_lo = []

    #These functions are used to update the average of the prices of the stock
    def atual(self):
        def media(cotacoes):
            soma = 0
            for cotacao in cotacoes:
                soma += cotacao       
            try: media = soma / len(cotacoes)
            except: media = 0   
            return media
        
        #hilo averages
        self.media_hi = media(self.cotacoes_hi)
        self.media_lo = media(self.cotacoes_lo)

#The main function, where the magic happens
def main(periodo):
    retorno = Retorno(periodo)
    hilo = HiLo()

    #Check_status is important to know if the status change
    check_status = '' 
    status = ''

    entrada = 0

    with open('USIM5.SA.csv') as ativo:
        read = csv.DictReader(ativo)

        for row in read:
            #The first IF serve to complete the lists of HiLo
            if periodo > len(hilo.cotacoes_hi):
                hilo.cotacoes_hi.append(float(row['High']))
                hilo.cotacoes_lo.append(float(row['Low']))
            else:
                #This statement update the hilo.averages [58]
                hilo.atual()

                #update the status and check status to compare them boths if their're == or !=
                check_status = status
                status = def_status(hilo.media_hi, hilo.media_lo, float(row['Close']), status)

                #Gives to entrada the value of the stock when the strategy starts 
                entrada = def_entrada(float(row['Close']), status, check_status, entrada)

                #Check when the status change to complete an operation 
                if check_status != '' and check_status != status:
                    
                    saida = float(row['Close'])
                    retorno.multplic = multiplic(entrada, saida, check_status)
                    #This statement updates the retorno.patrimonio
                    retorno.atual()
            
                    entrada = saida

                #Update the hilo lists [45]
                hilo.cotacoes_hi.pop(0)
                hilo.cotacoes_lo.pop(0)
                hilo.cotacoes_hi.append(float(row['High']))
                hilo.cotacoes_lo.append(float(row['Low']))

    return retorno

#Code to find the best configuration of Hi-Lo for the stock
max = 0
p = 0
for num in range(1, 100):
    a = main(num)
    if a.patrimonio > max:
        max = a.patrimonio
        p = num

print(p, max)