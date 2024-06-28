##Copyright 2011-2017 Thomas Paviot (tpaviot@gmail.com)
##
##This file is part of pythonOCC.
##
##pythonOCC is free software: you can redistribute it and/or modify
##it under the terms of the GNU Lesser General Public License as published by
##the Free Software Foundation, either version 3 of the License, or
##(at your option) any later version.
##
##pythonOCC is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU Lesser General Public License for more details.
##
##You should have received a copy of the GNU Lesser General Public License
##along with pythonOCC.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
from string import Template
import tempfile
import uuid
from xml.etree import ElementTree

from OCC.Core.Tesselator import ShapeTesselator
from OCC import VERSION

from OCC.Extend.TopologyUtils import is_edge, is_wire, discretize_edge, discretize_wire
from OCC.Display.WebGl.simple_server import start_server


def spinning_cursor():
    while True:
        yield from "|/-\\"


X3DFILE_HEADER_TEMPLATE = Template(
    """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE X3D PUBLIC "ISO//Web3D//DTD X3D 3.3//EN" "http://www.web3d.org/specifications/x3d-3.3.dtd">
<X3D profile="Immersive" version="3.3" xmlns:xsd="http://www.w3.org/2001/XMLSchema-instance" xsd:noNamespaceSchemaLocation="http://www.web3d.org/specifications/x3d-3.3.xsd">
<head>
    <meta name="generator" content="pythonocc-$VERSION X3D exporter (www.pythonocc.org)"/>
    <meta name="creator" content="pythonocc-$VERSION generator"/>
    <meta name="identifier" content="http://www.pythonocc.org"/>
    <meta name="description" content="pythonocc-$VERSION x3dom based shape rendering"/>
</head>
<Scene>
"""
)

HEADER_TEMPLATE = Template(
    """
<head>
    <title>pythonOCC $VERSION x3dom renderer</title>
    <meta name='Author' content='Thomas Paviot - tpaviot@gmail.com'>
    <meta name='Keywords' content='WebGl,pythonOCC'>
    <meta charset="utf-8">
    <link rel="stylesheet" type="text/css" href="https://x3dom.org/release/x3dom.css">
    <script src="https://x3dom.org/release/x3dom.js"></script>
    <style>
        body {
            background: linear-gradient($bg_gradient_color1, $bg_gradient_color2);
            margin: 0px;
            overflow: hidden;
        }
        #pythonocc_rocks {
            padding: 5px;
            position: absolute;
            left: 1%;
            bottom: 2%;
            height: 19px;
            width: 236px;
            border-radius: 5px;
            border: 2px solid #f7941e;
            opacity: 0.7;
            font-family: Arial;
            background-color: #414042;
            color: #ffffff;
            font-size: 14px;
            opacity: 0.5;
        }
        #commands {
            padding: 5px;
            position: absolute;
            right: 1%;
            top: 2%;
            height: 65px;
            width: 180px;
            border-radius: 5px;
            border: 2px solid #f7941e;
            opacity: 0.7;
            font-family: Arial;
            background-color: #414042;
            color: #ffffff;
            font-size: 14px;
            opacity: 0.5;
        }
        a {
            color: #f7941e;
            text-decoration: none;
        }
        a:hover {
            color: #ffffff;
        }
    </style>
</head>
"""
)

BODY_TEMPLATE = Template(
    """
<body>
    $X3DSCENE
    <div id="pythonocc_rocks">
        pythonocc-$VERSION <a href="https://www.x3dom.org" target="_blank">x3dom</a> renderer
    </div>
    <div id="commands">
    <b>t</b> view/hide shape<br>
    <b>r</b> reset view<br>
    <b>a</b> show all<br>
    <b>u</b> upright<br>
    </div>
    <script>
    var selected_target_color = null;
    var current_selected_shape = null;
    var current_mat = null;
    function fitCamera()
    {            
        var x3dElem = document.getElementById('pythonocc-x3d-scene');            
        x3dElem.runtime.fitAll();
    }
    function select(the_shape) // called whenever a shape is clicked
    {
        // restore color for previous selected shape
        if (current_mat) {
            current_mat.diffuseColor = selected_target_color;
        }
        // store the shape for future process
        current_selected_shape = the_shape;
        console.log(the_shape);
        // store color, to be restored later
        appear = current_selected_shape.getElementsByTagName("Appearance")[0];
        mat = appear.getElementsByTagName("Material")[0];
        current_mat = mat;
        console.log(mat);
        selected_target_color = mat.diffuseColor;
        mat.diffuseColor = "1, 0.65, 0";
        //console.log(the_shape.getElementsByTagName("Appearance"));//.getAttribute('diffuseColor'));
    }
    function onDocumentKeyPress(event) {
      event.preventDefault();
      if (event.key=="t") {  // t key
         if (current_selected_shape) {
           if (current_selected_shape.render == "true") {
              current_selected_shape.render = "false";
           }
           else {
              current_selected_shape.render = "true";
           }
         }
      }

    }
    // add events
    document.addEventListener('keypress', onDocumentKeyPress, false);
    </script>
</body>
"""
)


