def opis():
    cykl = open('Dane/Opisy.txt', mode='r', encoding='utf8', newline='\r\n')
    return cykl


def nowy_opis(wiadomosc=None):
    return "Warhammer"


def DataSystemuWatkuWyswietl(plik):
    """
    funkcja przyjmuje jako parametr nazwę pliku do otwarcia
    w folderze "dane" i ją wypisuje w formacie int
    :param plik:
    :return:
    """
    with open(f'Dane/{plik}.txt', "r") as data_z_archiwum:
        data_nowa = data_z_archiwum.readline()
        return data_nowa


def DataSystemuWatkuNadpisz(plik, data):
    """
    funkcja przyjmuje jako parametr nazwę pliku do
    nadpisania w folderze "dane" oraz datę w formacie
    int i ją zapisuje wewnątrz wskazanego pliku
    :param plik:
    :param data:
    :return:
    """
    if data is not None:
        with open(f'Dane/{plik}.txt', "w") as data_z_archiwum:
            data_z_archiwum.write(data)
