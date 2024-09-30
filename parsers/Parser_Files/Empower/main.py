import empower

path = 'Data\LAIR1_HexaVariants_032823.pdf'

chrom = empower.Chromatography(path)


print(chrom.getSampleInfo())
print(chrom.getChannelInfo())
print(chrom.getImages())
print(chrom.getAllData())
print(chrom.numberOfSamples())