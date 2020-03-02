class Automate (object):
    alphabet={}
    etats={}
    etatInitial=""
    etatsFinal={}
    instructions=[]
    def __init__(self):
        #l'alphabet : 
        stop=False
        X=set()
        print('l\'alphabet (entrer le caracter $ pour terminer) :')
        while not stop :
            alpha=input("")
            if alpha=='$' : 
                stop=True
            else :
                if (len(alpha)>1) or (len(alpha)==0):
                    print('vous devez entrer une lettre')
                else :
                    X.add(alpha)
        self.alphabet=X
        # les etats : 
        stop=False
        S=set()
        print('Les Etats (entrer le caracter $ pour terminer) :')
        while not stop :
            alpha=input("")
            if alpha=='$' : 
                stop=True
            else :
                S.add(alpha)
        self.etats=S
        stop=False
        S=set()
        print('Les états finaux (entrer le caracter $ pour terminer) :')
        while not stop :
            alpha=input("")
            if alpha=='$' : 
                stop=True
            else :
                if not(alpha in self.etats):
                    print('Erreur')
                else :
                    S.add(alpha)
        self.etatsFinal=S 
        stop=False
        while not stop : 
            alpha=input("entrer l'etat intial :")
            if not (alpha in self.etats) : 
                print("SVP, choisir un état valide")
            else :
                stop=True
        self.etatInitial=alpha
        #les instructions : 
        I={}
        for i in self.etats : 
            print ("taper $ pour terminer")
            print("entrer les instructions <",i,",word,Sj> (word=# pour vide) :")
            stop=False 
            I[i]={}
            while not stop : 
                alpha=input("word=")
                s=set(alpha)
                if alpha=="$" : 
                    stop=True 
                else:
                    if  not(s.issubset(self.alphabet.union(set('#')))): 
                        print("vous devez utiliser que les letters de l'alphabet ou #")
                    else :
                        etat=input("Sj=")
                        if not etat in self.etats : 
                            print ("etat non valide!")
                        else :
                            if not alpha in I[i].keys() : 
                                I[i][alpha]=[etat]
                            else: 
                                I[i][alpha].append(etat)
        self.instructions=I
    def reduireAutomate(self):
        #supprimer les etats non accessibles : 
        accessible=set()
        accessible.add(self.etatInitial)
        access=set()
        access.add(self.etatInitial)
        stop=False 
        while not stop : 
            for etat in accessible : 
                if etat in set(self.instructions.keys()) :
                    for word in self.instructions[etat].keys() : 
                        access=access.union(set(self.instructions[etat][word]))
            if access.issubset(accessible)  :           
                stop=True
            else : 
                accessible=accessible.union(access)
        for etat in self.etats.difference(accessible) : 
            if etat in set(self.instructions.keys()):
                del self.instructions[etat]
        self.etats=self.etats.intersection(accessible)
        self.etatsFinal=self.etatsFinal.intersection(accessible)
        #supprimer les etats non coaccessibles : 
        coaccessible=set(self.etatsFinal)
        coaccess=set(self.etatsFinal)
        empty=set()
        stop=False 
        while not stop : 
            for etat in self.etats : 
                if etat in set(self.instructions.keys()) : 
                    for word in self.instructions[etat].keys(): 
                        s=set(self.instructions[etat][word]).intersection(coaccess)
                        if not s.issubset(empty) : 
                            coaccess.add(etat)
            if coaccess.issubset(coaccessible)  :           
                stop=True
            else : 
                coaccessible=coaccessible.union(coaccess)   
        for etat in self.etats.difference(coaccessible) : 
            if etat in set(self.instructions.keys()):
                del self.instructions[etat]
        self.etats=self.etats.intersection(coaccessible)
        self.etatsFinal=self.etatsFinal.intersection(coaccessible)
        for etat in self.instructions.keys() : 
            for word in self.instructions[etat].keys() :
                self.instructions[etat][word]=list(self.etats.intersection(set(self.instructions[etat][word])))
    def rendreSimple(self):
        cpt=len(self.etats)
        #rendre l'automate partiellement génerlisé:
        for etat in list(self.instructions.keys()) : 
            for word in list(self.instructions[etat].keys()) :
                if len(word)>1 : 
                    Sj=set(self.instructions[etat][word])
                    del self.instructions[etat][word]
                    Si=etat
                    length=len(word)
                    for l in word : 
                        if not (length==1): 
                            self.etats.add('S'+str(cpt))
                            self.instructions['S'+str(cpt)]={}
                            if (l in self.instructions[Si].keys()) : 
                                self.instructions[Si][l].append('S'+str(cpt))
                            else : 
                                self.instructions[Si][l]=['S'+str(cpt)]
                            Si='S'+str(cpt)
                            cpt+=1
                        else : 
                            self.instructions[Si][l]=list(Sj)
                        length-=1
        #rendre l'automate simple :
        etat=self.etatInitial
        stop=False
        while not stop :
            stop=True
            for etat in list(self.instructions.keys()):
                for word in list(self.instructions[etat].keys()) :
                    if (word=='#'):
                        stop=False
                        for state in list(self.instructions[etat][word]):
                            if (state!=etat): 
                                for l in list(self.instructions[state].keys()) :
                                    if l in self.instructions[etat].keys() : 
                                        self.instructions[etat][l]=list(set(self.instructions[etat][l]+self.instructions[state][l]))
                                    else : 
                                        self.instructions[etat][l]=self.instructions[state][l]
                            self.instructions[etat][word].remove(state)
                        if(len(self.instructions[etat][word])==0) :
                            del self.instructions[etat][word]
    def rendreDeterminist(self):
        if not self.estSimple : 
            self.rendreSimple()
        etats=set()
        etats.add(self.etatInitial)
        I={}
        updatedEtats=set()
        updatedEtats.add(self.etatInitial)
        stop=False
        while not stop :
            for etat in list(etats) : 
                sousEtats=etat.split('|')
                print(sousEtats,etat)
                I[etat]={}
                for sousEtat in sousEtats :    
                    for word in self.instructions[sousEtat].keys() :
                        nouveauEtat=''
                        for state in list(self.instructions[sousEtat][word]):
                            if len(nouveauEtat)!=0 :
                               nouveauEtat=nouveauEtat+'|'+state   
                            else:
                                nouveauEtat=state
                        updatedEtats.add(nouveauEtat)
                        I[etat][word]=[nouveauEtat]
            if (updatedEtats.issubset(etats)) : 
                stop=True
            else : 
                etats=etats.union(updatedEtats)
        self.etats=updatedEtats
        self.instructions=I
        final=set()
        for etat in list(self.etats):
            if (len(set(etat.split('|')).intersection(self.etatsFinal))!=0 ): 
                final.add(etat)
        self.etatsFinal=final
    def estSimple(self):
        response=True
        for etat in self.instructions.keys() :
            for word in self.instructions[etat].keys(): 
                if (len(word)>1): 
                    response=False
                if (word=='#'):
                    response=False
        return response
    def estDeterminist(self):
        response=True
        for etat in self.instructions.keys():
            for word in self.instructions[etat].keys(): 
                if (len(self.instructions[etat][word])>1)  : 
                    response=False
        return response and self.estSimple()
    def construireComplement(self, complement):
        self.reduireAutomate()
        self.rendreSimple()
        self.rendreDeterminist()
        self.rendreComplet()
        self.etatsFinal=self.etats.difference(self.etatsFinal)
    def rendreComplet(self):
        self.reduireAutomate()
        self.rendreSimple()
        self.rendreDeterminist()
        for etat in list(self.instructions.keys()):
            for word in self.alphabet : 
                if not (word in set(self.instructions[etat].keys)): 
                    self.instructions[etat][word]=['Sp']
        self.etats.add('Sp')
        self.instructions['Sp']={}
        for word in self.alphabet :
            self.instructions['Sp'][word]=['Sp']

    def lireMot(self,mot):
        pass
v=Automate()