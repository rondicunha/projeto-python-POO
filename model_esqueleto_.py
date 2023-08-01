'''
Módulo imagem.

Contém classes para manipular
imagens georreferenciadas (com informação de GPS)

Authors: autor1
         autor2
'''

from datetime import datetime
from PIL import Image
import PIL.ImageFile
from PIL.ExifTags import TAGS, GPSTAGS
from typing import List, Tuple
import tkintermapview as tkmv

def converte_graus_para_decimais(tup: Tuple[int, int, int], ref: str) -> float:
    '''
    Função utilitária: converte coordenadas de
    graus, minutos e segundos (tupla) para
    decimais (float).
    '''

    if ref.upper() in ('N', 'E'):
        s = 1
    elif ref.upper() in ('S', 'W'):
        s = -1

    return s*(tup[0] + float(tup[1]/60) + float(tup[2]/3600))

# Utilize herança ou composição com o objeto
# retornado pelo método de classe "abre"
class Imagem():
    '''
    Representa uma imagem
    (classe principal do programa).
    '''

    def __init__(self, nome):
        '''
        Inicializa um objeto imagem
        a partir do nome do seu arquivo.
        '''
        self._img = Image.open(nome)
        #self._nome = nome.rsplit('/')[-1] # nome do arquivo da imagem
        self._nome = nome
        self._data = None # data de captura da imagem
        self._lat = None # latitude da captura da imagem
        self._lon = None # longitude da captura da imagem
        self._pais = None
        self._cidade = None
        self._processa_EXIF()

    def __repr__(self) -> str:
        '''
        Retorna representação de uma imagem
        em forma de str.
        '''
        return self._nome

    def _processa_EXIF(self) -> None:
        '''
        Processa metadados EXIF contidos no arquivo da imagem
        para extrair informações de data e local de captura.

        Atribui valores aos atributos de instância correspondentes
        à latitude, longitude e data de captura.
        '''
        tup_lat = None
        tup_lon = None
        ref_lat = None
        ref_lon = None

        for c, v in self._img._getexif().items():
            if TAGS[c] == 'GPSInfo':
                for gps_cod, gps_dado in v.items():
                    if GPSTAGS[gps_cod] == 'GPSLatitude':
                        tup_lat = gps_dado
                    if GPSTAGS[gps_cod] == 'GPSLongitude':
                        tup_lon = gps_dado
                    if GPSTAGS[gps_cod] == 'GPSLatitudeRef':
                        ref_lat = gps_dado
                    if GPSTAGS[gps_cod] == 'GPSLongitudeRef':
                        ref_lon = gps_dado

                self._lat = converte_graus_para_decimais(tup_lat, ref_lat)
                self._lon = converte_graus_para_decimais(tup_lon, ref_lon)
                self._pais = tkmv.convert_coordinates_to_country(self._lat, self._lon)
                self._cidade = tkmv.convert_coordinates_to_city(self._lat, self._lon)

            if TAGS[c] == 'DateTime':
                self._data = datetime.strptime(v, '%Y:%m:%d %H:%M:%S')

    @staticmethod
    def abre(nome: str) -> PIL.ImageFile:
        '''
        Abre imagem a partir de
        arquivo com o nome
        fornecido.
        Retorna objeto imagem
        aberto.
        '''
        imagem = Image.open(nome)
        return imagem
        
    @property
    def nome(self) -> str:
        '''
        Retorna o nome do arquivo
        da imagem.
        '''
        return self._nome

    @property
    def largura(self) -> int:
        '''
        Retorna a largura da imagem.
        '''
        return Image.width(self)

    @property
    def altura(self) -> int:
        '''
        Retorna a altura da imagem.
        '''
        return Image.height(self)

    @property
    def tamanho(self) -> Tuple[int, int]:
        '''
        Retorna o tamanho da imagem
        (tupla largura x altura).
        '''
        return Image.size(self)

    @property
    def data(self) -> datetime:
        '''
        Retorna a data em que a imagem
        foi capturada (objeto da classe datetime).
        '''
        return self._data

    @property
    def latitude(self) -> float:
        '''
        Retorna a latitude (em decimais)
        em que a imagem foi capturada
        '''
        return self._lat

    @property
    def longitude(self) -> float:
        '''
        Retorna a longitude (em decimais)
        em que a imagem foi capturada
        '''
        return self._lon

    @property
    def pais(self) -> float:
        '''
        Retorna o pais
        em que a imagem foi capturada
        '''
        return self._pais

    @property
    def cidade(self) -> float:
        '''
        Retorna a cidade
        em que a imagem foi capturada
        '''
        return self._cidade

    @property
    def img(self) -> float:
        
        return self._img

    def imprime_info(self) -> None:
        '''
        Imprime informações sobre
        a imagem.
        '''
        print(f"Nome: {self._nome}")
        print(f"Data: {self._data}")
        print(f"Latitude: {self._lat}")
        print(f"Longitude: {self._lon}")
        print(f"Cidade: {self._cidade}")
        print(f"Pais: {self._pais}")

    def redimensiona(self, nv_lar: float, nv_alt: float) -> None:
        '''
        Altera as dimensões do objeto imagem para
        que ele possua novo tamanho dado por
        nv_lar x nv_alt.
        '''
        Image.resize(size=(nv_lar, nv_alt))

