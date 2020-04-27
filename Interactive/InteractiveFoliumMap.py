import folium

locations = [
    ["H26", "LapUp", 38.291969, 21.788156],
    ["H27", "Arirtis", 38.284469, 21.765306],
    ["H28", "Zakynthou", 38.259222, 21.746347],
    ["H31", "Gounari", 38.244875, 21.731675],
    ["H32", "Fintiou", 38.234419, 21.735664],
    ["H29", "Isaiou", 38.225647, 21.733011],
    ["H52", "Dimaion", 38.211322, 21.716844],
    ["H53", "Mintilogli", 38.186581, 21.706458]
]

map = folium.Map(location=[38.234419, 21.735664], zoom_start=12,
                 tiles="OpenStreetMap")
for point in locations:
    alias = point[1]
    lat = point[2]
    lon = point[3]
    map.add_child(folium.Marker([lat,lon], popup=alias))

map.save('FoliumMap1.html')
