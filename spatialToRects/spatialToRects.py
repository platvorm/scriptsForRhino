# Script written by Platvorm on 2014-10-11
# Update on 2015-08-24
# -RunPythonScript programToRects.py

import rhinoscriptsyntax as rs
import math
import random
from System.Drawing import Color


# select a file to open
filename = rs.OpenFileName("Open CSV file", "*.csv|", None, None, None)

# open the file for reading
file = open(filename, 'r')
lines = file.readlines()
file.close()

# delete the first line because it's a header
del lines[0]

# print to check the data
# print(lines)

heightSet = rs.GetInteger("Set room height in meters. 0 makes everything square.", 0, 0)
heightSet = heightSet * 1000

plane = rs.WorldXYPlane()

pointOrigin = (0,0,0)
totalWidth = 0
margin = 1000
textSize = 300

rooms = {}

for line in lines:
	# remove the \n
	line = line.strip()

	# split the line by the separating char
	data = line.split(';')

	roomGroup = data[0].decode("utf-8")
	print roomGroup

	roomName = data[1].decode("utf-8")
	print roomName

	count = int(data[2])
	print count

	roomSizeMeters = float(data[3])
	print roomSizeMeters

	info = data[4].decode("utf-8")
	print info

	for c in range(0, count):
		room = { 'group': roomGroup, 'name': roomName, 'sizeMeters': roomSizeMeters, 'info': info }
		rooms[len(rooms)] = room

# create layer
mainLayer = rs.AddLayer("Program")

for key, room in rooms.iteritems():
	print key
	print room

	rooms[key]['size'] = room['sizeMeters'] * 1000 * 1000		# millimeters

	# square is height is 0 else by height
	if heightSet == 0:
		roomWidth = roomHeight = math.sqrt(room['size'])
		print roomWidth
	else:
		roomHeight = heightSet
		roomWidth = room['size'] / roomHeight

	# draw rectange
	# rs.AddRectangle(plane, width, height)
	roomId = rs.AddRectangle(plane, roomWidth, roomHeight)

	# move rectangle to position
	pointToDraw = (totalWidth, 0, 0)
	vectorToDraw = rs.VectorCreate(pointToDraw, pointOrigin)

	rs.MoveObject(roomId, vectorToDraw)

	# set additional data
	# rs.SetUserText(roomId, "Name", room['name'], True)

	# set annotations
	# roomData = rs.AddTextDot(roomName, (totalWidth + roomWidth / 2, roomHeight / 2, 0))
	dataGroup = rs.AddText(room['group'], (totalWidth + textSize, roomHeight - textSize * 2, 0), height = textSize, font = "Arial", font_style = 0, justification = None)
	dataName = rs.AddText(room['name'], (totalWidth + textSize, roomHeight - textSize * 3.5, 0), height = textSize, font = "Arial", font_style = 0, justification = None)
	dataSize = rs.AddText(str(room['sizeMeters']) + " M2", (totalWidth + textSize, roomHeight - textSize * 5, 0), height = textSize, font = "Arial", font_style = 0, justification = None)

	# group
	group = rs.AddGroup()
	rs.AddObjectsToGroup([ roomId, dataGroup, dataName, dataSize ], group)

	# group layers
	if rs.IsLayer(room['group']) and rs.IsLayerChildOf(room['group'], "Program"):
		print "The layer exists."
	else:
		print "The layer does not exist."
		rs.AddLayer(room['group'], parent = "Program")

	# text layer
	textLayerName = room['group'] + " texts"
	if rs.IsLayer(textLayerName) and rs.IsLayerChildOf(textLayerName, room['group']):
		print "The layer exists."
	else:
		print "The layer does not exist."
		rs.AddLayer(textLayerName, parent = room['group'])

	rs.ObjectLayer(roomId, room['group'])
	rs.ObjectLayer(dataGroup, textLayerName)
	rs.ObjectLayer(dataName, textLayerName)
	rs.ObjectLayer(dataSize, textLayerName)

	# set x point for next rectangle
	totalWidth = totalWidth + margin + roomWidth

# color layers
children = rs.LayerChildren("Program")

if children:
    for child in children:
    	rs.LayerColor(child, Color.FromArgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
