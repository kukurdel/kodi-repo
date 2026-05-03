import os
import hashlib
import xml.etree.ElementTree as ET
import zipfile

ADDONS_DIR = "addons"
ZIPS_DIR = "zips"
REPO_DIR = "repo"

os.makedirs(ZIPS_DIR, exist_ok=True)
os.makedirs(REPO_DIR, exist_ok=True)

addons_xml = ET.Element("addons")

for addon in os.listdir(ADDONS_DIR):
    addon_path = os.path.join(ADDONS_DIR, addon)
    
    if os.path.isdir(addon_path):
        xml_file = os.path.join(addon_path, "addon.xml")
        
        if os.path.exists(xml_file):
            tree = ET.parse(xml_file)
            root = tree.getroot()
            addons_xml.append(root)

            version = root.attrib.get("version", "1.0.0")
            zip_name = f"{addon}-{version}.zip"
            zip_path = os.path.join(ZIPS_DIR, zip_name)

            with zipfile.ZipFile(zip_path, 'w') as z:
                for root_dir, dirs, files in os.walk(addon_path):
                    for file in files:
                        full_path = os.path.join(root_dir, file)
                        rel_path = os.path.relpath(full_path, ADDONS_DIR)
                        z.write(full_path, rel_path)

tree = ET.ElementTree(addons_xml)
addons_xml_path = os.path.join(REPO_DIR, "addons.xml")
tree.write(addons_xml_path, encoding="utf-8", xml_declaration=True)

# md5
with open(addons_xml_path, 'rb') as f:
    md5 = hashlib.md5(f.read()).hexdigest()

with open(addons_xml_path + ".md5", 'w') as f:
    f.write(md5)

print("Repo built successfully!")
