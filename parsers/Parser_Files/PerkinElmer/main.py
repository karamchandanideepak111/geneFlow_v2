from perkinelmer import Dropsense96, Envisionxcite

dropsense_1 = Dropsense96(file_path='Data\DropsenseExampleInput1.xlsx')

print(dropsense_1.get_info())
print(dropsense_1.get_plateNum())
print(dropsense_1.get_plateId())
print(dropsense_1.get_plateInfo(plateId='DropPlate 2'))
print(dropsense_1.get_allPlateInfo())


print("-"*50)

envision_1 = Envisionxcite(file_path='Data\input_file.txt')

print(envision_1.get_plateInfo())
print(envision_1.get_backgound())
print(envision_1.get_allPlateInfo())
print(envision_1.get_basicAssayInfo())
print(envision_1.get_protocolInfo())
print(envision_1.get_plateTypeInfo())
print(envision_1.get_autoExportParaInfo())
print(envision_1.get_operationInfo())
print(envision_1.get_labelInfo())
print(envision_1.get_filterInfo())
print(envision_1.get_mirrorModuleInfo())
print(envision_1.get_instrumentInfo())
