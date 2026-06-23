# Priority Agent

north_congestion = 8
south_congestion = 4

north_emission = 12
south_emission = 5

north_score = north_congestion + north_emission
south_score = south_congestion + south_emission

print("\nPriority Agent")
print("-------------------")
print("North Score =", north_score)
print("South Score =", south_score)

if north_score > south_score:
    print("\nPRIORITIZE NORTH")
else:
    print("\nPRIORITIZE SOUTH")