def export_edge_to_indexed_lineset(edge_point_set):
    str_x3d_to_return = f"\t<LineSet vertexCount='{len(edge_point_set)}'>"
    str_x3d_to_return += "<Coordinate point='"
    for p in edge_point_set:
        str_x3d_to_return += f"{p[0]} {p[1]} {p[2]} "
    str_x3d_to_return += "'/></LineSet>\n"
    return str_x3d_to_return


def indexed_lineset_to_x3d_string(str_linesets, header=True, footer=True, ils_id=0):
    """takes an str_lineset, coming for instance from export_curve_to_ils,
    and export to an X3D string"""
    x3dfile_str = (
        X3DFILE_HEADER_TEMPLATE.substitute({"VERSION": f"{VERSION}"}) if header else ""
    )
    x3dfile_str += "<Switch whichChoice='0' id='swBRP'>\n"
    x3dfile_str += "\t<Group>\n"

    for ils_id, str_lineset in enumerate(str_linesets):
        x3dfile_str += f"\t\t<Transform scale='1 1 1'><Shape DEF='edg{ils_id}'>\n"
        # empty appearance, but the x3d validator complains if nothing set
        x3dfile_str += (
            "\t\t\t<Appearance><Material emissiveColor='0 0 0'/></Appearance>\n\t\t"
        )
        x3dfile_str += str_lineset
        x3dfile_str += "\t\t</Shape></Transform>\n"
    x3dfile_str += "\t</Group>\n"
    x3dfile_str += "</Switch>\n"
    if footer:
        x3dfile_str += "</Scene>\n</X3D>\n"

    return x3dfile_str


class HTMLHeader:
    def __init__(self, bg_gradient_color1="#ced7de", bg_gradient_color2="#808080"):
        self._bg_gradient_color1 = bg_gradient_color1
        self._bg_gradient_color2 = bg_gradient_color2

    def get_str(self):
        return HEADER_TEMPLATE.substitute(
            {
                "bg_gradient_color1": f"{self._bg_gradient_color1}",
                "bg_gradient_color2": f"{self._bg_gradient_color2}",
                "VERSION": f"{VERSION}",
            }
        )


class HTMLBody:
    def __init__(self, x3d_shapes, axes_plane, axes_plane_zoom_factor=1.0):
        """x3d_shapes is a list that contains uid for each shape"""
        self._x3d_shapes = x3d_shapes
        self.spinning_cursor = spinning_cursor()
        self._display_axes_plane = axes_plane
        self._axis_plane_zoom_factor = axes_plane_zoom_factor

    def get_str(self):
        # get the location where pythonocc is running from
        x3dcontent = "\n\t<x3d id='pythonocc-x3d-scene' style='width:100%;height:100%;border:none' >\n\t\t<Scene>\n"
        nb_shape = len(self._x3d_shapes)
        if self._display_axes_plane:
            x3dcontent += f"""
            <transform scale='{self._axis_plane_zoom_factor} {self._axis_plane_zoom_factor} {self._axis_plane_zoom_factor}'>
            <transform id='plane_small_axe_Id' rotation='1 0 0 -1.57079632679'>
                <inline url="https://rawcdn.githack.com/x3dom/component-editor/master/static/x3d/plane.x3d" mapDEFToID="true" namespaceName="plane"></inline>
                <inline url="https://rawcdn.githack.com/x3dom/component-editor/master/static/x3d/axesSmall.x3d" mapDEFToID="true" namespaceName="axesSmall"></inline>
            </transform>
            <inline url="https://rawcdn.githack.com/x3dom/component-editor/master/static/x3d/axes.x3d" mapDEFToID="true" namespaceName="axes"></inline>
            </transform>
            """
            # global rotate so that z is properly aligned
        x3dcontent += '<transform id="global_scene_rotation_Id" rotation="1 0 0 -1.57079632679">\n'
        for cur_shp, shp_uid in enumerate(self._x3d_shapes, start=1):
            sys.stdout.write(
                "\r%s meshing shapes... %i%%"
                % (next(self.spinning_cursor), round(cur_shp / nb_shape * 100))
            )
            sys.stdout.flush()
            # only the last downloaded shape raises a fitCamera event
            x3dcontent += "\t\t\t<Inline "
            if cur_shp == nb_shape:
                x3dcontent += 'onload="fitCamera() "'
            x3dcontent += f'mapDEFToID="true" url="{shp_uid}.x3d"></Inline>\n'
        x3dcontent += "\t\t\t</transform>\n\t\t</Scene>\n\t</x3d>\n"

        return BODY_TEMPLATE.substitute(
            {"VERSION": f"{VERSION}", "X3DSCENE": f"{x3dcontent}"}
        )


