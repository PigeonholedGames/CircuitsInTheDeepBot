from main import self


class Character:

    def __init__(self, aptitudenames, aptitudestats, skillnames, skillstats, server='', thread='', player='', name='', alias='', playbook='', abilities='', traits='', luck=9, realization=0):
        
        self.server = server
        self.thread = thread
        self.player = player
        self.name = name
        self.alias = alias
        self.playbook = playbook
        self.abilities = abilities
        self.traits = traits
        self.luck = luck
        self.realization = realization

        for x in skillnames:
            self.aptitudes1 = {
                aptitudenames[0]: (aptitudestats[0][0], aptitudestats[0][1], aptitudestats[0][2], aptitudestats[0][3], aptitudestats[0][4]),
                skillnames[0]: skillstats[0],
                skillnames[1]: skillstats[1],
                skillnames[2]: skillstats[2],
                skillnames[3]: skillstats[3],
                skillnames[4]: skillstats[4],
                skillnames[5]: skillstats[5],
                skillnames[6]: skillstats[6],
            }
            self.aptitudes2 = {
                aptitudenames[1]: (aptitudestats[1][0], aptitudestats[1][1], aptitudestats[1][2], aptitudestats[1][3], aptitudestats[1][4]),
                skillnames[7]: skillstats[7],
                skillnames[8]: skillstats[8],
                skillnames[9]: skillstats[9],
                skillnames[10]: skillstats[10],
                skillnames[11]: skillstats[11],
                skillnames[12]: skillstats[12],
                skillnames[13]: skillstats[13],
            }
            self.aptitudes3 = {
                aptitudenames[2]: (aptitudestats[2][0], aptitudestats[2][1], aptitudestats[2][2], aptitudestats[2][3], aptitudestats[2][4]),
                skillnames[14]: skillstats[14],
                skillnames[15]: skillstats[15],
                skillnames[16]: skillstats[16],
                skillnames[17]: skillstats[17],
                skillnames[18]: skillstats[18],
                skillnames[19]: skillstats[19],
                skillnames[20]: skillstats[20],
            }
            self.aptitudes4 = {
                aptitudenames[3]: (aptitudestats[3][0], aptitudestats[3][1], aptitudestats[3][2], aptitudestats[3][3], aptitudestats[3][4]),
                skillnames[21]: skillstats[21],
                skillnames[22]: skillstats[22],
                skillnames[23]: skillstats[23],
                skillnames[24]: skillstats[24],
                skillnames[25]: skillstats[25],
                skillnames[26]: skillstats[26],
                skillnames[27]: skillstats[27],
            }
            self.aptitudes5 = {
                aptitudenames[4]: (aptitudestats[4][0], aptitudestats[4][1], aptitudestats[4][2], aptitudestats[4][3], aptitudestats[4][4]),
                skillnames[28]: skillstats[28],
                skillnames[29]: skillstats[29],
                skillnames[30]: skillstats[30],
                skillnames[31]: skillstats[31],
                skillnames[32]: skillstats[32],
                skillnames[33]: skillstats[33],
                skillnames[34]: skillstats[34],
            }
            self.aptitudes6 = {
                aptitudenames[5]: (aptitudestats[5][0], aptitudestats[5][1], aptitudestats[5][2], aptitudestats[5][3], aptitudestats[5][4]),
                skillnames[35]: skillstats[35],
                skillnames[36]: skillstats[36],
                skillnames[37]: skillstats[37],
                skillnames[38]: skillstats[38],
                skillnames[39]: skillstats[39],
                skillnames[40]: skillstats[40],
                skillnames[41]: skillstats[41],
            }
            self.aptitudes7 = {
                aptitudenames[6]: (aptitudestats[6][0], aptitudestats[6][1], aptitudestats[6][2], aptitudestats[6][3], aptitudestats[6][4]),
                skillnames[42]: skillstats[42],
                skillnames[43]: skillstats[43],
                skillnames[44]: skillstats[44],
                skillnames[45]: skillstats[45],
                skillnames[46]: skillstats[46],
                skillnames[47]: skillstats[47],
                skillnames[48]: skillstats[48],
            }
            self.aptitudes8 = {
                aptitudenames[7]: (aptitudestats[7][0], aptitudestats[7][1], aptitudestats[7][2], aptitudestats[7][3], aptitudestats[7][4]),
                skillnames[49]: skillstats[49],
                skillnames[50]: skillstats[50],
                skillnames[51]: skillstats[51],
                skillnames[52]: skillstats[52],
                skillnames[53]: skillstats[53],
                skillnames[54]: skillstats[54],
                skillnames[55]: skillstats[55],
            }
            self.aptitudes9 = {
                aptitudenames[8]: (aptitudestats[8][0], aptitudestats[8][1], aptitudestats[8][2], aptitudestats[8][3], aptitudestats[8][4]),
                skillnames[56]: skillstats[56],
                skillnames[57]: skillstats[57],
                skillnames[58]: skillstats[58],
                skillnames[59]: skillstats[59],
                skillnames[60]: skillstats[60],
                skillnames[61]: skillstats[61],
                skillnames[62]: skillstats[62],
            }
            self.aptitudes10 = {
                aptitudenames[9]: (aptitudestats[9][0], aptitudestats[9][1], aptitudestats[9][2], aptitudestats[9][3], aptitudestats[9][4]),
                skillnames[63]: skillstats[63],
                skillnames[64]: skillstats[64],
                skillnames[65]: skillstats[65],
                skillnames[66]: skillstats[66],
                skillnames[67]: skillstats[67],
                skillnames[68]: skillstats[68],
                skillnames[69]: skillstats[69],
            }
            self.aptitudes11 = {
                aptitudenames[10]: (aptitudestats[10][0], aptitudestats[10][1], aptitudestats[10][2], aptitudestats[10][3], aptitudestats[10][4]),
                skillnames[70]: skillstats[70],
                skillnames[71]: skillstats[71],
                skillnames[72]: skillstats[72],
                skillnames[73]: skillstats[73],
                skillnames[74]: skillstats[74],
                skillnames[75]: skillstats[75],
                skillnames[76]: skillstats[76],
            }
            self.aptitudes12 = {
                aptitudenames[11]: (aptitudestats[11][0], aptitudestats[11][1], aptitudestats[11][2], aptitudestats[11][3], aptitudestats[11][4]),
                skillnames[77]: skillstats[77],
                skillnames[78]: skillstats[78],
                skillnames[79]: skillstats[79],
                skillnames[80]: skillstats[80],
                skillnames[81]: skillstats[81],
                skillnames[82]: skillstats[82],
                skillnames[83]: skillstats[83],
            }

    def getServer(self):
        return self.server

    def getThread(self):
        return self.thread

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setAlias(self, alias):
        self.alias = alias

    def getAlias(self):
        return self.alias

    def setPlaybook(self, playbook):
        self.playbook = playbook

    def getPlaybook(self):
        return self.playbook

    def setAbilities(self, abilities):
        self.abilities = abilities

    def getAbilities(self):
        return self.abilities

    def setTraits(self, traits):
        self.traits = traits

    def getTraits(self):
        return self.traits

    def changeLuck(self, luck):
        self.luck = self.luck + luck

    def getLuck(self):
        return self.luck

    def changeRealization(self, realization):
        self.realization = self.realization + realization

    def getRealization(self):
        return self.realization
