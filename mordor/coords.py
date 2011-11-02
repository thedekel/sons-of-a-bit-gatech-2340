import math

MILE_PIXEL_RATIO = 1.16
LOC_DIST = 6.25

SEGMENTS = { 
0 : ((408,328),(451,318)),
6 : ((451,318),(524,333)),
16 : ((524,333),(526,409)),
26 : ((526,409),(585,478)),
39 : ((585,478),(664,679)),
69 : ((664,679),(707,686)),
75 : ((707,686),(793,746)),
89 : ((793,746),(900,808)),
106 : ((900,808),(1033,838)),
125 : ((1033,838),(1066,834)),
}


def get_player_coords(position):
	segment = None
	if position < 0:
		return None
	elif position < 6:
		segment = 0
	elif position < 16:
		segment = 6
	elif position < 26:
		segment = 16
	elif position < 39:
		segment = 26
	elif position < 69:
		segment = 39
	elif position < 75:
		segment = 69
	elif position < 89:
		segment = 75
	elif position < 106:
		segment = 89
	elif position < 125:
		segment = 106
	else:
		segment = 125
	
	segment_line = SEGMENTS[segment]
	
	difference = position - segment
	pixel_difference = difference * LOC_DIST * MILE_PIXEL_RATIO

	p1 = segment_line[0]
	p2 = segment_line[1]
	percent = pixel_difference / distance(p1[0],p1[1],p2[0],p2[1])

	x = (abs((p1[0] - p2[0]))*percent) + p1[0]
	y = (abs((p1[1] - p2[1]))*percent) + p1[1]
	
	return (int(x),int(y))


def distance(x1, y1, x2, y2):
	return (math.sqrt((x2-x1)**2 + (y2-y1)**2))

