# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "Surface Psycho",
    "author": "Romain Guimbal",
    "version": (0, 1),
    "blender": (3, 6, 0),
    "description": "Surface design for the mechanical industry",
    #"warning": "Alpha",
    "doc_url": "",
    "category": "3D View",
    "location": "View3D > Add > Surface  |  View3D > N Panel > Edit"
}

import bpy
import sys
import numpy as np

from os.path import dirname, abspath, exists

file_dirname = dirname(__file__)
if file_dirname not in sys.path:
    sys.path.append(file_dirname)

from OCC.Core.Geom import Geom_BezierSurface, Geom_BSplineSurface
from OCC.Core.gp import gp_Pnt
from OCC.Core.TColGeom import TColGeom_Array2OfBezierSurface
from OCC.Core.TColgp import TColgp_Array2OfPnt
from OCC.Core.GeomConvert import GeomConvert_CompBezierSurfacesToBSplineSurface



def new_bezier_surface(points):
    controlPoints = TColgp_Array2OfPnt(1, 4, 1, 4)
    for i in range(4):
        for j in range(4):
            id= 4*i+j
            controlPoints.SetValue(i+1, j+1, gp_Pnt(points[id][0], points[id][1], points[id][2]))

    BZ1 = Geom_BezierSurface(controlPoints)

    bezierarray = TColGeom_Array2OfBezierSurface(1, 1, 1, 1)
    bezierarray.SetValue(1, 1, BZ1)
    
    BB = GeomConvert_CompBezierSurfacesToBSplineSurface(bezierarray)
    if BB.IsDone():
        poles = BB.Poles().Array2()
        uknots = BB.UKnots().Array1()
        vknots = BB.VKnots().Array1()
        umult = BB.UMultiplicities().Array1()
        vmult = BB.VMultiplicities().Array1()
        udeg = BB.UDegree()
        vdeg = BB.VDegree()

        BSPLSURF = Geom_BSplineSurface( poles, uknots, vknots, umult, vmult, udeg, vdeg, False, False )
        return BSPLSURF


def get_GN_bezierSurf_controlPoints_Coords(o, context):
    try :
        ob = o.evaluated_get(context.evaluated_depsgraph_get())
        me = ob.data
        coords = np.empty(3 * len(me.attributes['handle_co'].data))
        me.attributes['handle_co'].data.foreach_get("vector", coords)
        points = coords[0:16*3].reshape((-1, 3))
    except KeyError:
        return None
    
    return points
                

addonpath = dirname(abspath(__file__)) # The PsychoPath ;)
filepath = addonpath + "/assets/assets.blend"


def append_object_by_name(obj_name, context):
    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        data_to.objects = [name for name in data_from.objects if name==obj_name]


    cursor_loc = context.scene.cursor.location

    for o in data_to.objects:
        if o is not None:
            if context.mode != 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            context.collection.objects.link(o)
            o.location = cursor_loc
            o.asset_clear()
            o.select_set(True)
            bpy.context.view_layer.objects.active = o







##############################
##       OPERTATORS         ##
##############################

from OCC.Extend.DataExchange import write_step_file
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_Sewing
from OCC.Core.TopoDS import TopoDS_Shape #, TopoDS_Compound
# from OCC.Core.BRep import BRep_Builder
from datetime import datetime

class SP_OT_test(bpy.types.Operator):
    bl_idname = "sp.test"
    bl_label = "Add Mesh Object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return {'FINISHED'}
    
class SP_OT_quick_export(bpy.types.Operator):
    bl_idname = "sp.quick_export"
    bl_label = "Add Mesh Object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        aShape = TopoDS_Shape()
        aSew = BRepBuilderAPI_Sewing(1e-1)
        
        for o in context.selected_objects:
            try :
                points = get_GN_bezierSurf_controlPoints_Coords(o, context)
            except KeyError:
                self.report({'ERROR'}, "Select only SP surfaces")
                return {'FINISHED'}
            
            #unit correction
            points *= 1000

            bsurf = new_bezier_surface(points)
            face = BRepBuilderAPI_MakeFace(bsurf, 1e-6).Face()
            aSew.Add(face)
            
            # mirrors (do not support rotations of mirror object)
            for m in o.modifiers :
                if m.type == 'MIRROR':
                    # /!\ Doesn't supports multiple mirror axis yet
                    for j in range(2):
                        if m.use_axis[j]:
                            mirror_vect = [1-2*(j==0), 1-2*(j==1), 1-2*(j==2)]
                            if m.mirror_object==None:
                                mirror_offset = o.location*1000
                            else :
                                mirror_offset = m.mirror_object.location*1000
                            bsurf = new_bezier_surface((points - mirror_offset)*mirror_vect + mirror_offset)
                            face = BRepBuilderAPI_MakeFace(bsurf, 1e-6).Face()
                            aSew.Add(face)

        aSew.SetNonManifoldMode(True)
        aSew.Perform()
        aShape = aSew.SewedShape()

        pathstr = bpy.path.abspath("//") + str(datetime.today())[:-7]
        
        write_step_file(aShape, f"{pathstr}.step", application_protocol="AP203")
        self.report({'INFO'}, f"Step file exported as {pathstr}.step")
        return {'FINISHED'}

