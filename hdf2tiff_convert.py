import gdal
import os

## List input raster files
os.chdir("C:/Users/Nazia/research_ntl/PR")
rasterFiles = os.listdir(os.getcwd())
#print(rasterFiles)

## Open HDF file
for i in range(0,341):
    
    #Get File Name Prefix
    rasterFilePre = rasterFiles[i][:-3]
    print(rasterFilePre)

    fileExtension = "_BBOX.tif"
    hdflayer = gdal.Open(rasterFiles[i], gdal.GA_ReadOnly)

    #print (hdflayer.GetSubDatasets())

    # Open raster layer
    #hdflayer.GetSubDatasets()[0][0] - for first layer  
    #hdflayer.GetSubDatasets()[1][0] - for second layer ...etc
    for j in range(6):
        subhdflayer = hdflayer.GetSubDatasets()[j][0]
        rlayer = gdal.Open(subhdflayer, gdal.GA_ReadOnly)
        #outputName = rlayer.GetMetadata_Dict()['long_name']

        #Subset the Long Name
        outputName = subhdflayer[100:]

        outputNameNoSpace = outputName.strip().replace(" ","_").replace("/","_")
        outputNameFinal = rasterFilePre + fileExtension
        print(outputNameFinal)

        outputFolder = "C:/Users/Nazia/research_ntl/PR2/"
        outputRaster = outputFolder + outputNameFinal

        #collect bounding box coordinates
        HorizontalTileNumber = int(rlayer.GetMetadata_Dict()["HorizontalTileNumber"])
        VerticalTileNumber = int(rlayer.GetMetadata_Dict()["VerticalTileNumber"])
            
        WestBoundCoord = (10*HorizontalTileNumber) - 180
        NorthBoundCoord = 90-(10*VerticalTileNumber)
        EastBoundCoord = WestBoundCoord + 10
        SouthBoundCoord = NorthBoundCoord - 10

        EPSG = "-a_srs EPSG:4326" #WGS84

        translateOptionText = EPSG+" -a_ullr " + str(WestBoundCoord) + " " + str(NorthBoundCoord) + " " + str(EastBoundCoord) + " " + str(SouthBoundCoord)

        translateoptions = gdal.TranslateOptions(gdal.ParseCommandLine(translateOptionText))
        gdal.Translate(outputRaster,rlayer, options=translateoptions)

        #Display image in QGIS (run it within QGIS python Console) - remove comment to display
        #iface.addRasterLayer(outputRaster, outputNameFinal)