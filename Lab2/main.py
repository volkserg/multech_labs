class Image:

    def __init__(self, filename):
        with open(filename, 'r') as f:
            img = f.read()
            rows = img.strip().split('\n')
            image = []
            for row in rows:
                for el in row.split(' '):
                    if el:
                        image.append(el)
            self.pixels = []
            self.type = image[0]
            self.width = int(image[1])
            self.height = int(image[2])
            self.intens = int(image[3])
            self.get_pixels(image[4:])
            self.counter = 0

    def get_pixels(self, pixels):
        if self.type=='P2':
            q = 0
            self.pixels = []
            for i in range(self.height):
                temp_row = []
                for j in range(self.width):
                    temp_row.append(int(pixels[q]))
                    q += 1
                self.pixels.append(temp_row)

        if self.type == 'P3':
            q = 0
            self.pixels = {}
            r, g, b = [], [], []
            for i in range(self.height):
                r_row, g_row, b_row = [], [], []
                for j in range(self.width):
                    r_row.append(int(pixels[q]))
                    g_row.append(int(pixels[q+1]))
                    b_row.append(int(pixels[q+2]))
                    q += 3
                r.append(r_row)
                g.append(g_row)
                b.append(b_row)
            self.pixels['r'] = r
            self.pixels['g'] = g
            self.pixels['b'] = b

    def save_image(self, filename):
        with open (filename, 'w') as f:
            if self.type == 'P2':
                f.write('P2\n')
                f.write(str(self.width) + ' ' + str(self.height) + "\n")
                f.write(str(self.intens) + "\n")
                for i in range(self.height):
                    for j in range(self.width):
                        f.write(str(self.pixels[i][j]) + " ")
                    f.write("\n")

            if self.type == 'P3':
                f.write('P3\n')
                f.write(str(self.width) + ' ' + str(self.height) + "\n")
                f.write(str(self.intens) + "\n")
                for i in range(self.height):
                    for j in range(self.width):
                        f.write(str(self.pixels['r'][i][j]) + " ")
                        f.write(str(self.pixels['g'][i][j]) + " ")
                        f.write(str(self.pixels['b'][i][j]) + " ")
                    f.write("\n")

    def _norm(self, pix):
        if pix > self.intens:
            return self.intens
        elif pix < 0:
            return 0
        else:
            return pix

    def _conv_pixel(self, m1, m2):
        res = 0
        div = 0
        for k in m2:
            for m in k:
                div += m
        for i in range(len(m1)):
            for j in range(len(m1[0])):
                res += m1[i][j]*m2[i][j]
        self.counter += 1
        if div == 0:
            return self._norm(res)
        else:
            return self._norm(int(res/div))

    # def _exp(self, coresize):
    #     size = int(coresize/2)
    #     new_img = []
    #     for i in range(0, self.height + 2 * size):
    #         row = []
    #         for j in range(0, self.width + 2 * size):
    #             if ((j < size) or (j >= self.width + size)) or ((i < size) or (i>=self.height+size)):
    #                 row.append(0)
    #             else:
    #                 row.append(self.pixels[i-size][j-size])
    #         new_img.append(row)
    #     return new_img

    def change(self, pixels, core):
        new_pixels = []
        img = pixels #self._exp(core.size)
        for i in range(int(core.size/2), len(img)-int(core.size/2)):
            new_pixel_row = []
            for j in range(int(core.size/2), len(img[0])-int(core.size/2)):
                matrix = []
                rows = img[i-int(core.size/2):i+int(core.size/2)+1]
                for row in rows:
                    matrix.append(row[j-int(core.size/2):j+int(core.size/2)+1])
                new_pixel_row.append(self._conv_pixel(matrix, core.matrix))
            new_pixels.append(new_pixel_row)
        self.height = len(new_pixels)
        self.width = len(new_pixels[0])
        return new_pixels

    def make_filter(self, core):
        if self.type == 'P2':
            pixels = self.change(self.pixels, core)
            self.pixels = pixels
        if self.type == 'P3':
            self.pixels['r'] = self.change(self.pixels['r'], core)
            self.pixels['g'] = self.change(self.pixels['g'], core)
            self.pixels['b'] = self.change(self.pixels['b'], core)





class Core:

    def __init__(self, filename):
        self.matrix = []
        self.height, self.width = 0, 0
        self.get_core(filename)

    def get_core(self, filename):
        with open(filename, 'r') as f:
            file = f.read()
            rows = file.split('\n')
            self.size = len(rows)
            for row in rows:
                current_row = row.split(' ')
                self.matrix.append([int(i) for i in current_row])
