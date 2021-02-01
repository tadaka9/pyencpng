from encpng import EncPNG
enc = EncPNG("Ko n ni chi ka!", "Password ][!")
# Image passed as bytes
img = enc.encrypt()
result = enc.decrypt(img)
