import feedparser
from bs4 import BeautifulSoup
import requests


def forumKrysztalyCzasuWatki():
    return (
        'https://krysztalyczasu.pl/forum/viewforum.php?f=146', 'https://krysztalyczasu.pl/forum/viewforum.php?f=145',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=142', 'https://krysztalyczasu.pl/forum/viewforum.php?f=141',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=140', 'https://krysztalyczasu.pl/forum/viewforum.php?f=139',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=133', 'https://krysztalyczasu.pl/forum/viewforum.php?f=132',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=130', 'https://krysztalyczasu.pl/forum/viewforum.php?f=128',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=127', 'https://krysztalyczasu.pl/forum/viewforum.php?f=126',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=125', 'https://krysztalyczasu.pl/forum/viewforum.php?f=124',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=123', 'https://krysztalyczasu.pl/forum/viewforum.php?f=122',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=121', 'https://krysztalyczasu.pl/forum/viewforum.php?f=120',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=118', 'https://krysztalyczasu.pl/forum/viewforum.php?f=117',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=116', 'https://krysztalyczasu.pl/forum/viewforum.php?f=115',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=114', 'https://krysztalyczasu.pl/forum/viewforum.php?f=113',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=112', 'https://krysztalyczasu.pl/forum/viewforum.php?f=110',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=109', 'https://krysztalyczasu.pl/forum/viewforum.php?f=104',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=83', 'https://krysztalyczasu.pl/forum/viewforum.php?f=87',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=42', 'https://krysztalyczasu.pl/forum/viewforum.php?f=31',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=22')


def forumKrysztalyCzasuPbf():
    return (
        'https://krysztalyczasu.pl/forum/viewforum.php?f=107', 'https://krysztalyczasu.pl/forum/viewforum.php?f=134',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=106', 'https://krysztalyczasu.pl/forum/viewforum.php?f=135',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=136', 'https://krysztalyczasu.pl/forum/viewforum.php?f=137',
        'https://krysztalyczasu.pl/forum/viewforum.php?f=138')


def kanalRssKrysztalyCzasu():
    return ('https://krysztalyczasu.pl/feed/')


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


def daneStrony(dane):
    """
    funkcja wydobywa autora artykułu, nazwę artykułu, adres
    www artykułu, datę publikacji artykułu oraz surową datę do
    oznaczenia ostatniego opublikowanego artykułu na kanale
    :param dane:
    :return:
    """
    author = dane.author
    title = dane.title
    link = dane.link
    data = dane.published[5:-9]
    published = [''] + data \
        .rsplit(sep=" ", maxsplit=1)
    sol_daty = data_surowa(published)
    data_czytelna = data_przerobiona(sol_daty)
    yield author, title, link, data_czytelna, sol_daty


def daneFacebook(dane):
    tresc = dane[0]
    tresc = tresc.replace('\n', ' ') \
        .replace('shared a link to the group', 'udostępnił link do grupy') \
        .split('https://' or 'http://')
    link = dane[1]
    data = dane[2]
    data = data.rstrip(data[-2:]).replace('-', '').replace(':', '').replace(' ', '')
    if data == 'No':
        pass
    else:
        yield tresc[0], link, data_przerobiona(data), data


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


def zupaStrony(dane):
    """
    funkcja pobiera kod strony internetowej. Następnie
    wydobywa ARTYKUŁY celem sprawdzenia
    które z nich są najstarsze i przekazuje dalej.
    :param dane:
    :return:
    """
    dane = feedparser.parse(dane)
    for x in range(8):
        yield dane.entries[x]


def zupaFacebook(dane):
    """
    funkcja pobiera kod strony facebookowej. Następnie
    wydobywa z niej posty celem sprawdzenia
    które z nich są najstarsze i przekazuje dalej.
    :param dane:
    :return:
    """
    from facebook_scraper import get_posts

    for post in get_posts(dane, pages=8):
        if post['text'][:50] or post['post_url'] or post['time'] is not None:
            yield f"{post['text'][:50]}...", f"{post['post_url']}", f"{post['time']}"
        else:
            pass


def zrzutForum(dane):
    """
    funkcja zrzuca wszystkie wydobyte dane z Forum w formie listy i je drukuje.
    :return:
    """
    return tuple([daneForum(x) for x in (zupaForum(i))] for i in dane)


def zrzutStrony(dane):
    """
    funkcja zrzuca wszystkie wydobyte dane z RSS w formie listy i je drukuje.
    :return:
    """
    return tuple([*daneStrony(i)] for i in zupaStrony(dane))


def zrzutFacebook(dane):
    """
    funkcja zrzuca wszystkie wydobyte dane z Forum w formie listy i je drukuje.
    :return:
    """
    return tuple([*daneFacebook(i)] for i in zupaFacebook(dane))


def tekstPBF(dane=forumKrysztalyCzasuPbf()):
    from OperacjeNaPlikach import DataSystemuWatkuWyswietl, DataSystemuWatkuNadpisz
    data_archiwum = DataSystemuWatkuWyswietl('forumKrysztalyCzasuPbfData')
    data_temp = data_archiwum
    for strona in zrzutForum(dane):
        for watek in strona:
            if data_archiwum < watek[4]:
                if data_temp < watek[4]:
                    data_temp = watek[4]
                yield (f'Rozpoczęły się igrzyska ku chwale niezwyciężonego Katana. '
                       f'Dnia {watek[3][0]} o godzinie {watek[3][1]} niejaki {watek[0]} '
                       f'ogłosił, że szuka grupy śmiałków, gotowych podjąć się świętej '
                       f'próby zwanej {watek[1]}. Chętni przyjmowani są na {watek[2]}. \n'
                       f'Zwycięzcy okryją się wieczną chwałą!\n')
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
                yield (f'Uwaga! Uwaga! Ogłasza się, co następuje: Dnia {watek[3][0]} '
                       f'o godzinie {watek[3][1]}, niejaki {watek[0]} dopuścił się '
                       f'bluźnierstwa na temat {watek[1]}, i zostanie za to przykładnie '
                       f'ukarany na oczach tłumu {watek[2]}. \n'
                       f'Ku chwale Katana!\n')
    DataSystemuWatkuNadpisz('forumKrysztalyCzasuWatkiData', data_temp)


def tekstRSS(dane=kanalRssKrysztalyCzasu()):
    from OperacjeNaPlikach import DataSystemuWatkuWyswietl, DataSystemuWatkuNadpisz
    data_archiwum = DataSystemuWatkuWyswietl('kanalRssKrysztalyCzasuData')
    data_temp = data_archiwum
    for kanalRss in zrzutStrony(dane):
        for artykul in kanalRss:
            if data_archiwum < artykul[4]:
                if data_temp < artykul[4]:
                    data_temp = artykul[4]
                yield (f'Dekretem samego Katana ogłasza się, co następuje: '
                       f'Dnia {artykul[3][0]} o godzinie {artykul[3][1]} '
                       f'odtajniono wpis z Wielkiego Archiwum Katana. '
                       f'Niejaki {artykul[0]} podaje kluczowe Informacje '
                       f'dla funkcjonowania całego imperium na temat {artykul[1]}, {artykul[2]}.\n')
    DataSystemuWatkuNadpisz('kanalRssKrysztalyCzasuData', data_temp)


def tekstFacebook(dane=facebookWatki()):
    from OperacjeNaPlikach import DataSystemuWatkuWyswietl, DataSystemuWatkuNadpisz
    data_archiwum = DataSystemuWatkuWyswietl('facebookWatkiData')
    data_temp = data_archiwum
    for strona in zrzutFacebook(dane):
        for watek in strona:
            if data_archiwum < watek[3]:
                if data_temp < watek[3]:
                    data_temp = watek[3]
                yield f'Setyccy szpiedzy donoszą: "{watek[0]}", {watek[1]}\n'
    DataSystemuWatkuNadpisz('facebookWatkiData', data_temp)

# print(*tekstPBF(forumKrysztalyCzasuPbf()))
# print(*tekstForum(forumKrysztalyCzasuWatki()))
# print(*tekstRSS(kanalRssKrysztalyCzasu()))
# print(*tekstFacebook(facebookWatki())
