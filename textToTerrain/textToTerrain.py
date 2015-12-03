# script by PLATVORM
# 2015-12-03

import rhinoscriptsyntax as rs
import math
import random
from System.Drawing import Color

layer = rs.AddLayer("terrainPoints")

textObjects = rs.GetObjects("select text objects", 512, False, True)

for id in textObjects:
    print id
    print rs.TextObjectPoint(id)
    print rs.TextObjectText(id)

    x = rs.TextObjectPoint(id)[0]
    y = rs.TextObjectPoint(id)[1]
    z = float(rs.TextObjectText(id)) * 1

    point = (x, y, z)
    print point

    pointId = rs.AddPoint(point)
    rs.ObjectLayer(pointId, "terrainPoints")

print "done"