
class Character:

    def __init__(self, aptitudenames, aptitudestats, skillnames, skillstats, server, thread, player, name, playbook,
                 abilities, traits, alias='', luck=9, realization=0, harm1='', harm2='', harm3=''):
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
        self.harm1 = harm1
        self.harm2 = harm2
        self.harm3 = harm3

        # a dictionary of all aptitudes containing a nested dictionary of its skills alongside their stat requirement
        # additional comment from a later me: WHAT THE FUCK, WHY DID I DO THIS
        self.skills = {
            aptitudenames[0]: {
                skillnames[0]: [skillstats[0], 0],
                skillnames[1]: [skillstats[1], 0],
                skillnames[2]: [skillstats[2], 0],
                skillnames[3]: [skillstats[3], 0],
                skillnames[4]: [skillstats[4], 0],
                skillnames[5]: [skillstats[5], 2],
                skillnames[6]: [skillstats[6], 4]},
            aptitudenames[1]: {
                skillnames[7]: [skillstats[7], 0],
                skillnames[8]: [skillstats[8], 0],
                skillnames[9]: [skillstats[9], 0],
                skillnames[10]: [skillstats[10], 0],
                skillnames[11]: [skillstats[11], 0],
                skillnames[12]: [skillstats[12], 2],
                skillnames[13]: [skillstats[13], 4]},
            aptitudenames[2]: {
                skillnames[14]: [skillstats[14], 0],
                skillnames[15]: [skillstats[15], 0],
                skillnames[16]: [skillstats[16], 0],
                skillnames[17]: [skillstats[17], 0],
                skillnames[18]: [skillstats[18], 0],
                skillnames[19]: [skillstats[19], 2],
                skillnames[20]: [skillstats[20], 4]},
            aptitudenames[3]: {
                skillnames[21]: [skillstats[21], 0],
                skillnames[22]: [skillstats[22], 0],
                skillnames[23]: [skillstats[23], 0],
                skillnames[24]: [skillstats[24], 0],
                skillnames[25]: [skillstats[25], 0],
                skillnames[26]: [skillstats[26], 2],
                skillnames[27]: [skillstats[27], 4]},
            aptitudenames[4]: {
                skillnames[28]: [skillstats[28], 0],
                skillnames[29]: [skillstats[29], 0],
                skillnames[30]: [skillstats[30], 0],
                skillnames[31]: [skillstats[31], 0],
                skillnames[32]: [skillstats[32], 0],
                skillnames[33]: [skillstats[33], 2],
                skillnames[34]: [skillstats[34], 4]},
            aptitudenames[5]: {
                skillnames[35]: [skillstats[35], 0],
                skillnames[36]: [skillstats[36], 0],
                skillnames[37]: [skillstats[37], 0],
                skillnames[38]: [skillstats[38], 0],
                skillnames[39]: [skillstats[39], 0],
                skillnames[40]: [skillstats[40], 2],
                skillnames[41]: [skillstats[41], 4]},
            aptitudenames[6]: {
                skillnames[42]: [skillstats[42], 0],
                skillnames[43]: [skillstats[43], 0],
                skillnames[44]: [skillstats[44], 0],
                skillnames[45]: [skillstats[45], 0],
                skillnames[46]: [skillstats[46], 0],
                skillnames[47]: [skillstats[47], 2],
                skillnames[48]: [skillstats[48], 4]},
            aptitudenames[7]: {
                skillnames[49]: [skillstats[49], 0],
                skillnames[50]: [skillstats[50], 0],
                skillnames[51]: [skillstats[51], 0],
                skillnames[52]: [skillstats[52], 0],
                skillnames[53]: [skillstats[53], 0],
                skillnames[54]: [skillstats[54], 2],
                skillnames[55]: [skillstats[55], 4]},
            aptitudenames[8]: {
                skillnames[56]: [skillstats[56], 0],
                skillnames[57]: [skillstats[57], 0],
                skillnames[58]: [skillstats[58], 0],
                skillnames[59]: [skillstats[59], 0],
                skillnames[60]: [skillstats[60], 0],
                skillnames[61]: [skillstats[61], 2],
                skillnames[62]: [skillstats[62], 4]},
            aptitudenames[9]: {
                skillnames[63]: [skillstats[63], 0],
                skillnames[64]: [skillstats[64], 0],
                skillnames[65]: [skillstats[65], 0],
                skillnames[66]: [skillstats[66], 0],
                skillnames[67]: [skillstats[67], 0],
                skillnames[68]: [skillstats[68], 2],
                skillnames[69]: [skillstats[69], 4]},
            aptitudenames[10]: {
                skillnames[70]: [skillstats[70], 0],
                skillnames[71]: [skillstats[71], 0],
                skillnames[72]: [skillstats[72], 0],
                skillnames[73]: [skillstats[73], 0],
                skillnames[74]: [skillstats[74], 0],
                skillnames[75]: [skillstats[75], 2],
                skillnames[76]: [skillstats[76], 4]},
            aptitudenames[11]: {
                skillnames[77]: [skillstats[77], 0],
                skillnames[78]: [skillstats[78], 0],
                skillnames[79]: [skillstats[79], 0],
                skillnames[80]: [skillstats[80], 0],
                skillnames[81]: [skillstats[81], 0],
                skillnames[82]: [skillstats[82], 2],
                skillnames[83]: [skillstats[83], 4]}
        }

        # a dictionary containing all aptitudes, their levels, and their level up conditions
        self.aptitudeprogress = {
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

    def getHarm(self):
        return [self.harm1, self.harm2, self.harm3]
