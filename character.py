class Character:

    def __init__(self, aptitudenames, aptitudestats=None, skillnames='', skillstats=None, server='', thread='', player='', name='', playbook='', stuff='', traits='', luck=9, realization=0, harm1='', harm1clock=0, harm2='', harm2clock=0, harm3='', harm3clock=0):

        self.server = server
        self.thread = thread
        self.player = player
        self.name = name
        self.stuff = stuff
        self.traits = traits
        self.luck = luck
        self.realization = realization

        # harm is the name of the affected area and the number of ticks on the clock to heal it
        self.harm1 = {harm1, harm1clock}
        self.harm2 = {harm2, harm2clock}
        self.harm3 = {harm3, harm3clock}

        # a dictionary of all aptitudes containing a nested dictionary of its skills alongside their stat requirement
        # additional comment from a later me: WHAT THE FUCK, WHY DID I DO THIS
        if aptitudestats is None:
            self.skills = {
                aptitudenames[0]: {
                    skillnames[0]: [0, 0],
                    skillnames[1]: [0, 0],
                    skillnames[2]: [0, 0],
                    skillnames[3]: [0, 0],
                    skillnames[4]: [0, 2],
                    skillnames[5]: [0, 4]},
                aptitudenames[1]: {
                    skillnames[6]: [0, 0],
                    skillnames[7]: [0, 0],
                    skillnames[8]: [0, 0],
                    skillnames[9]: [0, 0],
                    skillnames[10]: [0, 2],
                    skillnames[11]: [0, 4]},
                aptitudenames[2]: {
                    skillnames[12]: [0, 0],
                    skillnames[13]: [0, 0],
                    skillnames[14]: [0, 0],
                    skillnames[15]: [0, 0],
                    skillnames[16]: [0, 2],
                    skillnames[17]: [0, 4]},
                aptitudenames[3]: {
                    skillnames[18]: [0, 0],
                    skillnames[19]: [0, 0],
                    skillnames[20]: [0, 0],
                    skillnames[21]: [0, 0],
                    skillnames[22]: [0, 2],
                    skillnames[23]: [0, 4]},
                aptitudenames[4]: {
                    skillnames[24]: [0, 0],
                    skillnames[25]: [0, 0],
                    skillnames[26]: [0, 0],
                    skillnames[27]: [0, 0],
                    skillnames[28]: [0, 2],
                    skillnames[29]: [0, 4]},
                aptitudenames[5]: {
                    skillnames[30]: [0, 0],
                    skillnames[31]: [0, 0],
                    skillnames[32]: [0, 0],
                    skillnames[33]: [0, 0],
                    skillnames[34]: [0, 2],
                    skillnames[35]: [0, 4]},
                aptitudenames[6]: {
                    skillnames[36]: [0, 0],
                    skillnames[37]: [0, 0],
                    skillnames[38]: [0, 0],
                    skillnames[39]: [0, 0],
                    skillnames[40]: [0, 2],
                    skillnames[41]: [0, 4]},
                aptitudenames[7]: {
                    skillnames[42]: [0, 0],
                    skillnames[43]: [0, 0],
                    skillnames[44]: [0, 0],
                    skillnames[45]: [0, 0],
                    skillnames[46]: [0, 2],
                    skillnames[47]: [0, 4]},
                aptitudenames[8]: {
                    skillnames[48]: [0, 0],
                    skillnames[49]: [0, 0],
                    skillnames[50]: [0, 0],
                    skillnames[51]: [0, 0],
                    skillnames[52]: [0, 2],
                    skillnames[53]: [0, 4]},
                aptitudenames[9]: {
                    skillnames[54]: [0, 0],
                    skillnames[55]: [0, 0],
                    skillnames[56]: [0, 0],
                    skillnames[57]: [0, 0],
                    skillnames[58]: [0, 2],
                    skillnames[59]: [0, 4]},
                aptitudenames[10]: {
                    skillnames[60]: [0, 0],
                    skillnames[61]: [0, 0],
                    skillnames[62]: [0, 0],
                    skillnames[63]: [0, 0],
                    skillnames[64]: [0, 2],
                    skillnames[65]: [0, 4]},
                aptitudenames[11]: {
                    skillnames[66]: [0, 0],
                    skillnames[67]: [0, 0],
                    skillnames[68]: [0, 0],
                    skillnames[69]: [0, 0],
                    skillnames[70]: [0, 2],
                    skillnames[71]: [0, 4]}
            }
        else:
            self.skills = {
                aptitudenames[0]: {
                    skillnames[0]: [skillstats[0], 0],
                    skillnames[1]: [skillstats[1], 0],
                    skillnames[2]: [skillstats[2], 0],
                    skillnames[3]: [skillstats[3], 0],
                    skillnames[4]: [skillstats[4], 2],
                    skillnames[5]: [skillstats[5], 4]},
                aptitudenames[1]: {
                    skillnames[6]: [skillstats[6], 0],
                    skillnames[7]: [skillstats[7], 0],
                    skillnames[8]: [skillstats[8], 0],
                    skillnames[9]: [skillstats[9], 0],
                    skillnames[10]: [skillstats[10], 2],
                    skillnames[11]: [skillstats[11], 4]},
                aptitudenames[2]: {
                    skillnames[12]: [skillstats[12], 0],
                    skillnames[13]: [skillstats[13], 0],
                    skillnames[14]: [skillstats[14], 0],
                    skillnames[15]: [skillstats[15], 0],
                    skillnames[16]: [skillstats[16], 2],
                    skillnames[17]: [skillstats[17], 4]},
                aptitudenames[3]: {
                    skillnames[18]: [skillstats[18], 0],
                    skillnames[19]: [skillstats[19], 0],
                    skillnames[20]: [skillstats[20], 0],
                    skillnames[21]: [skillstats[21], 0],
                    skillnames[22]: [skillstats[22], 2],
                    skillnames[23]: [skillstats[23], 4]},
                aptitudenames[4]: {
                    skillnames[24]: [skillstats[24], 0],
                    skillnames[25]: [skillstats[25], 0],
                    skillnames[26]: [skillstats[26], 0],
                    skillnames[27]: [skillstats[27], 0],
                    skillnames[28]: [skillstats[28], 2],
                    skillnames[29]: [skillstats[29], 4]},
                aptitudenames[5]: {
                    skillnames[30]: [skillstats[30], 0],
                    skillnames[31]: [skillstats[31], 0],
                    skillnames[32]: [skillstats[32], 0],
                    skillnames[33]: [skillstats[33], 0],
                    skillnames[34]: [skillstats[34], 2],
                    skillnames[35]: [skillstats[35], 4]},
                aptitudenames[6]: {
                    skillnames[36]: [skillstats[36], 0],
                    skillnames[37]: [skillstats[37], 0],
                    skillnames[38]: [skillstats[38], 0],
                    skillnames[39]: [skillstats[39], 0],
                    skillnames[40]: [skillstats[40], 2],
                    skillnames[41]: [skillstats[41], 4]},
                aptitudenames[7]: {
                    skillnames[42]: [skillstats[42], 0],
                    skillnames[43]: [skillstats[43], 0],
                    skillnames[44]: [skillstats[44], 0],
                    skillnames[45]: [skillstats[45], 0],
                    skillnames[46]: [skillstats[46], 2],
                    skillnames[47]: [skillstats[47], 4]},
                aptitudenames[8]: {
                    skillnames[48]: [skillstats[48], 0],
                    skillnames[49]: [skillstats[49], 0],
                    skillnames[50]: [skillstats[50], 0],
                    skillnames[51]: [skillstats[51], 0],
                    skillnames[52]: [skillstats[52], 2],
                    skillnames[53]: [skillstats[53], 4]},
                aptitudenames[9]: {
                    skillnames[54]: [skillstats[54], 0],
                    skillnames[55]: [skillstats[55], 0],
                    skillnames[56]: [skillstats[56], 0],
                    skillnames[57]: [skillstats[57], 0],
                    skillnames[58]: [skillstats[58], 2],
                    skillnames[59]: [skillstats[59], 4]},
                aptitudenames[10]: {
                    skillnames[60]: [skillstats[60], 0],
                    skillnames[61]: [skillstats[61], 0],
                    skillnames[62]: [skillstats[62], 0],
                    skillnames[63]: [skillstats[63], 0],
                    skillnames[64]: [skillstats[64], 2],
                    skillnames[65]: [skillstats[65], 4]},
                aptitudenames[11]: {
                    skillnames[66]: [skillstats[66], 0],
                    skillnames[67]: [skillstats[67], 0],
                    skillnames[68]: [skillstats[68], 0],
                    skillnames[69]: [skillstats[69], 0],
                    skillnames[70]: [skillstats[70], 2],
                    skillnames[71]: [skillstats[71], 4]}
            }

        # a dictionary containing all aptitudes, their levels, and their level up conditions
        if aptitudestats is None:
            self.aptitudes = {
                aptitudenames[0]: (0, 0),
                aptitudenames[1]: (0, 0),
                aptitudenames[2]: (0, 0),
                aptitudenames[3]: (0, 0),
                aptitudenames[4]: (0, 0),
                aptitudenames[5]: (0, 0),
                aptitudenames[6]: (0, 0),
                aptitudenames[7]: (0, 0),
                aptitudenames[8]: (0, 0),
                aptitudenames[9]: (0, 0),
                aptitudenames[10]: (0, 0),
                aptitudenames[11]: (0, 0),
            }
        else:
            self.aptitudes = {
                aptitudenames[0]: (
                    aptitudestats[0][0], aptitudestats[0][1], aptitudestats[0][2], aptitudestats[0][3],
                    aptitudestats[0][4]),
                aptitudenames[1]: (
                    aptitudestats[1][0], aptitudestats[1][1], aptitudestats[1][2], aptitudestats[1][3],
                    aptitudestats[1][4]),
                aptitudenames[2]: (
                    aptitudestats[2][0], aptitudestats[2][1], aptitudestats[2][2], aptitudestats[2][3],
                    aptitudestats[2][4]),
                aptitudenames[3]: (
                    aptitudestats[3][0], aptitudestats[3][1], aptitudestats[3][2], aptitudestats[3][3],
                    aptitudestats[3][4]),
                aptitudenames[4]: (
                    aptitudestats[4][0], aptitudestats[4][1], aptitudestats[4][2], aptitudestats[4][3],
                    aptitudestats[4][4]),
                aptitudenames[5]: (
                    aptitudestats[5][0], aptitudestats[5][1], aptitudestats[5][2], aptitudestats[5][3],
                    aptitudestats[5][4]),
                aptitudenames[6]: (
                    aptitudestats[6][0], aptitudestats[6][1], aptitudestats[6][2], aptitudestats[6][3],
                    aptitudestats[6][4]),
                aptitudenames[7]: (
                    aptitudestats[7][0], aptitudestats[7][1], aptitudestats[7][2], aptitudestats[7][3],
                    aptitudestats[7][4]),
                aptitudenames[8]: (
                    aptitudestats[8][0], aptitudestats[8][1], aptitudestats[8][2], aptitudestats[8][3],
                    aptitudestats[8][4]),
                aptitudenames[9]: (
                    aptitudestats[9][0], aptitudestats[9][1], aptitudestats[9][2], aptitudestats[9][3],
                    aptitudestats[9][4]),
                aptitudenames[10]: (
                    aptitudestats[10][0], aptitudestats[10][1], aptitudestats[10][2], aptitudestats[10][3],
                    aptitudestats[10][4]),
                aptitudenames[11]: (
                    aptitudestats[11][0], aptitudestats[11][1], aptitudestats[11][2], aptitudestats[11][3],
                    aptitudestats[11][4]),
            }

    def getServer(self):
        return self.server

    def getThread(self):
        return self.thread

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setStuff(self, stuff):
        self.stuff = stuff

    def getStuff(self):
        return self.stuff

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

    def getHarm(self):
        return [self.harm1, self.harm2, self.harm3]
