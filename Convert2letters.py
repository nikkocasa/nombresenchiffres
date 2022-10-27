LANG = "FR-be"  # "FR-fr, FR-be",  etc.
CURRENCY = "Euro"
d_units2twenty = {0:"Zéro",1:"Un",2:"Deux",3:"Trois",4:"Quatre",5:"Cinq",6:"Six",7:"Sept",8:"Huit",9:"Neuf",
                  10:"Dix", 11:"Onze", 12:"Douze", 13:"Treize", 14:"Quatorze", 15:"Quinze",
                  16:"Seize", 17:"Dix-sept", 18:"Dix-huit", 19:"Dix-neuf"}

d_tensUp20 = {20: "Vingt", 30: "Trente", 40: "Quarante", 50: "Cinquante", 60: "Soixante", 70: "Soixante",
              80: "Quatre-vingt", 90: "Quatre-vingt"}\
            if LANG == "FR-fr" else\
             {20: "Vingt", 30: "Trente", 40: "Quarante", 50: "Cinquante", 60: "Soixante", 70: "Septante",
              80: "Octante", 90: "Nonante"}

d_mUp100 = {0:["Centimes", "Euros"], 1:d_tensUp20, 2:["Cent", "Cents"]}
d_mUp1000 = {0:["Euros", "Centimes"], 1:"mille", 2:["million", "millions"], 3:["milliard", "milliards"], 4:["Trillard", "Trillards"]}

def convSt2DicByN(stnb, n=3):
    """ Return a dict of cutting the string in group of n char ordering key from right to left (as numbering does)
    [convSt2DicByN("123456748901", 3)    -->> {3: '12', 2: '345', 1: '678', 0: '901'} """
    return {**({} if len(stnb) % n == 0 else {len(stnb) // n:stnb[0:len(stnb) % n]}),
            **{((len(stnb) - i)-1) // n:stnb[i:i+n] for i in range(len(stnb) % n, len(stnb), n)}}

def convSt2DicIntByN(stnb, n=3):
    """ Return a dict of cutting the string in group of n char convertong it in int
     ordering key from right to left (as numbering does)
    [convSt2DicByN("123456748901", 3)    -->> {3: 12, 2: 345, 1: 678, 0: 901} """
    return {**({} if len(stnb) % n == 0 else {len(stnb) // n:int(stnb[0:len(stnb) % n])}),
            **{((len(stnb) - i)-1) // n:int(stnb[i:i+n]) for i in range(len(stnb) % n, len(stnb), n)}}

def convIntUnderThousand(nb):
    _intnb = nb if type(nb) is int else int(nb)
    if _intnb < 20:
        return d_units2twenty[_intnb]
    elif 20 <= _intnb < 100:
        div = _intnb // 10
        modulo = (_intnb % 10) if LANG != "FR-fr" else (_intnb % (10 if div < 6 else 60 if div < 8 else 80))
        if modulo == 0:
            return d_tensUp20[_intnb]
        elif (modulo == 1 or modulo == 11) and LANG == "FR-fr":  # case "soixante et onze, etc
            return "".join([d_tensUp20[_intnb - modulo], " et " if div < 8 else "-", d_units2twenty[modulo]])
        else:
            return "-".join([d_tensUp20[_intnb - modulo], d_units2twenty[modulo].lower()])
    elif 100 <= _intnb < 1000:
        Div, Rest = _intnb // 100, _intnb - ((_intnb // 100) * 100)
        res = " ".join([d_units2twenty[Div] if (Div > 1) else "",
                        "".join([d_mUp100[2][0], "s" if (Div > 1 and Rest == 0) else ""]),
                        convIntUnderThousand(Rest) if Rest != 0 else ""
                        ])
        return res.strip(" ")
    else:
        return "up to 999"  # need to raise error in your context !

def convInt2lettres(integer, unit):
    d_Inr_str = convSt2DicIntByN(str(integer))
    Letters = []
    for rank in d_Inr_str.keys():
        Conv2Letter = convIntUnderThousand(int(d_Inr_str[rank]))
        if rank == 0:
            Letters.append(Conv2Letter)
            Letters.append(d_mUp1000[rank][unit] if type(d_mUp1000[rank]) is list else d_mUp1000[rank])
        elif Conv2Letter != d_units2twenty[0]:
            Letters.append(Conv2Letter)
            Letters.append(d_mUp1000[rank][0] if type(d_mUp1000[rank]) is list else d_mUp1000[rank])
    return " ".join(Letters)

def convNombre2lettres(nombre):
    _enstr = str(nombre).split('.')
    _pent = convInt2lettres(int(nombre), 0)
    _pdec = convInt2lettres(int(_enstr[1]), 1) if len(_enstr) > 1 else ""
    return (_pent + " et " + _pdec) if len(_pdec) > 0 else _pent


print(convNombre2lettres(45.91))
print(convNombre2lettres(8.54))
print(convNombre2lettres(05.99))
print(convNombre2lettres(10000000.00))
print(convNombre2lettres(12345678901.99))
