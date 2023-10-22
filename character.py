import db


class Character:

    def __init__(self, aptitudes=None, skills=None, server='', thread='', player='',
                 name='', stuff=[], traits=[], luck=9, realization=0, harm1='', harm1clock=0, harm2='',
                 harm2clock=0, harm3='', harm3clock=0):

        self.aptitudes = aptitudes
        self.skills = skills
        self.server = server
        self.thread = thread
        self.player = player
        self.name = name
        self.stuff = stuff
        self.traits = traits
        self.luck = luck
        self.realization = realization
        self.harm1 = harm1
        self.harm1clock = harm1clock
        self.harm2 = harm2
        self.harm2clock = harm2clock
        self.harm3 = harm3
        self.harm3clock = harm3clock

        # a dictionary of all aptitudes containing a nested dictionary of its skills alongside their stat levels and requirements
        # additional comment from a later me: WHAT THE FUCK, WHY DID I DO THIS
        if skills is None:
            aptitudenamestemp = db.queryAptitudeNames()
            aptitudenames = []
            for n in aptitudenamestemp:
                aptitudenames.append(n[0])

            skillnamestemp = db.querySkillNames()
            skillnames = []
            for n in skillnamestemp:
                skillnames.append(n[0])

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

        # a dictionary containing all aptitudes, their levels, and their level up conditions
        if aptitudes is None:
            self.aptitudes = {
                aptitudenames[0]: [0, 0],
                aptitudenames[1]: [0, 0],
                aptitudenames[2]: [0, 0],
                aptitudenames[3]: [0, 0],
                aptitudenames[4]: [0, 0],
                aptitudenames[5]: [0, 0],
                aptitudenames[6]: [0, 0],
                aptitudenames[7]: [0, 0],
                aptitudenames[8]: [0, 0],
                aptitudenames[9]: [0, 0],
                aptitudenames[10]: [0, 0],
                aptitudenames[11]: [0, 0],
            }

    def getAptitude(self, name):
        return self.aptitudes[name][0]

    def getSkill(self, name):
        for y in self.skills:
            if name in self.skills[y].keys():
                return self.skills[y][name][0]
        raise Exception("Skill Name not Found")

    def getServer(self):
        return self.server

    def getThread(self):
        return self.thread

    def getName(self):
        return self.name

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

    def incrementAptitude(self, thread, name, x):
        if name not in self.aptitudes.keys():
            thread.send("Something has gone terribly wrong, please contact us.")
            raise Exception("Aptitude increment failed.")

        self.aptitudes[name][0] = self.aptitudes[name][0] + x

    def incrementSkill(self, thread, name, x):
        flag = True
        for y in self.skills:
            if name in self.skills[y].keys():
                flag = False
                self.skills[y][name][0] = self.skills[y][name][0] + x
        if flag:
            thread.send("Something has gone terribly wrong, please contact us.")
            raise Exception("Skill increment failed.")

    def addStuff(self, thing):
        self.stuff.append(thing)
