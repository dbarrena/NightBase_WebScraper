from collections import OrderedDict

artists = OrderedDict()

lineup = ["Optimo",
          " (",
          "Optimo",
          " music)",
          "\n",
          "Paranoid London",
          " (dj set)",
          "\n",
          "Capablanca",
          " (discoscapablanca)",
          "\n",
          "Sebastian Voigt",
          " (renate, outcast oddity)",
          "\n",
          "ZK Bucket",
          " (outcast oddity)",
          "\n",
          "Engyn",
          " (outcast oddity)"]

temp_label = None

for artist in lineup:

    # Is Label
    if "(" in artist and ")" in artist:
        last_key = list(artists.keys())[-1]
        label = {last_key: artist}
        artists.update(label)
        continue

    if artist == "\n" or artist.isspace():
        continue

    if temp_label:
        print(temp_label)
        if ")" in artist:
            temp_label += artist
            last_key = list(artists.keys())[-1]
            label = {last_key: temp_label}
            artists.update(label)
            temp_label = None
            continue
        else:
            temp_label += artist
            continue
    else:
        if "(" in artist:
            temp_label = artist
            continue

    artists[artist] = ""

print(artists)
