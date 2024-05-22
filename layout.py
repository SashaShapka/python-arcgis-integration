import arcpy
import os
# def MakeRec_LL(llx, lly, w, h):
#     xyRecList = [[llx, lly], [llx, lly+h], [llx+w,lly+h], [llx+w,lly], [llx,lly]]
#     array = arcpy.Array([arcpy.Point(*coords) for coords in xyRecList])
#     rec = arcpy.Polygon(array)
#     return rec
#
#
# aprx = arcpy.mp.ArcGISProject(r"D:\deep_leatning_project\MyProject1\MyProject1.aprx")
# layer_file = r"D:\deep_leatning_project\MyProject1\park.lyrx"
# layer = arcpy.mp.LayerFile(layer_file)
# layout = aprx.createLayout(8.5, 11, 'INCH')
# map = aprx.listMaps()[0]
# map.addLayer(layer, "TOP")
# mf = layout.createMapFrame(MakeRec_LL(0.5, 5.5, 7.5, 5), map, "PAGE_LAYOUT")
# title = aprx.listStyleItems('ArcGIS 2D', 'TEXT')[0]
# title.text = "Карта"

# output_path = r'D:\deep_leatning_project\MyProject1'
#
# layout.exportToPDF(os.path.join(output_path, "NAME" + '_small.pdf'), 500,
#                 image_quality=1,
#                 output_as_image=True)



def create_layout():
    # CAUTION - this script will remove any existing guides

    p = arcpy.mp.ArcGISProject('CURRENT')

    for lyt in p.listLayouts():
        lyt_cim = lyt.getDefinition('V3')

        newGuides = []

        # Bottom horizontal guide
        botHorz = arcpy.cim.CreateCIMObjectFromClassName('CIMGuide', 'V3')
        botHorz.position = 0.5
        botHorz.orientation = 'Horizontal'
        newGuides.append(botHorz)

        # Top horizontal guide
        topHorz = arcpy.cim.CreateCIMObjectFromClassName('CIMGuide', 'V3')
        topHorz.position = lyt.pageHeight - 0.5
        topHorz.orientation = 'Horizontal'
        newGuides.append(topHorz)

        # Left vertical guide
        leftVert = arcpy.cim.CreateCIMObjectFromClassName('CIMGuide', 'V3')
        leftVert.position = 0.5
        leftVert.orientation = 'Vertical'
        newGuides.append(leftVert)

        # Right vertical guide
        rightVert = arcpy.cim.CreateCIMObjectFromClassName('CIMGuide', 'V3')
        rightVert.position = lyt.pageWidth - 0.5
        rightVert.orientation = 'Vertical'
        newGuides.append(rightVert)

        # Add guides and make sure they are turned on
        lyt_cim.page.guides = newGuides
        lyt_cim.page.showGuides = True

        # Set back to layer
        lyt.setDefinition(lyt_cim)




aprx = arcpy.mp.ArcGISProject(r"D:\deep_leatning_project\MyProject1\MyProject1.aprx")
m = aprx.listMaps('Map')[0]
lyr = m.listLayers('park')[0]
layout = aprx.listLayouts('Layout')[0]
mf = layout.listElements('mapframe_element', 'Map Frame')[0]
arcpy.SelectLayerByAttribute_management(lyr, 'NEW_SELECTION')
mf.zoomToAllLayers(True)
mf.exportToPDF(r'D:\deep_leatning_project\MyProject1\Selection.pdf', 500, image_quality=1, output_as_image=True)
arcpy.SelectLayerByAttribute_management(lyr, 'CLEAR_SELECTION')