class X3DExporter:
    """A class for exporting a TopoDS_Shape to an x3d file"""

    def __init__(
        self,
        shape,  # the TopoDS shape to mesh
        vertex_shader,  # the vertex_shader, passed as a string
        fragment_shader,  # the fragment shader, passed as a string
        export_edges,  # if yes, edges are exported to IndexedLineSet (might be SLOWW)
        color,  # the default shape color
        specular_color,  # shape specular color (white by default)
        shininess,  # shape shininess
        transparency,  # shape transparency
        line_color,  # edge color
        line_width,  # edge liewidth,
        mesh_quality,  # mesh quality default is 1., good is <1, bad is >1
    ):
        self._shape = shape
        self._vs = vertex_shader
        self._fs = fragment_shader
        self._export_edges = export_edges
        self._color = color
        self._shininess = shininess
        self._specular_color = specular_color
        self._transparency = transparency
        self._mesh_quality = mesh_quality
        # the list of indexed face sets that compose the shape
        # if ever the map_faces_to_mesh option is enabled, this list
        # maybe composed of dozains of TriangleSet
        self._triangle_sets = []
        self._line_sets = []
        self._x3d_string = ""  # the string that contains the x3d description

    def compute(self):
        shape_tesselator = ShapeTesselator(self._shape)
        shape_tesselator.Compute(
            compute_edges=self._export_edges,
            mesh_quality=self._mesh_quality,
            parallel=True,
        )
        self._triangle_sets.append(shape_tesselator.ExportShapeToX3DTriangleSet())
        # then process edges
        if self._export_edges:
            # get number of edges
            nbr_edges = shape_tesselator.ObjGetEdgeCount()
            for i_edge in range(nbr_edges):
                nbr_vertices = shape_tesselator.ObjEdgeGetVertexCount(i_edge)
                edge_point_set = [
                    shape_tesselator.GetEdgeVertex(i_edge, i_vert)
                    for i_vert in range(nbr_vertices)
                ]
                ils = export_edge_to_indexed_lineset(edge_point_set)
                self._line_sets.append(ils)

    def to_x3dfile_string(self, shape_id):
        x3dfile_str = X3DFILE_HEADER_TEMPLATE.substitute({"VERSION": f"{VERSION}"})
        for triangle_set in self._triangle_sets:
            x3dfile_str += "<Switch whichChoice='0' id='swBRP'>"
            x3dfile_str += f"<Transform scale='1 1 1'>\n<Shape DEF='shape{shape_id}' onclick='select(this);'>\n"
            x3dfile_str += "<Appearance>\n"
            #
            # set Material or shader
            #
            if self._vs is None and self._fs is None:
                x3dfile_str += "<Material id='color' diffuseColor="
                x3dfile_str += f"'{self._color[0]} {self._color[1]} {self._color[2]}' "
                x3dfile_str += f"shininess='{self._shininess}' "
                x3dfile_str += f"specularColor='{self._specular_color[0]} {self._specular_color[1]} {self._specular_color[2]}' "
                x3dfile_str += f"transparency='{self._transparency}'/>\n"
            else:  # set shaders
                x3dfile_str += (
                    '<ComposedShader><ShaderPart type="VERTEX" style="display:none;">\n'
                )
                x3dfile_str += self._vs
                x3dfile_str += "</ShaderPart>\n"
                x3dfile_str += '<ShaderPart type="FRAGMENT" style="display:none;">\n'
                x3dfile_str += self._fs
                x3dfile_str += "</ShaderPart></ComposedShader>\n"
            x3dfile_str += "</Appearance>\n"
            # export triangles
            x3dfile_str += triangle_set
            x3dfile_str += "</Shape></Transform></Switch>\n"
        # and now, process edges
        if self._export_edges:
            # below '0' means show all
            # -1 means doesn't show line
            # the "Switch" node selects the group to be displayed

            x3dfile_str += indexed_lineset_to_x3d_string(
                self._line_sets, header=False, footer=False
            )
        x3dfile_str += "</Scene>\n</X3D>\n"

        #
        # use ElementTree to ensure xml file quality
        #
        xml_et = ElementTree.fromstring(x3dfile_str)
        return ElementTree.tostring(xml_et, encoding="utf8").decode("utf8")

    def write_to_file(self, filename, shape_id):
        with open(filename, "w") as f:
            f.write(self.to_x3dfile_string(shape_id))


