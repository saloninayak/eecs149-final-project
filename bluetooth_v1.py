import bluetooth_v0

# Look for devices in the range
nearby_devices = bluetooth_v0.discover_devices(lookup_names=True, lookup_uuids=True, lookup_oui=True)

print("Found {} devices.".format(len(nearby_devices)))

for addr, name in nearby_devices:
    print(f"Device found: {name} ({addr})")
