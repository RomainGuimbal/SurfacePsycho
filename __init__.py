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
    "blender": (4, 0, 0),
    "description": "Surface design for the mechanical industry",
    "warning": "Alpha",
    "doc_url": "",
    "category": "3D View",
    "location": "View3D > Add > Surface  |  View3D > N Panel > Edit"
}

import bpy
import sys
import numpy as np
from mathutils import Vector

from datetime import datetime
from os.path import dirname, abspath, exists

file_dirname = dirname(__file__)
if file_dirname not in sys.path:
    sys.path.append(file_dirname)

from OCC.Core.Geom import Geom_BezierSurface, Geom_BSplineSurface, Geom_BezierCurve, Geom_Plane
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Pln, gp_Trsf, gp_Ax1, gp_Ax2, gp_Vec
from OCC.Core.TColGeom import TColGeom_Array2OfBezierSurface
from OCC.Core.TColgp import TColgp_Array2OfPnt, TColgp_Array1OfPnt
from OCC.Core.GeomAPI import GeomAPI_ProjectPointOnSurf
from OCC.Core.GeomConvert import GeomConvert_CompBezierSurfacesToBSplineSurface
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeEdge, BRepBuilderAPI_Sewing, BRepBuilderAPI_Transform
from OCC.Core.TopTools import TopTools_Array1OfShape
from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Wire #, TopoDS_Compound
from OCC.Extend.DataExchange import write_step_file

addonpath = dirname(abspath(__file__)) # The PsychoPath ;)
filepath = addonpath + "/assets/assets.blend"





##############################
##         FUNCTIONS        ##
##############################

def new_bezier_face(points):
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

        bsurf = Geom_BSplineSurface( poles, uknots, vknots, umult, vmult, udeg, vdeg, False, False )
        face = BRepBuilderAPI_MakeFace(bsurf, 1e-6).Face()
        return face


def get_GN_bezierSurf_controlPoints_Coords(o, context):
    ob = o.evaluated_get(context.evaluated_depsgraph_get())
    me = ob.data
    raw_coords = np.empty(3 * len(me.attributes['handle_co'].data))
    me.attributes['handle_co'].data.foreach_get("vector", raw_coords)
    coords = raw_coords[0:16*3].reshape((-1, 3))
    return coords


def append_object_by_name(obj_name, context):# for importing from the asset file
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


