bl_info = {
	"name": "Eldewrito Prefab Exporter",
	"author": "Weebmaster",
	"version": (1, 0, 1),
	"blender": (2, 80, 0),
	"location": "File > Export > Eldewrito Prefab (.prefab)",
	"description": "Prefab exporter compatible with Eldewrito's forge prefab system ",
	"warning": "Requires OBJ files obtained from Eldewrito to properly display once exported from blender",
	"wiki_url": "",
	"category": "Import-Export",
}
import bpy
import mathutils
from math import radians
import struct
from pathlib import Path


def write_some_data(context, filepath, use_some_setting):
    #TODO: Move dictionart outside of the function and possibly pass it in, so it isnt created everytime the function is called.
    tagDict = {
        "BLOCK [01 x 05 x 05]": "0000015c",
        "BLOCK [01 x 1 x 05]": "00000158",
        "BLOCK [01 x 1 x 1]": "00000148",
        "BLOCK [01 x 2 x 05]": "00000156",
        "BLOCK [01 x 2 x 1]": "0000014c",
        "BLOCK [01 x 2 x 2]": "00000155",
        "BLOCK [01 x 3 x 05]": "0000015a",
        "BLOCK [01 x 3 x 1]": "0000014a",
        "BLOCK [01 x 3 x 2]": "00000154",
        "BLOCK [01 x 3 x 3]": "00000153",
        "BLOCK [01 x 4 x 05]": "00000159",
        "BLOCK [01 x 4 x 1]": "00000149",
        "BLOCK [01 x 4 x 2]": "00000141",
        "BLOCK [01 x 4 x 3]": "00000152",
        "BLOCK [01 x 4 x 4]": "00000151",
        "BLOCK [01 x 5 x 05]": "0000015b",
        "BLOCK [01 x 5 x 1]": "0000014b",
        "BLOCK [01 x 5 x 2]": "0000014f",
        "BLOCK [01 x 5 x 3]": "0000014e",
        "BLOCK [01 x 5 x 4]": "0000014d",
        "BLOCK [01 x 5 x 5]": "00000150",
        "BLOCK [01 x 10 x 05]": "00000157",
        "BLOCK [01 x 10 x 1]": "00000145",
        "BLOCK [01 x 10 x 2]": "00000144",
        "BLOCK [01 x 10 x 3]": "00000143",
        "BLOCK [01 x 10 x 4]": "00000142",
        "BLOCK [01 x 10 x 5]": "00000146",
        "BLOCK [01 x 10 x 10]": "00000147",
        "BLOCK [01 x 20 x 20]": "0000015d",
        "BLOCK [05 x 05 x 05]": "0000012a",
        "BLOCK [05 x 1 x 05]": "0000012b",
        "BLOCK [05 x 1 x 1]": "00000132",
        "BLOCK [05 x 2 x 1]": "00000136",
        "BLOCK [05 x 2 x 2]": "0000013f",
        "BLOCK [05 x 3 x 1]": "00000134",
        "BLOCK [05 x 3 x 2]": "0000013e",
        "BLOCK [05 x 3 x 3]": "0000013d",
        "BLOCK [05 x 4 x 1]": "00000133",
        "BLOCK [05 x 4 x 2]": "00000129",
        "BLOCK [05 x 4 x 3]": "0000013c",
        "BLOCK [05 x 4 x 4]": "0000013b",
        "BLOCK [05 x 5 x 1]": "00000135",
        "BLOCK [05 x 5 x 2]": "00000139",
        "BLOCK [05 x 5 x 3]": "00000138",
        "BLOCK [05 x 5 x 4]": "00000137",
        "BLOCK [05 x 5 x 5]": "0000013a",
        "BLOCK [05 x 10 x 1]": "0000012f",
        "BLOCK [05 x 10 x 2]": "0000012e",
        "BLOCK [05 x 10 x 3]": "0000012d",
        "BLOCK [05 x 10 x 4]": "0000012c",
        "BLOCK [05 x 10 x 5]": "00000130",
        "BLOCK [05 x 10 x 10]": "00000131",
        "BLOCK [05 x 20 x 20]": "00000128",
        "BLOCK [1 x 1 x 1]": "0000011f",
        "BLOCK [1 x 2 x 1]": "0000011b",
        "BLOCK [1 x 2 x 2]": "00000140",
        "BLOCK [1 x 3 x 1]": "0000011d",
        "BLOCK [1 x 3 x 2]": "00000113",
        "BLOCK [1 x 3 x 3]": "00000114",
        "BLOCK [1 x 4 x 1]": "0000011e",
        "BLOCK [1 x 4 x 2]": "00000126",
        "BLOCK [1 x 4 x 3]": "00000115",
        "BLOCK [1 x 4 x 4]": "00000116",
        "BLOCK [1 x 5 x 1]": "0000011c",
        "BLOCK [1 x 5 x 2]": "00000118",
        "BLOCK [1 x 5 x 3]": "00000119",
        "BLOCK [1 x 5 x 4]": "0000011a",
        "BLOCK [1 x 5 x 5]": "00000117",
        "BLOCK [1 x 10 x 1]": "00000122",
        "BLOCK [1 x 10 x 2]": "00000123",
        "BLOCK [1 x 10 x 3]": "00000124",
        "BLOCK [1 x 10 x 4]": "00000125",
        "BLOCK [1 x 10 x 5]": "00000121",
        "BLOCK [1 x 10 x 10]": "00000120",
        "BLOCK [1 x 20 x 20]": "00000127",
        "TRIANGLE [01 x 05 x 05]": "00000163",
        "TRIANGLE [01 x 1 x 1]": "00000164",
        "TRIANGLE [01 x 2 x 2]": "00000162",
        "TRIANGLE [01 x 3 x 3]": "00000161",
        "TRIANGLE [01 x 4 x 4]": "00000160",
        "TRIANGLE [01 x 5 x 5]": "0000015f",
        "TRIANGLE [01 x 10 x 10]": "0000015e",
        "TRIANGLE [05 x 05 x 05]": "00000112",
        "TRIANGLE [05 x 1 x 1]": "0000010b",
        "TRIANGLE [05 x 2 x 2]": "0000010f",
        "TRIANGLE [05 x 3 x 3]": "0000010e",
        "TRIANGLE [05 x 4 x 4]": "0000010d",
        "TRIANGLE [05 x 5 x 5]": "0000010c",
        "TRIANGLE [05 x 10 x 10]": "00000110",
        "TRIANGLE [1 x 05 x 05]": "00000105",
        "TRIANGLE [1 x 1 x 1]": "0000010a",
        "TRIANGLE [1 x 2 x 2]": "00000106",
        "TRIANGLE [1 x 3 x 3]": "00000107",
        "TRIANGLE [1 x 4 x 4]": "00000108",
        "TRIANGLE [1 x 5 x 5]": "00000109",
        "TRIANGLE [1 x 10 x 10]": "00000111",
        "TRIANGLE (EQUAL) [01 x 05 x 043]": "000000f7",
        "TRIANGLE (EQUAL) [01 x 1 x 087]": "000000f5",
        "TRIANGLE (EQUAL) [01 x 2 x 073]": "000000f4",
        "TRIANGLE (EQUAL) [01 x 3 x 06]": "000000f3",
        "TRIANGLE (EQUAL) [01 x 4 x 046]": "000000f2",
        "TRIANGLE (EQUAL) [01 x 5 x 033]": "000000f6",
        "CYLINDER [05 x 05 x 01]": "000000d6",
        "CYLINDER [05 x 05 x 05]": "000000ed",
        "CYLINDER [05 x 05 x 1]": "000000dd",
        "CYLINDER [05 x 05 x 2]": "000000e0",
        "CYLINDER [05 x 05 x 4]": "000000e3",
        "CYLINDER [1 x 1 x 01]": "000000d7",
        "CYLINDER [1 x 1 x 05]": "000000d8",
        "CYLINDER [1 x 1 x 1]": "000000dc",
        "CYLINDER [1 x 1 x 2]": "000000df",
        "CYLINDER [1 x 1 x 4]": "000000e2",
        "CYLINDER [2 x 2 x 01]": "000000d5",
        "CYLINDER [2 x 2 x 05]": "000000d9",
        "CYLINDER [2 x 2 x 1]": "000000db",
        "CYLINDER [2 x 2 x 2]": "000000de",
        "CYLINDER [2 x 2 x 4]": "000000e1",
        "CYLINDER [5 x 5 x 01]": "000000da",
        "CYLINDER [5 x 5 x 05]": "000000ec",
        "CYLINDER [5 x 5 x 1]": "000000eb",
        "CYLINDER [5 x 5 x 2]": "000000ea",
        "CYLINDER [5 x 5 x 4]": "000000e9",
        "CYLINDER [10 x 10 x 01]": "000000e8",
        "CYLINDER [10 x 10 x 05]": "000000e7",
        "CYLINDER [10 x 10 x 1]": "000000e6",
        "CYLINDER [10 x 10 x 2]": "000000e5",
        "CYLINDER [10 x 10 x 4]": "000000e4",
        "CYLINDER (HALF) [05 x 01 x 1]": "000000ef",
        "CYLINDER (HALF) [05 x 01 x 2]": "000000ee",
        "CYLINDER (HALF) [05 x 01 x 3]": "000000f0",
        "CYLINDER (HALF) [05 x 1 x 1]": "00000104",
        "CYLINDER (HALF) [05 x 1 x 2]": "00000101",
        "CYLINDER (HALF) [05 x 1 x 3]": "000000fe",
        "CYLINDER (HALF) [05 x 3 x 1]": "000000f9",
        "CYLINDER (HALF) [05 x 3 x 2]": "00000102",
        "CYLINDER (HALF) [05 x 3 x 3]": "000000ff",
        "CYLINDER (HALF) [05 x 4 x 1]": "000000fa",
        "CYLINDER (HALF) [05 x 4 x 2]": "00000103",
        "CYLINDER (HALF) [05 x 4 x 3]": "00000100",
        "CYLINDER (HALF) [05 x 10 x 1]": "000000fb",
        "CYLINDER (HALF) [05 x 10 x 2]": "000000fc",
        "CYLINDER (HALF) [05 x 10 x 3]": "000000fd",
        "HEMISPHERE [2 x 2 x 01]": "000000b9",
        "HEMISPHERE [2 x 2 x 05]": "000000b8",
        "HEMISPHERE [2 x 2 x 1]": "000000cf",
        "HEMISPHERE [5 x 5 x 025]": "000000bf",
        "HEMISPHERE [5 x 5 x 1]": "000000be",
        "HEMISPHERE [5 x 5 x 2]": "000000bd",
        "HEMISPHERE [10 x 10 x 05]": "000000c5",
        "HEMISPHERE [10 x 10 x 2]": "000000c4",
        "HEMISPHERE [10 x 10 x 5]": "000000c3",
        "HEMISPHERE [20 x 20 x 1]": "000000cb",
        "HEMISPHERE [20 x 20 x 5]": "000000ca",
        "HEMISPHERE [20 x 20 x 10]": "000000c9",
        "HEMISPHERE [1 x 2 x 01]": "000000ba",
        "HEMISPHERE [1 x 2 x 05]": "000000bb",
        "HEMISPHERE [1 x 2 x 1]": "000000bc",
        "HEMISPHERE [2 x 5 x 025]": "000000c0",
        "HEMISPHERE [2 x 5 x 1]": "000000c1",
        "HEMISPHERE [2 x 5 x 2]": "000000c2",
        "HEMISPHERE [5 x 10 x 1]": "000000c6",
        "HEMISPHERE [5 x 10 x 2]": "000000c7",
        "HEMISPHERE [5 x 10 x 5]": "000000c8",
        "HEMISPHERE [10 x 20 x 1]": "000000cc",
        "HEMISPHERE [10 x 20 x 5]": "000000cd",
        "HEMISPHERE [10 x 20 x 10]": "000000ce",
    }
    print("running write_some_data...")
    #Get List of all objects in scene
    objectsList = list(bpy.data.objects)

    f = open(filepath, 'wb')
    objectsList1 = [x for x in objectsList if x.name in tagDict]
    objectsList2 = [x for x in objectsList if x.name[:x.name.rfind('.')] in tagDict]
    objectsList = objectsList1 + objectsList2
    #start obtain variables for header to write to file. 
    #magic, flags, version, date
    magic = bytearray([0x62, 0x66, 0x72, 0x70, 0x00, 0x00, 0x00, 0x00, 0xBE, 0x05, 0x57, 0x5F, 0x00, 0x00, 0x00, 0x00])
    f.write(magic)

    #Take prefab name and convert to binary and write to file.
    prefabname = bytes(Path(filepath).stem, 'utf-8') 
    buff = struct.pack("16s", prefabname)
    f.write(buff)

    #Take username and convert to binary and write to file.
    username = bytes(use_some_setting, 'utf-8')
    buff = struct.pack("16s", username)
    f.write(buff)

    #get number of objects in the scene and write to prefab
    buff = struct.pack('I',len(objectsList))
    f.write(buff)

    #padding between the headder and the objects
    padding = bytearray([0x00, 0x00, 0x00, 0x00])
    f.write(padding)
    
    #properties of object. Left default, so user can change in game.
    properties = bytearray([0xFF, 0x03, 0x0C, 0x08, 0x00, 0x1E, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    for object in objectsList:
        if str(object.name) != 'Camera':

            #obtain filler and tag info
            flags = bytearray([0x00, 0x00, 0x00, 0x00])
            tagIndex= bytearray()
            if object.name.rfind('.') != -1:
                tagIndex = bytearray.fromhex(tagDict[object.name[:object.name.rfind('.')]])
            else:
                tagIndex = bytearray.fromhex(tagDict[object.name])
            
            tagIndex.reverse()
            


            rightVector = mathutils.Vector([1,0,0])
            upVector = mathutils.Vector([0,0,1])
            rightVector.rotate(object.rotation_euler)
            rightVector.normalize()
            upVector.rotate(object.rotation_euler)
            upVector.normalize()


            f.write(flags)
            f.write(tagIndex)
            data = [object.location.x,object.location.y, object.location.z]
            buf = struct.pack('%sf' % len(data), *data)
            f.write(buf)
            data = [rightVector.x,rightVector.y,rightVector.z,upVector.x,upVector.y,upVector.z]
            buf = struct.pack('%sf' % len(data), *data)
            f.write(buf)
            f.write(properties)
    f.close()

    return {'FINISHED'}


# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ExportSomeData(Operator, ExportHelper):
    """Export an Eldewrito prefab file"""
    bl_idname = "export_test.some_data"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export Some Data"

    # ExportHelper mixin class uses this
    filename_ext = ".prefab"

    filter_glob = StringProperty(
            default="*.prefab",
            options={'HIDDEN'},
            maxlen=15,  # Max length of a prefab name to not crash dewrito
            )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    use_setting = StringProperty(
            name="Author Name",
            description="Creator of the prefab",
            default="",
            maxlen=15,
            )

    

    def execute(self, context):
        return write_some_data(context, self.filepath, self.use_setting)


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(ExportSomeData.bl_idname, text="Eldewrito Prefab (.prefab)")


def register():
    bpy.utils.register_class(ExportSomeData)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)



def unregister():
    bpy.utils.unregister_class(ExportSomeData)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.export_test.some_data('INVOKE_DEFAULT')