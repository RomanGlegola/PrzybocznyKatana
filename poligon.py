import feedparser
from bs4 import BeautifulSoup
import requests


def forumKrysztalyCzasuWatki():
    return (
        'https://krysztalyczasu.pl/forum/viewforum.php?f=146',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=145',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=142',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=141',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=140',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=139',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=133',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=132',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=130',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=128',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=127',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=126',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=125',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=124',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=123',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=122',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=121',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=120',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=118',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=117',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=116',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=115',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=114',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=113',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=112',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=110',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=109',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=104',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=83',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=87',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=42',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=31',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=22')


def forumKrysztalyCzasuPbf():
    return (
        'https://krysztalyczasu.pl/forum/viewforum.php?f=107',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=134',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=106',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=135',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=136',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=137',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=138')


def facebookWatki():
    return ('krysztalyczasupl')


def daneForum(dane):
    """
    funkcja wydobywa autora wątku, nazwę wątku, adres
    www wątku, datę publikacji wątku oraz surową datę do
    oznaczenia ostatniego opublikowanego wątku na kanale
    """

    autor_watku = dane.findAll(("a", "span"), class_=
    ["username", "username-coloured"])[0] \
        .text \
        .strip()
    nazwa_watku = dane.find("a", class_="topictitle") \
        .getText()
    adres_watku = dane.find("a", class_="topictitle") \
                      .attrs["href"][1:].split('&sid=')
    data_watku = dane.select("div", class_="username")[2] \
        .text \
        .strip() \
        .split(' » ')
    data_do_soli = ' , ' + ''.join(data_watku[1])
    sol_daty = data_surowa(data_do_soli.split(', '))
    data_czytelna = data_przerobiona(sol_daty)
    return (autor_watku, nazwa_watku, f'https://krysztalyczasu.pl/forum{adres_watku[0]}',
           data_czytelna, sol_daty)

def data_przerobiona(dane):
    rok = dane[0:4]
    miesiac = dane[4:6]
    dzien = dane[6:8]
    godzina = dane[8:10]
    minuta = dane[10:12]

    cyfra_z_zerem = ['00', '01', '02', '03', '04',
                     '05', '06', '07', '08', '09',
                     '10', '11', '12']
    cyfra_bez_zera = ['0', '1', '2', '3', '4',
                      '5', '6', '7', '8', '9']

    for x in range(10):
        if godzina == cyfra_z_zerem[x]:
            godzina = godzina.replace(cyfra_z_zerem[x], cyfra_bez_zera[x])

    for x in range(10):
        if dzien == cyfra_z_zerem[x]:
            dzien = dzien.replace(cyfra_z_zerem[x], cyfra_bez_zera[x])

    miesiac_czytelny = ['', 'stycznia', 'lutego', 'marca',
                        'kwietnia', 'maja', 'czerwca',
                        'lipca', 'sierpnia', 'września',
                        'października', 'listopada', 'grudnia']

    for x in range(len(miesiac_czytelny)):
        if miesiac == cyfra_z_zerem[x]:
            miesiac = miesiac.replace(cyfra_z_zerem[x], miesiac_czytelny[x])
    return f"{dzien} {miesiac} {rok}", f"{godzina}:{minuta}"


def data_surowa(dane):
    """
    funkcja wydobywa z daty do funkcji surowe
    cyfry celem późniejszej obróbki wiadomości
    :param dane:
    :return:
    """
    miesiace_stare = [
        ['stycznia', 'lutego', 'marca',
         'kwietnia', 'maja', 'czerwca',
         'lipca', 'sierpnia', 'września',
         'października', 'listopada', 'grudnia'],
        ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']]
    miesiace_nowe = [
        '01', '02', '03', '04', '05', '06',
        '07', '08', '09', '10', '11', '12']
    for x in range(len(miesiace_nowe)):
        for i in range(len(miesiace_stare)):
            dane = [item.replace(miesiace_stare[i][x], miesiace_nowe[x]) for item in dane]
    lista = [int(x) for x in
             dane[1].split()[::-1] +
             dane[2].split(':')]
    return "".join(map(lambda x: "%02d" % x, lista[:6]))


def zupaForum(dane):
    """
    funkcja pobiera kod strony internetowej. Następnie
    wydobywa z działu na forum posty celem sprawdzenia
    które z nich są najstarsze i przekazuje dalej.
    :param dane:
    :return:
    """
    strona = requests \
        .get(dane) \
        .text
    for watek in BeautifulSoup(strona, 'lxml').findAll(class_=
                                                       ['row-item sticky_read_locked',
                                                        'row-item topic_read',
                                                        'row-item topic_read_hot',
                                                        'row-item topic_read_mine',
                                                        'row-item topic_unread',
                                                        'row-item topic_unread_mine']):
        yield watek


def zrzutForum(dane):
    """
    funkcja zrzuca wszystkie wydobyte dane z Forum w formie listy i je drukuje.
    :return:
    """
    return tuple([daneForum(x) for x in (zupaForum(i))] for i in dane)


def tekstPBF(dane=forumKrysztalyCzasuPbf()):
    from OperacjeNaPlikach import DataSystemuWatkuWyswietl, DataSystemuWatkuNadpisz
    data_archiwum = DataSystemuWatkuWyswietl('forumKrysztalyCzasuPbfData')
    data_temp = data_archiwum
    for strona in zrzutForum(dane):
        for watek in strona:
            if data_archiwum < watek[4]:
                if data_temp < watek[4]:
                    data_temp = watek[4]
                yield (f'Ogłaszam uroczyście, że {watek[3][0]} o godzinie {watek[3][1]} '
                       f'na forum pojawił się scenariusz PGF do rozegrania! "{watek[1]}". '
                       f'Autorstwa "{watek[0]}". Rozgrywkę można znaleźć pod adresem: {watek[2]}\n')
    DataSystemuWatkuNadpisz('forumKrysztalyCzasuPbfData', data_temp)


def tekstForum(dane=forumKrysztalyCzasuWatki()):
    from OperacjeNaPlikach import DataSystemuWatkuWyswietl, DataSystemuWatkuNadpisz
    data_archiwum = DataSystemuWatkuWyswietl('forumKrysztalyCzasuWatkiData')
    data_temp = data_archiwum
    for strona in zrzutForum(dane):
        for watek in strona:
            if data_archiwum < watek[4]:
                if data_temp < watek[4]:
                    data_temp = watek[4]
                yield (f'Ogłaszam uroczyście, że dnia {watek[3][0]} o godzinie {watek[3][1]} '
                       f'na forum pojawił się wątek! "{watek[1]}". '
                       f'Autorstwa "{watek[0]}". Pełną wiadomość można poznać pod adresem: {watek[2]} ')
    DataSystemuWatkuNadpisz('forumKrysztalyCzasuWatkiData', data_temp)


print(*tekstPBF(forumKrysztalyCzasuPbf()))
print(*tekstForum(forumKrysztalyCzasuWatki()))
# print(*tekstRSS(kanalRssKrysztalyCzasu()))
# print(*zupaForum('https://krysztalyczasu.pl/forum/viewforum.php?f=107'))
# print(*tekstPBF(forumKrysztalyCzasuPbf()))