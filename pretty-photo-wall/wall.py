import os

basedir = os.path.join(os.getcwd(), "static")

class Wall(object):
    def __init__(self, dict):
        self.dict = dict
        self.half_col = 0
        self.half_row = 0
        self.z = 0
        self.positons = []
        self.folder = os.path.join(basedir, dict)

    def create(self):
        wall = {0: (2, 5, 5000), 10: (2, 5, 5000), 20: (4, 5, 5000), 30: (5, 6, 5000), 40: (5, 8, 6000),
                50: (5, 10, 6000),60: (6, 10, 6000), 70: (7, 10, 7000), 80: (8, 10, 7000),
                90: (9, 10, 8000), 100: (10, 10, 9000)}
        col = 0
        row = 0
        print(self.dict, self.folder)
        filelist = []
        for f in os.listdir(self.folder):
            filelist.append(f)

        count = len(filelist)
        for k in wall.keys():
            if count in range(k - 10, k + 1):
                col, row, self.z = wall[k-10]
        for x in range(400, 900 * row, 900):
            for y in range(300, 700 * col, 700):
                #convert to set
                #must be '/'
                self.positons.append((self.dict+"/"+filelist.pop(), x, y, self.z))

        self.half_col = col * 900 / 2
        self.half_row = row * 700 / 2
        print(self.positons)
        return self.positons

    def overview(self):
        x = self.half_row
        y = self.half_col
        z = self.z * 2
        return [x, y, z]
