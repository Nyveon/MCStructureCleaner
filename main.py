'''
MC Structure cleaner
By: Nyveon

v: 1.1

Modded structure cleaner for minecraft. Removes all references to non-existent structures to allow for
clean error logs and chunk saving.
'''

# Imports
import anvil    # anvil-parser by matcool
import os       # for file-system
import time     # for progress messages
version = "1.1"

def sep():
    print("----------------------------------")


# User input
sep()
print("MC Structure cleaner\nBy: Nyveon")
print("Version: ", version)
sep()
print("Please type in the EXACT structure tag name you want removed (Use NBTExplorer to find the name)")
to_replace = input("Tag: ") #todo: allow multiple tags
print("Replacing", to_replace, "in all region files.")
sep()

# Create new directory and access regions directory
print("Saving newly generated region files to .\\new_region\\")
try:
    os.mkdir("./new_region")
except:
    print("The folder new_region already exists, this may cause issues!")
ld = os.listdir("./world/region") #todo: add other worlds/dimensions
ldn = len(ld)
print("Region files to process:", ldn)
sep()
counter = 1
removed = 0
previous_removed = 0
last_time = time.time()


# Main parsing loop
for file_name in ld:

    # Current region file
    # todo: allow for picking up progress where it left off in case of termination
    print("Progress: [", counter, "/", ldn,  "] | Processing:", file_name, "| ", end = "")
    coords = file_name.split(".")
    region = anvil.Region.from_file("./world/region/" + file_name)
    new_region = anvil.EmptyRegion(int(coords[1]), int(coords[2]))
    previous_removed = removed

    # Check all possible chunks in the region (32 x 32 area)
    for chunk_x in range(32):
        for chunk_z in range(32):
            if region.chunk_location(chunk_x, chunk_z) != (0, 0):  # Check if chunk exists
                #chunk = region.get_chunk(chunk_x, chunk_z)
                data = region.chunk_data(chunk_x, chunk_z)

                # Remove tag from structure starts
                for tag in data["Level"]["Structures"]["Starts"].tags:
                    if tag.name == to_replace:
                        del data["Level"]["Structures"]["Starts"][tag.name]
                        removed += 1

                # Remove tag from structure references
                for tag in data["Level"]["Structures"]["References"].tags:
                    if tag.name == to_replace:
                        del data["Level"]["Structures"]["References"][tag.name]
                        removed += 1

                # Add the modified chunk data to the new region
                new_region.add_chunk(anvil.Chunk(data))

    # Save generated region file and increment counter
    new_region.save("./new_region/" + file_name)
    counter += 1
    delta_seconds = round((time.time() - last_time) % 60, 2)
    last_time = time.time()
    print(removed - previous_removed, "instances of the tag removed. |", delta_seconds, "seconds taken.")

print("\nDone. Removed", removed, "instances of", to_replace, "in", ldn, "region files.")
print("You can now replace the region folder in your world for the new_region folder.")