class SP_OT_add_bicubic_patch(bpy.types.Operator):
    bl_idname = "sp.add_bicubic_patch"
    bl_label = "Add Bicubic PsychoPatch"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        append_object_by_name("PsychoPatch", context)
        return {'FINISHED'}
    
class SP_OT_add_biquadratic_patch(bpy.types.Operator):
    bl_idname = "sp.add_biquadratic_patch"
    bl_label = "Add Biquadratic PsychoPatch"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        append_object_by_name("PsychoPatch Quadratic", context)
        return {'FINISHED'}

class SP_OT_add_cubic_curve(bpy.types.Operator):
    bl_idname = "sp.add_cubic_curve"
    bl_label = "Add Cubic PsychoCurve"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        append_object_by_name("PsychoCurve", context)
        return {'FINISHED'}

class SP_OT_add_curvatures_probe(bpy.types.Operator):
    bl_idname = "sp.add_curvatures_probe"
    bl_label = "Add Curvatures Probe"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        append_object_by_name("SP - Curvatures Probe", context)
        return {'FINISHED'}

class SP_OT_add_library(bpy.types.Operator):
    bl_idname = "sp.add_library"
    bl_label = "Add Library"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        asset_lib_path = dirname(abspath(__file__))
        paths = [a.path for a in bpy.context.preferences.filepaths.asset_libraries]
        if asset_lib_path not in paths :
            bpy.ops.preferences.asset_library_add(directory=asset_lib_path)
        return {'FINISHED'}

class SP_OT_psychopatch_to_bl_nurbs(bpy.types.Operator):
    bl_idname = "sp.psychopatch_to_bl_nurbs"
    bl_label = "Convert Psychopatches to internal NURBS"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        i=-1
        for o in context.selected_objects :
            cp=get_GN_bezierSurf_controlPoints_Coords(o, context)
            if cp is not None :
                bpy.ops.surface.primitive_nurbs_surface_surface_add(enter_editmode=True, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
                i+=1
                spline=context.active_object.data.splines[i]
                spline.use_endpoint_u = True
                spline.use_endpoint_v = True
                spline.order_u = 4
                spline.order_v = 4
                
                # set CP of spline 
                for j,p in enumerate(spline.points): 
                    p.co = (cp[j][0], cp[j][1], cp[j][2], 1)
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}



#TODO : nurbs to SP :  cp = [p.co for p in o.data.splines[0].points]




##############################
##          VIEW            ##
##############################

class SP_PT_MainPanel(bpy.types.Panel):
    bl_label = "Surface Psycho"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Edit"
    
    def draw(self, context):
        """panel layout"""
        row = self.layout.row()
        row.operator("sp.quick_export", text="Quick export as .STEP")
        row = self.layout.row()
        row.operator("sp.add_curvatures_probe", text="Add Curvatures Probe")
        row = self.layout.row()
        row.operator("sp.psychopatch_to_bl_nurbs", text="Convert to internal NURBS")


class SP_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.operator("sp.add_library", text="Add Assets Path")

def menu_surface(self, context):
    self.layout.separator()
    if context.mode == 'OBJECT':
        self.layout.operator("sp.add_bicubic_patch", text="Bicubic PsychoPatch", icon="SURFACE_NSURFACE")
        self.layout.operator("sp.add_biquadratic_patch", text="Biquadratic PsychoPatch", icon="SURFACE_NSURFACE")

def menu_curve(self, context):
    self.layout.separator()
    if context.mode == 'OBJECT':
        self.layout.operator("sp.add_cubic_curve", text="Cubic PsychoCurve", icon="CURVE_BEZCURVE")



classes = (
    SP_OT_quick_export,
    SP_PT_MainPanel,
    SP_OT_test,
    SP_OT_add_bicubic_patch,
    SP_OT_add_biquadratic_patch,
    SP_OT_add_cubic_curve,
    SP_OT_add_curvatures_probe,
    SP_OT_add_library,
    SP_AddonPreferences,
    SP_OT_psychopatch_to_bl_nurbs,
)

def register():    
    for c in classes:
        bpy.utils.register_class(c)
    # bpy.utils.register_class(SP_OT_add_library)
    bpy.types.VIEW3D_MT_surface_add.append(menu_surface)
    bpy.types.VIEW3D_MT_curve_add.append(menu_curve)
    

def unregister():
    for c in classes[::-1]:
        bpy.utils.unregister_class(c)
    bpy.types.VIEW3D_MT_surface_add.remove(menu_surface)
    bpy.types.VIEW3D_MT_curve_add.remove(menu_curve)

if __name__ == "__main__":
    register()