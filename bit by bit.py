import enum, types, collections, pprint


plava, žuta, crvena = 'plava žuta crvena'.split()


class Objekt(types.SimpleNamespace):
    __hash__ = object.__hash__
    __eq__ = object.__eq__


class Lik(Objekt):
    def __init__(self, orijentacija, boja):
        self.boja = boja
        self.orijentacija = orijentacija


class Iks(Objekt):
    def __init__(self, boja):
        self.boja = boja


class Kuća(Objekt):
    def __init__(self, boja):
        self.boja = boja


ulaz_ploča = [
    [None, None, None, Lik(-1j, žuta), None, None, None],
    [None, Lik(1, crvena), True, True, Lik(-1, žuta), True, None],
    [None, True, Lik(1, plava), Iks(žuta), True, True, True],
    [Lik(1, plava), True, Iks(plava), True, Iks(crvena), True, Lik(-1, crvena)],
    [None, None, True, True, True, None, None],
    [None, None, Kuća(plava), Kuća(žuta), Kuća(crvena), None, None],
]
raspolaganje = Strelica(plava)*2 + Strelica(crvena)*4 + Strelica(žuta)*2 + \
    Boja(plava)*2 + Boja(crvena)*2 + Boja(žuta)*2
    
assert len(set(map(len, ulaz_ploča))) == 1

ploča = {}
likovi = set()
slobodne = set()
for i, redak in enumerate(ulaz_ploča, 1):
    for j, ćelija in enumerate(redak, 1):
        pozicija = j - i*1j
        if isinstance(ćelija, (Kuća, Iks, bool)):
            ploča[pozicija] = ćelija
        if isinstance(ćelija, Lik):
            ploča[pozicija] = False
            ćelija.pozicija = pozicija
            likovi.add(ćelija)
        if ćelija is True:
            slobodne.add(pozicija)

