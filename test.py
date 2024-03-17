from PIL import Image
from root.settings import MEDIA_ROOT

img = Image.open(MEDIA_ROOT + "/product-images/Screenshot_from_2024-03-17_09-29-07.png")
img.show()