class X3DomRenderer:
    def __init__(self, path=None, display_axes_plane=True, axes_plane_zoom_factor=1.0):
        self._path = tempfile.mkdtemp() if not path else path
        self._html_filename = os.path.join(self._path, "index.html")
        self._x3d_shapes = {}
        self._x3d_edges = {}
        self._axes_plane = (
            display_axes_plane  # display the small RVB axes and the plane
        )
        self._axes_plane_zoom_factor = axes_plane_zoom_factor

        print(
            f"## x3dom webgl renderer - render axes/planes : {self._axes_plane} - axes/plane zoom factor : {self._axes_plane_zoom_factor}"
        )

    def DisplayShape(
        self,
        shape,
        vertex_shader=None,
        fragment_shader=None,
        export_edges=False,
        color=(0.65, 0.65, 0.7),
        specular_color=(0.2, 0.2, 0.2),
        shininess=0.9,
        transparency=0.0,
        line_color=(0, 0.0, 0.0),
        line_width=2.0,
        mesh_quality=1.0,
    ):
        """Adds a shape to the rendering buffer. This class computes the x3d file"""
        # if the shape is an edge or a wire, use the related functions
        if is_edge(shape):
            print("X3D exporter, discretize an edge")
            pnts = discretize_edge(shape)
            edge_hash = f"edg{uuid.uuid4().hex}"
            line_set = export_edge_to_indexed_lineset(pnts)
            x3dfile_content = indexed_lineset_to_x3d_string(
                [line_set], ils_id=edge_hash
            )
            edge_full_path = os.path.join(self._path, f"{edge_hash}.x3d")
            with open(edge_full_path, "w") as edge_file:
                edge_file.write(x3dfile_content)
            # store this edge hash
            self._x3d_edges[edge_hash] = [color, line_width]
            return self._x3d_shapes, self._x3d_edges

        if is_wire(shape):
            print("X3D exporter, discretize a wire")
            pnts = discretize_wire(shape)
            wire_hash = f"wir{uuid.uuid4().hex}"
            line_set = export_edge_to_indexed_lineset(pnts)
            x3dfile_content = indexed_lineset_to_x3d_string(
                [line_set], ils_id=wire_hash
            )
            wire_full_path = os.path.join(self._path, f"{wire_hash}.x3d")
            with open(wire_full_path, "w") as wire_file:
                wire_file.write(x3dfile_content)
            # store this edge hash
            self._x3d_edges[wire_hash] = [color, line_width]
            return self._x3d_shapes, self._x3d_edges

        shape_uuid = uuid.uuid4().hex
        shape_hash = f"shp{shape_uuid}"
        x3d_exporter = X3DExporter(
            shape,
            vertex_shader,
            fragment_shader,
            export_edges,
            color,
            specular_color,
            shininess,
            transparency,
            line_color,
            line_width,
            mesh_quality,
        )
        x3d_exporter.compute()
        x3d_filename = os.path.join(self._path, f"{shape_hash}.x3d")
        # the x3d filename is computed from the shape hash
        shape_id = len(self._x3d_shapes)
        x3d_exporter.write_to_file(x3d_filename, shape_id)

        self._x3d_shapes[shape_hash] = [
            export_edges,
            color,
            specular_color,
            shininess,
            transparency,
            line_color,
            line_width,
        ]
        return self._x3d_shapes, self._x3d_edges

    def render(self, addr="localhost", server_port=8080, open_webbrowser=False):
        """Call the render() method to display the X3D scene."""
        # first generate the HTML root file
        self.generate_html_file(self._axes_plane, self._axes_plane_zoom_factor)
        # then create a simple web server
        start_server(addr, server_port, self._path, open_webbrowser)

    def generate_html_file(self, axes_plane, axes_plane_zoom_factor):
        """Generate the HTML file to be rendered wy the web browser
        axes_plane: a boolean, tells whether or not display axes
        """
        with open(self._html_filename, "w") as html_file:
            html_file.write("<!DOCTYPE HTML>\n")
            html_file.write('<html lang="en">')
            # header
            html_file.write(HTMLHeader().get_str())
            # body
            # merge shapes and edges keys
            all_shapes = list(self._x3d_shapes) + list(self._x3d_edges)
            html_file.write(
                HTMLBody(all_shapes, axes_plane, axes_plane_zoom_factor).get_str()
            )
            html_file.write("</html>\n")
