import re

def parse_encounters(file_path):
    pokemon_data = {}
    current_route = None
    current_rod = None

    rod_images = {
        "OldRod": "[[File:OLDROD.png]]",
        "GoodRod": "[[File:GOODROD.png]]",
        "SuperRod": "[[File:SUPERROD.png]]"
    }

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            route_match = re.match(r"\[(\d+)\] # (.+)", line)
            if route_match:
                current_route = route_match.group(2)
                current_rod = None
                continue

            if line in rod_images:
                current_rod = line
                continue

            if current_rod and line:
                parts = line.split(",")
                if len(parts) >= 2:
                    pokemon_name = parts[1].capitalize()

                    if pokemon_name not in pokemon_data:
                        pokemon_data[pokemon_name] = {
                            "rods": set(),
                            "locations": set()
                        }
                    
                    pokemon_data[pokemon_name]["rods"].add(rod_images[current_rod])
                    pokemon_data[pokemon_name]["locations"].add(current_route)

    return pokemon_data

def save_to_wiki_format(pokemon_data, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("{| class=\"wikitable\"\n")
        file.write("! Pokémon !! Rods !! Locations\n")

        for pokemon, data in pokemon_data.items():
            pokemon_image = f"[[File:{pokemon}.png]] {pokemon}"
            rods = "".join(data["rods"])
            locations = ", ".join(data["locations"])

            file.write(f"|-\n| {pokemon_image} || {rods} || {locations}\n")

        file.write("|}")

file_path = "encounters.txt"
output_file = "fishing_encounters.txt"
pokemon_data = parse_encounters(file_path)
save_to_wiki_format(pokemon_data, output_file)
print("Fishing encounters saved to", output_file)
