import os
import json

dir = os.getcwd()+"/maps"
strairsCost = 5
elevatorCost = doorCost = 1

mergeData = {
    "floors" : {},
    "places": {},
    "entries": {},
    "graph": {}
}

def entryDecode(code):
    s = code.split("_")
    return s # [0]: id, [1]: level, [2]: floor

def findById(entries, id):
    for entry in entries:
        if entry["id"]==id:
            return entry["code"]

def entryCode(entry, floorId):
    return entry["id"] + "_" + entry["level"] + "_" + floorId

def addToGraph(entries, floorid):
    for curEnt in entries:
        data = {}
        for ent in curEnt["costs"]:
            curCode = findById(entries, ent["id"])
            data[curCode] = ent["cost"]
        
        for ent in mergeData["graph"]:
            curCode = entryDecode(ent)
            id = curCode[0]
            level = curCode[1]
            if (id == curEnt["id"] and abs(int(level)-int(curEnt["level"]))==1 ):
                acost = elevatorCost
                if curEnt["type"]=="stairs":
                    acost = strairsCost

                elif curEnt["type"]=="door":
                    acost = doorCost

                data[ent] = acost
                mergeData["graph"][ent][curEnt["code"]] = acost
        print(data)
        mergeData["graph"][curEnt["code"]] = data



def formPlace(place, floorId):
    return {
        "floorId": floorId,
        "cords": place["cords"],
        "id": place["id"],
    }

def formEntry(entry, floorId):
    return {
        "floorId": floorId,
        "id": entry["id"],
        "level": entry["level"],
        "cords": entry["cords"],
        "type": entry["type"]
    }

def formMapData(mapData):
    floorId = mapData["id"]

    newMapData = mapData.copy()

    newMapData["places"] = {}
    for place in mapData["places"]:
        newMapData["places"][place["id"]] = place
    
    newMapData["entries"] = {}
    for entry in mapData["entries"]:
        newMapData["entries"][entry["code"]] = entry

    mergeData["floors"][floorId] = newMapData

    for place in mapData["places"]:
        mergeData["places"][place["name"]] = formPlace(place, floorId)

    for entry in mapData["entries"]:
        mergeData["entries"][entry["code"]] = formEntry(entry, floorId)

    addToGraph(mapData["entries"], floorId)

for filename in os.listdir(dir):
    curData = {}
    with open(os.path.join(dir, filename), 'r') as f:
        curData = json.load(f)
        formMapData(curData)


with open("mergeData.json", "w") as f:
    json.dump(mergeData, f)


