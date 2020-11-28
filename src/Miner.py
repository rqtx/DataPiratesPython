import requests
from bs4 import BeautifulSoup
import json
import os.path
import hashlib

class Miner:
    __PAYLOAD = "UF={uf}&qtdrow={qtdrow}&pagini={pagini}&pagfim={pagfim}"
    __URL = "http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm"
    __HEADERS = {
        'Content-Type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache"
        }
    
    def __init__(self, uf, datafolder=""):
        self.uf = uf
        self.dataFolder = datafolder       
        if self.dataFolder:
            if not os.path.exists(self.dataFolder):  
                os.makedirs(self.dataFolder)
    
    def __coreMiner(self, htmlText):
        data = []
        soup = BeautifulSoup(htmlText, 'html.parser')
        tables = soup.find_all('table', class_='tmptabela')
        if not tables:
            return []

        if len(tables) > 1:
            citys = tables[1].find_all('tr')
        else:
            citys = tables[0].find_all('tr')
        
        for line in citys[2:]:
            record = line.find_all('td')
            data.append(self.__createDictionary(record[0].get_text(), record[1].get_text()))
        return data
    
    def __dumpJsonl(self, data, output_path, append=False):
        """
        Write list of objects to a JSON lines file.
        """
        mode = 'a+' if append else 'w'
        with open(output_path, mode, encoding='utf-8') as f:
            for line in data:
                json_record = json.dumps(line, ensure_ascii=False)
                f.write(json_record + '\n')
        print('Wrote {} records to {}'.format(len(data), output_path))

    def __createDictionary(self, localidade, fcep):
        id = hashlib.md5(bytes(localidade + fcep, encoding='utf-8')).hexdigest()
        return {"id": id, "localidade": localidade, "faixa de cep": fcep}

    def __requestPage(self, method, url, payload, headers):
        return requests.request(method, url, data=payload, headers=headers)

    def remove_dupe_dicts(self, l):
        list_of_strings = [
            json.dumps(d, sort_keys=True)
            for d in l
        ]
        list_of_strings = set(list_of_strings)
        return [
            json.loads(s)
            for s in list_of_strings
        ]

    def mine(self):
        qtdrow = pagfim =100
        pagini = 1
        data = []

        while True:
            response = self.__requestPage("POST", self.__URL, self.__PAYLOAD.format(uf=self.uf, qtdrow=qtdrow, pagini=pagini, pagfim=pagfim), self.__HEADERS)
            result = self.__coreMiner(response.text)
            if not result:
                data = self.remove_dupe_dicts(data)
                self.__dumpJsonl(data, os.path.join(self.dataFolder, self.uf + ".jsonl"))
                break
            data += result
            pagini += qtdrow
            pagfim += qtdrow