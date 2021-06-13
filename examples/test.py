from os import name
import capytaine as cpt
import logging

logging.basicConfig(level=logging.WARNING)

body = cpt.FloatingBody.from_file("t13_data.msh", file_format="msh", name="unit")

body.show()