class BDImagens:
    '''
    Representa um banco de dados de
    imagens geoespaciais
    (classe de busca do programa).
    '''

    def __init__(self, idx):
        self.bd = idx
        self.listBD: List[Imagem] = []

    def processa(self) -> None:
        '''
        Abre cada imagem no arquivo de índice
        e adiciona cada imagem à lista.
        '''
        with open(self.bd) as arq:
            for linha in arq:
                nome_arquivo = linha.rstrip()
                imagem_jpeg = Imagem(nome_arquivo)
                imagem_jpeg.abre(nome_arquivo)
                self.listBD.append(imagem_jpeg)

    @property
    def tamanho(self) -> int:
        '''
        Retorna a quantidade de imagem
        no banco de dados.
        '''

        return len(self.listBD)

    def todas(self) -> List[Imagem]:
        '''
        Retorna uma lista contendo
        todas as imagens abertas
        no banco de dados.
        '''

        return self.listBD

    def busca_por_nome(self, texto: str) -> List[Imagem]:
        '''
        Retorna uma lista contendo
        todas as imagens do banco de dados
        cujo nome contenha o texto passado
        como parâmetro.
        '''

        encontrados = []
        for s in self.listBD:
            if texto in s.nome:
                encontrados.append(s)
        return encontrados

    def busca_por_data(self, dini: datetime, dfim: datetime) -> List[Imagem]:
        '''
        Retorna uma lista contendo
        todas as imagens do banco de dados
        cuja data de captura encontra-se entre
        dini (data inicial) e dfim (data final).
        '''
        encontrados = []
        for s in self.listBD:
            if (dini <= s.data <= dfim):
                encontrados.append(s)
        return encontrados

    def busca_por_pais(self, texto:str) -> List[Imagem]:
        '''
        Retorna uma lista contendo
        todas as imagens do banco de dados
        cujo país seja passado como parametro.
        '''
        encontrados = []
        for s in self.listBD:
            if texto in str(s.pais):
                encontrados.append(s)
        return encontrados
    
    def busca_por_cidade(self, texto:str) -> List[Imagem]:
        '''
        Retorna uma lista contendo
        todas as imagens do banco de dados
        cuja cidade seja passado como parametro.
        '''
        encontrados = []
        for s in self.listBD:
            if texto in str(s.cidade):
                encontrados.append(s)
        return encontrados

    def busca_por_filtros(self, start_date, end_date, name, city, country):
        encontrados = []

        # Converta as datas para objetos datetime
        dini = datetime.strptime(start_date, "%Y-%m-%d")
        dfim = datetime.strptime(end_date, "%Y-%m-%d")

        # Realize a busca por nome, data, cidade e país
        for imagem in self.listBD:
            if name.lower() in imagem.nome.lower() and \
               dini <= imagem.data <= dfim and \
               city.lower() in imagem.cidade.lower() and \
               country.lower() in imagem.pais.lower():
                encontrados.append(imagem)

        return encontrados

def main():

    bd = BDImagens('dataset1/index')
    bd.processa()

    # Mostra as informações de todas as imagens do banco de dados
    print('Imagens do Banco de Dados:')
    for img in bd.todas():
        img.imprime_info()

    print("===========================================")

    # Mostra os nomes das imagens que possuam texto no seu nome
    texto = 'Porto'
    for img in bd.busca_por_cidade(texto):
        print(img.cidade)

    print("===========================================")

    # Mostra as datas das imagens capturadas entre d1 e d2
    d1 = datetime(2021, 1, 1)
    d2 = datetime(2023, 1, 1)
    for img in bd.busca_por_pais("United States"):
        print(img.pais)

if __name__ == '__main__':
    main()