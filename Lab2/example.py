from main import Image, Core

i = Image('dog.pgm')
c = Core('core.txt')

i.make_filter(c)

i.save_image('save.pgm')