def new_planar_face(o, context):
    # List edges
    ob = o.evaluated_get(context.evaluated_depsgraph_get())
    me = ob.data
    point_count = me.attributes['P_count'].data[0].value

    raw_cp_planar = np.empty(3 * len(me.attributes['CP_planar'].data))
    me.attributes['CP_planar'].data.foreach_get("vector", raw_cp_planar)
    cp_planar = raw_cp_planar.reshape((-1, 3))[0:point_count]
    cp_planar*=1000 #unit correction

    loc, rot, scale = o.matrix_world.decompose()
    loc*=1000
    pl_normal = rot@ Vector([0,0,1])
    pl = gp_Pln(gp_Pnt(loc.x,loc.y,loc.z),gp_Dir(pl_normal.x, pl_normal.y, pl_normal.z))
    gpl = Geom_Plane(pl)

    controlPoints = TColgp_Array1OfPnt(1, point_count)
    for i in range(point_count):
        pnt= gp_Pnt(cp_planar[i][0], cp_planar[i][1], cp_planar[i][2])
        pnt= GeomAPI_ProjectPointOnSurf(pnt, gpl).Point(1)
        controlPoints.SetValue(i+1, pnt)

    edges_list = TopTools_Array1OfShape(1, point_count//3)
    for i in range(point_count//3):
        bezier_segment_CP_array = TColgp_Array1OfPnt(0,3)
        bezier_segment_CP_array.SetValue(0, controlPoints[i*3])
        bezier_segment_CP_array.SetValue(1, controlPoints[(i*3+1)%point_count])
        bezier_segment_CP_array.SetValue(2, controlPoints[(i*3+2)%point_count])
        bezier_segment_CP_array.SetValue(3, controlPoints[(i*3+3)%point_count])
         
        segment = Geom_BezierCurve(bezier_segment_CP_array)
        edge = BRepBuilderAPI_MakeEdge(segment).Edge()
        edges_list.SetValue(i+1, edge)

    makeWire = BRepBuilderAPI_MakeWire()
    for e in edges_list :
        makeWire.Add(e)
    w = TopoDS_Wire()
    w = makeWire.Wire()

    aface = BRepBuilderAPI_MakeFace(w, True).Face()
    return aface

def geom_type_of_object(o, context):
    type = None
    ob = o.evaluated_get(context.evaluated_depsgraph_get())
    if hasattr(ob.data, "attributes") :
        for k in ob.data.attributes.keys() :
            if k == 'handle_co' :
                type = 'bezier_surf'
                break
            if k == 'CP_planar' :
                type = 'planar'
                break
    return type


def mirrors(o, face):
    ms = BRepBuilderAPI_Sewing(1e-1)
    ms.SetNonManifoldMode(True)
    ms.Add(face)
    mshape = TopoDS_Shape()

    ms.Perform()
    shape = ms.SewedShape()
    loc, rot, scale = o.matrix_world.decompose()

    for m in o.modifiers :
        if m.type == 'MIRROR':
            if m.mirror_object==None:
                mirror_offset = loc*1000
            else :
                loc, rot, scale = m.mirror_object.matrix_world.decompose()
                mirror_offset = loc*1000
            
            #Fill configurations array
            configurations = [False]*7

            x = m.use_axis[0]
            y = m.use_axis[1]
            z = m.use_axis[2]

            configurations[0]= x
            configurations[1]= y
            configurations[2]= z
            configurations[3]= x and y and z
            configurations[4]= y and z
            configurations[5]= x and z
            configurations[6]= x and y

            xscales = [ 1, 0, 0, 1, 0, 1, 1]
            yscales = [ 0, 1, 0, 1, 1, 0, 1]
            zscales = [ 0, 0, 1, 1, 1, 1, 0]
            symtype = [x+y+z for x,y,z in zip(xscales,yscales,zscales)]

            for i in range(7):
                if configurations[i]:
                    if symtype[i]==1:#sym planaire
                        base = rot@(Vector([xscales[i],yscales[i],zscales[i]]))
                        atrsf = gp_Trsf()
                        atrsf.SetMirror(gp_Ax2(gp_Pnt(mirror_offset[0], mirror_offset[1], mirror_offset[2]), gp_Dir(base.x, base.y, base.z)))
                    elif symtype[i]==2 :#sym axiale
                        base = rot@(Vector([xscales[i]-1,abs(yscales[i]-1),abs(zscales[i]-1)])) 
                        atrsf = gp_Trsf()
                        atrsf.SetMirror(gp_Ax1(gp_Pnt(mirror_offset[0], mirror_offset[1], mirror_offset[2]), gp_Dir(base.x, base.y, base.z)))
                    else :#sym centrale
                        atrsf = gp_Trsf()
                        atrsf.SetMirror(gp_Pnt(mirror_offset[0], mirror_offset[1], mirror_offset[2]))
                    
                    mshape = BRepBuilderAPI_Transform(shape, atrsf).Shape()
                    # mshape = BRepBuilderAPI_Transform(mshape, trans_trsf).Shape()
                    
                    ms.Add(mshape)
            
            ms.Perform()
            shape = ms.SewedShape()
            
    # ms.Perform()
    shape = ms.SewedShape()
    return shape














##############################
##       OPERTATORS         ##
##############################
    
class SP_OT_quick_export(bpy.types.Operator):
    bl_idname = "sp.quick_export"
    bl_label = "Add Mesh Object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        aShape = TopoDS_Shape()
        aSew = BRepBuilderAPI_Sewing(1e-1)
        
        SPobj_count=0
        
        for o in context.selected_objects:
            gto = geom_type_of_object(o, context)

            if gto == "bezier_surf" :
                SPobj_count +=1

                points = get_GN_bezierSurf_controlPoints_Coords(o, context)
                #unit correction
                points *= 1000
                bf = new_bezier_face(points)
                aSew.Add(bf)
                aSew.Add(mirrors(o, bf))
            elif gto == "planar" :
                SPobj_count +=1
                pf =new_planar_face(o, context)
                aSew.Add(pf)
                aSew.Add(mirrors(o, pf))

        aSew.SetNonManifoldMode(True)
        aSew.Perform()
        aShape = aSew.SewedShape()

        blenddir = bpy.path.abspath("//")
        if blenddir !="":#avoid exporting to root
            dir =  blenddir
        else :
            dir = bpy.context.preferences.filepaths.temporary_directory
        pathstr = dir + str(datetime.today())[:-7].replace('-','').replace(' ','-').replace(':','')

        if SPobj_count>0 :
            write_step_file(aShape, f"{pathstr}.step", application_protocol="AP203")
            self.report({'INFO'}, f"Step file exported as {pathstr}.step")
        else :
            self.report({'INFO'}, 'No SurfacePsycho Objects selected')
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
    
class SP_OT_add_flat_patch(bpy.types.Operator):
    bl_idname = "sp.add_flat_patch"
    bl_label = "Add flat PsychoPatch"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        append_object_by_name("FlatPatch", context)
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
            try:
                cp=get_GN_bezierSurf_controlPoints_Coords(o, context)
            except Exception :
                cp=None
            
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
##          MENUES          ##
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
        self.layout.operator("sp.add_flat_patch", text="Flat patch", icon="SURFACE_NCURVE")

def menu_curve(self, context):
    self.layout.separator()
    if context.mode == 'OBJECT':
        self.layout.operator("sp.add_cubic_curve", text="Cubic PsychoCurve", icon="CURVE_BEZCURVE")













##############################
##         REGISTER         ##
##############################

classes = (
    SP_OT_quick_export,
    SP_PT_MainPanel,
    SP_OT_add_bicubic_patch,
    SP_OT_add_biquadratic_patch,
    SP_OT_add_flat_patch,
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