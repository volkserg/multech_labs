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
        if self.type == 'P2':
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

    def _norm(self, pixel):
        # return int(pixel)
        if pixel > self.intens:
            return self.intens
        if pixel < 0:
            return self._norm(pixel*(-1))
        else:
            return int(pixel)

    def _haar(self, pixels):
        matrix = []
        new_pixels = []
        if len(pixels) % 2 != 0:
            pixels.append([0 for i in range(len(pixels[0]))])
        if len(pixels[0]) % 2 != 0:
            for i in range(len(pixels)):
                pixels[i].append(0)
        for i in range(len(pixels)):
            new_line = []
            for j in range(int(len(pixels[i])/2)):
                new_line.append((pixels[i][2*j]+pixels[i][2*j+1])/2)
            for j in range(int(len(pixels[i])/2)):
                new_line.append((pixels[i][2*j]-pixels[i][2*j+1])/2)
            matrix.append(new_line)
        for i in range(int(len(matrix)/2)):
            new_line = []
            for j in range(len(matrix[i])):
                new_line.append(self._norm((matrix[2*i][j]+matrix[2*i+1][j])/2))
            new_pixels.append(new_line)
        for i in range(int(len(matrix) / 2)):
            new_line = []
            for j in range(len(matrix[i])):
                new_line.append(self._norm((matrix[2*i][j]-matrix[2*i+1][j])/2))
            new_pixels.append(new_line)
        return new_pixels

    def haar(self):
        if self.type == 'P2':
            self.pixels = self._haar(self.pixels)
        if self.type == 'P3':
            self.pixels['r'] = self._haar(self.pixels['r'])
            self.pixels['g'] = self._haar(self.pixels['g'])
            self.pixels['b'] = self._haar(self.pixels['b'])




