from collections import Counter, namedtuple
import heapq


class Image:

    def __init__(self, filename):
        with open(filename, 'r') as f:
            img = f.read()
            rows = img.split('\n')
            rows.pop()
            self.pixels = []
            self.type = rows.pop(0)
            self.width = int(rows[0].split(' ')[0])
            self.height = int(rows[0].split(' ')[1])
            rows.pop(0)
            self.intens = rows[0]
            rows.pop(0)
            self.get_pixels(rows)
            self.compressor = Compressor()

    def get_pixels(self, rows):
        if self.type=='P2':
            self.pixels = []
            for i in rows:
                current_row = i.split(' ')
                if current_row[len(current_row)-1] == '':
                    current_row.pop()
                for j in current_row:
                    self.pixels.append(int(j))

        if self.type == 'P3':
            self.pixels = {}
            r = []
            g = []
            b = []
            for i in rows:
                current_row = i.split(' ')
                for j in range(0, len(current_row), 3):
                    r.append(int(current_row[j]))
                for j in range(1, len(current_row), 3):
                    g.append(int(current_row[j]))
                for j in range(2, len(current_row), 3):
                    b.append(int(current_row[j]))
            self.pixels['r'] = r
            self.pixels['g'] = g
            self.pixels['b'] = b

    def save_image(self, filename):
        with open (filename, 'w') as f:
            if self.type == 'P2':
                f.write('P2\n')
                f.write(str(self.width) + ' ' + str(self.height) + "\n")
                f.write(str(self.intens) + "\n")
                pixel = 0
                for i in range(self.height):
                    for j in range(self.width):
                        f.write(str(self.pixels[pixel]) + " ")
                        pixel += 1
                    f.write("\n")

            if self.type == 'P3':
                f.write('P3\n')
                f.write(str(self.width) + ' ' + str(self.height) + "\n")
                f.write(str(self.intens) + "\n")
                pixel = 0
                for i in range(self.height):
                    for j in range(self.width):
                        f.write(str(self.pixels['r'][pixel]) + " ")
                        f.write(str(self.pixels['g'][pixel]) + " ")
                        f.write(str(self.pixels['b'][pixel]) + " ")
                        pixel += 1
                    f.write("\n")

    def rle(self):
        if self.type == 'P2':
            return self.compressor.rle(self.pixels)

        if self.type == 'P3':
            channels = {'r': self.compressor.rle(self.pixels['r']),
                        'g': self.compressor.rle(self.pixels['g']),
                        'b': self.compressor.rle(self.pixels['b'])}
            return channels

    def huffman(self):
        if self.type == 'P2':
            return self.compressor.huffman(self.pixels)

        if self.type == 'P3':
            channels = {'r': self.compressor.huffman(self.pixels['r']),
                        'g': self.compressor.huffman(self.pixels['g']),
                        'b': self.compressor.huffman(self.pixels['b'])}
            return channels


class Node(namedtuple("Node", ["left", "right"])):
    def walk(self, code, acc):
        self.left.walk(code, acc + "0")
        self.right.walk(code, acc + "1")


class Leaf (namedtuple("Leaf", ["char"])):
    def walk(self, code, acc):
        code[self.char] = acc


class Compressor:

    def __init__(self):
        pass

    def rle(self, pixels):
        res = []
        prev = ''
        count = 1
        for j in pixels:
            if prev == '':
                prev = j
            elif prev == j:
                count += 1
            else:
                res.append((prev, count))
                prev = j
                count = 1
        if count != 1:
            res.append((prev, count))
        return res

    def huffman(self, pixels):
        h = []
        for ch, freq in Counter(pixels).items():
            h.append((freq, len(h), Leaf(ch)))
        heapq.heapify(h)
        count = 0
        while len(h) > 1:
            freq1, _count1, left = heapq.heappop(h)
            freq2, _count2, right = heapq.heappop(h)
            heapq.heappush(h, (freq1 + freq2, count, Node(left, right)))
            count += 1
        [(_freq, _count, root)] = h
        code = {}
        root.walk(code, "")
        res = {'dict': code,
               'content': "".join(code[ch] for ch in pixels)}
        return res
