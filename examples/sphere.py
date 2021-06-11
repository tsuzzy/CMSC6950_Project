from capytaine import *
import logging

logging.basicConfig(level=logging.DEBUG)

# Adding a new floating body
sphere = Sphere(radius=1.0, center=(0, 0, -2), name="my_sphere")
sphere.show()