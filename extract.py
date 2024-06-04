import re

data = '''
<font size="28">SrtCnt : 31, DiffTime : 34ms
2024-03-03 11:19:10.302
[iso : 3200] [shutter : 1/8000.0] [fnum : 170] [ev : -1.3] [ct : 5117] [color_md : default] [focal_len : 240] [dzoom_ratio: 10000, delta:0],[latitude: 64.087525] [longitude: -22.005898] [rel_alt: 19.200 abs_alt: 26.264] </font>
'''

# Removing HTML tags for cleaner text processing
clean_text = re.sub(r'<[^>]+>', '', data)

# Extracting the numbers for specific keys
latitude = re.search(r'latitude: ([\d\.\-]+)', clean_text)
longitude = re.search(r'longitude: ([\d\.\-]+)', clean_text)
rel_alt = re.search(r'rel_alt: ([\d\.\-]+)', clean_text)
abs_alt = re.search(r'abs_alt: ([\d\.\-]+)', clean_text)

# Print the extracted values, ensuring they are found before attempting to access the group
print("Latitude:", latitude.group(1) if latitude else "Not found")
print("Longitude:", longitude.group(1) if longitude else "Not found")
print("Relative Altitude:", rel_alt.group(1) if rel_alt else "Not found")
print("Absolute Altitude:", abs_alt.group(1) if abs_alt else "Not found")
