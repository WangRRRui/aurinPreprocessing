import json
file = open("test.json")
data = ""
while True:
    line = file.readline()
    if not line:
        break
    data += line

cellTotDict = dict()
cellNotEngDict = dict()

originalJson = json.loads(data)
for i in originalJson["features"]:
    properties = i["properties"]
    tot = properties["person_tot_tot"] - properties["person_lang_spkn_home_notstated_tot"]
    """
    eng_only = properties["person_tot_spks_eng_only"]
    eng_and_else = properties["person_spks_oth_lang_tot"]
    """
    eng_else_only = properties["person_spks_oth_lang_tot"]

    geo = i["geometry"]
    points = geo["coordinates"][0][0]
    xTotal = 0
    yTotal = 0
    for p in points:
        xTotal += p[0]
        yTotal += p[1]
    "print({'type': 'Point', 'coordinates': [xTotal / len(points), yTotal / len(points)]})"
    pointX = round(xTotal / len(points))
    pointY = round(yTotal / len(points))
    if pointX in cellTotDict:
        if pointY in cellTotDict[pointX]:
            cellTotDict[pointX][pointY] += tot
            cellNotEngDict[pointX][pointY] += eng_else_only
        else:
            cellTotDict[pointX][pointY] = tot
            cellNotEngDict[pointX][pointY] = eng_else_only
    else:
        cellTotDict[pointX] = dict()
        cellNotEngDict[pointX] = dict()
        cellTotDict[pointX][pointY] = tot
        cellNotEngDict[pointX][pointY] = eng_else_only
    """i["geometry"] = {'type': 'Point', 'coordinates': [xTotal / len(points), yTotal / len(points)]}"""



features = list()
for pointX in cellTotDict:
    for pointY in cellTotDict[pointX]:
        if cellTotDict[pointX][pointY] < 100:
            continue
        features.append(
            {
                "type": "Feature",
                "geometry" : {
                    "type": "Point",
                    "coordinates": [pointX, pointY]
                    },
                "properties" : {"ratio": cellNotEngDict[pointX][pointY]/cellTotDict[pointX][pointY]}
            }
        )
        print (cellNotEngDict[pointX][pointY]/cellTotDict[pointX][pointY]*100)

print (len(features))
geojson = {
    "type": "FeatureCollection",
    "features": features
}

with open("output1.geojson","w") as o:
    json.dump(geojson,o)

file = open("aurin.geojson")
data = ""
while True:
    line = file.readline()
    if not line:
        break
    data += line
aurin = json.loads(data)

print(aurin)
