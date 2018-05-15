import os

module_names = open("grass_modules_names.txt", "r").read()

list_modules = module_names.split()

file_names_under = module_names.replace('.', '_')
file_names = file_names_under.split()

print list_modules
print file_names

with open(os.path.join("C:\Users", "radek", "Desktop", "generate_xml.bat"), 'w') as file:
    file.write('@ECHO ON\n')
    for name, file_name in zip(list_modules,file_names):
        file.write('{} --interface-description > C:\Users\\radek\Desktop\XML_grass\{}.xml\n'.format(name, file_name))


# r.univar --interface-description > C:\Users\radek\Desktop\r_univar.txt
