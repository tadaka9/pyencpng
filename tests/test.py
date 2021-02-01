from encpng import EncPNG
enc = EncPNG("rubenkuori", "Password")
# Image passed as bytes
img = enc.encrypt()
result = enc.decrypt(img)
