from main import Image


i = Image('lena.ppm')
i.haar()
i.save_image('save.ppm')