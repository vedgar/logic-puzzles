import types, graph, itertools

class Objekt(types.SimpleNamespace):
    __hash__ = object.__hash__

    def __str__(self):
        return self.ime

class Osoba(Objekt):
    vozač = False

class Splav(Objekt):
    vozač = None

tata = Osoba(vozač=True)
mama = Osoba(vozač=True)
sin1 = Osoba()
sin2 = Osoba()
kći1 = Osoba()
kći2 = Osoba()
policajac = Osoba(vozač=True)
lopov = Osoba()

splav = Splav()

objekti = set()
ime = objekt = None
kod = 1
for ime, objekt in sorted(vars().items()):
    if isinstance(objekt, Objekt) and ime != 'objekt':
        objekt.ime = ime
        objekt.kod = kod
        kod *= 2
        objekti.add(objekt)

def dozvoljen(s):
    """Odgovara li skup objekata s uvjetima zadatka."""
    if tata in s and mama not in s and (kći1 in s or kći2 in s): return False
    if mama in s and tata not in s and (sin1 in s or sin2 in s): return False
    if policajac not in s and s > {lopov}: return False
    return True

def partitivni(s):
    """Partitivni generator skupa s."""
    return itertools.chain.from_iterable(
        itertools.combinations(s, broj_el) for broj_el in range(len(s) + 1))

class Konfiguracija(graph.Node, frozenset):
    def kod(self):
        return sum(objekt.kod for objekt in self)
    
    def ok(self):
        return dozvoljen(self) and dozvoljen(objekti - self)

    def susjedna(self, druga):
        if self.ok() and druga.ok() and (self < druga or self > druga):
            prešlo = self ^ druga
            return splav in prešlo and len(prešlo) <= 3 and any(
                osoba.vozač for osoba in prešlo)

    def neighbors(self):
        for konfiguracija in prostor:
            if self.susjedna(konfiguracija):
                yield konfiguracija, (self ^ konfiguracija) - {splav}, 1

prostor = set(filter(Konfiguracija.ok, map(Konfiguracija, partitivni(objekti))))
print(len(prostor))
početna = Konfiguracija()
završna = Konfiguracija(objekti)

def rješenje():
    for i, prelaznici in enumerate(početna.astar(završna), 1):
        print(i, *prelaznici)

def graf():
    for lijevo in prostor:
        for desno in prostor:
            if lijevo.susjedna(desno):
                lk = lijevo.kod()
                dk = desno.kod()
                if lk < dk:
                    print(lk, '--', dk)

graf()
