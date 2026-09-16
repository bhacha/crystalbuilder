import crystalbuilder as cb
import logging
import sys

logger = logging.getLogger('crystalbuilder')
logger.setLevel(logging.DEBUG)
loghandler = logging.StreamHandler(sys.stdout)
loghandler.setLevel(logging.DEBUG)
logger.addHandler(loghandler)

if __name__ == "__main__":
    geometry = cb.geometry.Cylinder(center=(0,0,0), radius=1, height=1)
    geo2 = geometry.copy()
    print(geometry)