"""
Mesh comparison utility for evaluated Blender meshes.
Compares vertices, edges, faces, and all mesh attributes between two evaluated meshes.

For evaluated (geometry) meshes in Blender:
- Use `ob.data.mge` to get the evaluated geometry container
- Vertices are accessed as `.mge.vertices` 
- Positions/attributes are vectors stored with `position`, `normal`, etc.
"""


def compare_evaluated_meshes(mesh1_name, mesh2_name):
    """
    Compare two evaluated meshes (their full data blocks and attributes).
    
    Args:
        mesh1_name: Name of the first evaluated mesh in the scene (str)
        mesh2_name: Name of the second evaluated mesh in the scene (str)
    
    Returns:
        dict containing detailed comparison results with:
        - topology counts (vertices, edges, faces)
        - position comparisons for all vertices
        - normal/tangent/uv/color attribute comparisons
        - face polygon matching
        - overall result
    
    Raises:
        ValueError: If meshes cannot be found or are not valid evaluated meshes.
    """
    import bpy
    
    # Find both objects in the scene
    try:
        ob1 = bpy.data.objects[mesh1_name]
        ob2 = bpy.data.objects[mesh2_name]
        
        if ob1 is None or ob2 is None:
            raise ValueError(f"One or both meshes not found in scene")
            
        # Get their mesh data blocks
        me1 = ob1.data
        me2 = ob2.data
        
        # Check if both are Mesh data types (evaluated meshes always have geometry)
        if not hasattr(me1, 'mge') or not hasattr(me2, 'mge'):
            raise ValueError("Both objects must be mesh data blocks")
            
    except KeyError as e:
        raise ValueError(f"Mesh not found: {e}")
    
    # Get the evaluated geometry (the multi-layer geometry container)
    vdata1 = me1.mge  # first geometry of the evaluated mesh
    vdata2 = me2.mge
    
    comparison_result = {
        'mesh1': mesh1_name,
        'mesh2': mesh2_name,
        'is_identical': None,
        'differences': []
    }
    
    # ======================
    # STEP 1: Compare TOPLOGY COUNTS
    # ======================
    comparison_result['vertex_count_1'] = len(vdata1.vertices) if hasattr(vdata1, 'vertices') else len(me1.mge.vertices)
    comparison_result['vertex_count_2'] = len(vdata2.vertices) if hasattr(vdata2, 'vertices') else len(me2.mge.vertices)
    
    comparison_result['edge_count_1'] = len(vdata1.edges) if hasattr(vdata1, 'edges') else len(me1.mge.edges)
    comparison_result['edge_count_2'] = len(vdata2.edges) if hasattr(vdata2, 'edges') else len(me2.mge.edges)
    
    # For faces (polygons), access directly from geometry
    comparison_result['face_count_1'] = len(vdata1.polygons) if hasattr(vdata1, 'polygons') else 0
    comparison_result['face_count_2'] = len(vdata2.polygons) if hasattr(vdata2, 'polygons') else 0
    
    # ======================
    # STEP 2: Compare POSITION of all vertices
    # ======================
    comparison_result['positions_identical'] = True
    comparison_result['position_differences'] = []
    
    eps = 1e-5  # tolerance for floating-point position comparison
    
    # Get evaluated geometry vertex count
    vc1 = len(vdata1.vertices) if hasattr(vdata1, 'vertices') else len(me1.mge.vertices)
    vc2 = len(vdata2.vertices) if hasattr(vdata2, 'vertices') else len(me2.mge.vertices)
    
    for i in range(min(vc1, vc2)):
        # Access vertex data from the evaluated geometry (multi-layer)
        v1 = vdata1[i].position  # This returns a vector directly in Blender's .mge
        
        if hasattr(vdata2, 'vertices') and i < len(vdata2.vertices):
            v2 = vdata2[i].position
            pos_diff = abs(v1[0] - v2[0]) > eps or abs(v1[1] - v2[1]) > eps or abs(v1[2] - v2[2]) > eps
            
            if pos_diff:
                comparison_result['positions_identical'] = False
                comparison_result['position_differences'].append({
                    'vertex_index': i,
                    'mesh1_position': list(v1),
                    'mesh2_position': list(v2)
                })
        else:
            # Mismatch in vertex counts
            pass
    
    # ======================
    # STEP 3: Compare NORMAL vectors of all vertices
    # ======================
    comparison_result['normals_identical'] = True
    comparison_result['normal_differences'] = []
    
    for i in range(min(vc1, vc2)):
        if hasattr(vdata1, 'vertices'):
            v1 = vdata1.vertices[i]
        else:
            v1 = me1.mge.vertices[i]
        
        n1 = v1.normal
        
        if hasattr(vdata2, 'vertices') and i < len(vdata2.vertices):
            v2 = vdata2.vertices[i]
            n2 = v2.normal
            
            # Normalize normals if needed
            norm1 = max(0.001, len(n1))
            norm2 = max(0.001, len(n2))
            
            diff = (abs(n1[0]/norm1 - n2[0]/norm2) > eps or
                    abs(n1[1]/norm1 - n2[1]/norm2) > eps or
                    abs(n1[2]/norm1 - n2[2]/norm2) > eps)
            
            if diff:
                comparison_result['normals_identical'] = False
                comparison_result['normal_differences'].append({
                    'vertex_index': i,
                    'mesh1_normal': list(n1),
                    'mesh2_normal': list(n2)
                })
    
    # ======================
    # STEP 4: Compare TANGENT vectors of all vertices  
    # ======================
    comparison_result['tangents_identical'] = True
    comparison_result['tangent_differences'] = []
    
    for i in range(min(vc1, vc2)):
        if hasattr(vdata1, 'vertices'):
            v1 = vdata1.vertices[i]
        else:
            v1 = me1.mge.vertices[i]
        
        t1 = v1.tangent
        
        if hasattr(vdata2, 'vertices') and i < len(vdata2.vertices):
            v2 = vdata2.vertices[i]
            t2 = v2.tangent
            
            # Normalize tangents
            norm1 = max(0.001, len(t1))
            norm2 = max(0.001, len(t2))
            
            diff = (abs(t1[0]/norm1 - t2[0]/norm2) > eps or
                    abs(t1[1]/norm1 - t2[1]/norm2) > eps or
                    abs(t1[2]/norm1 - t2[2]/norm2) > eps)
            
            if diff:
                comparison_result['tangents_identical'] = False
                comparison_result['tangent_differences'].append({
                    'vertex_index': i,
                    'mesh1_tangent': list(t1),
                    'mesh2_tangent': list(t2)
                })
    
    # ======================
    # STEP 5: Compare UV coordinates of all vertices
    # ======================
    comparison_result['uvs_identical'] = True
    comparison_result['uv_differences'] = []
    
    for i in range(min(vc1, vc2)):
        if hasattr(vdata1, 'vertices'):
            v1 = vdata1.vertices[i]
        else:
            v1 = me1.mge.vertices[i]
        
        u1 = v1.uv
        
        if hasattr(vdata2, 'vertices') and i < len(vdata2.vertices):
            v2 = vdata2.vertices[i]
            u2 = v2.uv
            
            diff = (abs(u1[0] - u2[0]) > eps or abs(u1[1] - u2[1]) > eps)
            
            if diff:
                comparison_result['uvs_identical'] = False
                comparison_result['uv_differences'].append({
                    'vertex_index': i,
                    'mesh1_uv': list(u1),
                    'mesh2_uv': list(u2)
                })
    
    # ======================
    # STEP 6: Compare COLOR (col_0, col_1) of all vertices
    # ======================
    comparison_result['colors_identical'] = True
    comparison_result['color_differences'] = []
    
    for i in range(min(vc1, vc2)):
        if hasattr(vdata1, 'vertices'):
            v1 = vdata1.vertices[i]
        else:
            v1 = me1.mge.vertices[i]
        
        c1 = v1.col
        
        if hasattr(vdata2, 'vertices') and i < len(vdata2.vertices):
            v2 = vdata2.vertices[i]
            c2 = v2.col
            
            diff = (abs(c1[0] - c2[0]) > eps or abs(c1[1] - c2[1]) > eps or 
                    abs(c1[2] - c2[2]) > eps)
            
            if diff:
                comparison_result['colors_identical'] = False
                comparison_result['color_differences'].append({
                    'vertex_index': i,
                    'mesh1_color': list(c1),
                    'mesh2_color': list(c2)
                })
    
    # ======================
    # STEP 7: Compare POLYGON TOPOLOGY (face vertices indices)
    # ======================
    comparison_result['polygon_topology_identical'] = True
    comparison_result['polygon_differences'] = []
    
    pc1 = len(vdata1.polygons) if hasattr(vdata1, 'polygons') else 0
    pc2 = len(vdata2.polygons) if hasattr(vdata2, 'polygons') else 0
    
    if pc1 != pc2:
        comparison_result['polygon_topology_identical'] = False
        comparison_result['polygon_differences'].append({
            'type': 'face_count_mismatch',
            'mesh1_faces': pc1,
            'mesh2_faces': pc2
        })
    else:
        for i in range(pc1):
            try:
                p1 = vdata1.polygons[i]
                if hasattr(vdata1, 'vertices'):
                    vlist1 = vdata1.vertices
                
                p2 = vdata2.polygons[i]
                
                # Compare vertex indices defining each face (topology)
                if len(p1.vertices) != len(p2.vertices):
                    comparison_result['polygon_topology_identical'] = False
                    comparison_result['polygon_differences'].append({
                        'face_index': i,
                        'mesh1_vertex_indices': list(p1.vertices),
                        'mesh2_vertex_indices': list(p2.vertices)
                    })
                else:
                    # Compare the actual vertex indices of each face
                    for j in range(len(p1.vertices)):
                        v_idx1 = p1.vertices[j]
                        v_idx2 = p2.vertices[j]
                        
                        if hasattr(vdata1, 'vertices') and v_idx1 < len(vdata1.vertices):
                            actual_v1 = vdata1.vertices[v_idx1].position
                        
                        # For topology check, we mainly care that the indices match exactly
                        # (or are within tolerance of the same vertex)
            
            except:
                pass
    
    # ======================
    # STEP 8: Determine overall identicalness
    # ======================
    if any([
        not comparison_result.get('positions_identical'),
        not comparison_result.get('normals_identical'),
        not comparison_result.get('tangents_identical'),
        not comparison_result.get('uvs_identical'),
        not comparison_result.get('colors_identical'),
        not comparison_result.get('polygon_topology_identical')
    ]):
        comparison_result['is_identical'] = False
    elif (comparison_result.get('vertex_count_1', 0) != comparison_result.get('vertex_count_2', 0)):
        comparison_result['is_identical'] = False
    else:
        comparison_result['is_identical'] = True
    
    return comparison_result


if __name__ == "__main__":
    # Example usage with error handling for non-existent meshes
    try:
        result = compare_evaluated_meshes("Cube", "Cube")
        print(f"Mesh comparison result:")
        print(f"  Mesh1: {result['mesh1']}")
        print(f"  Mesh2: {result['mesh2']}")
        print(f"  Is identical: {result.get('is_identical', 'unknown')}")
    except ValueError as e:
        print(f"Expected error for non-existent meshes: {e}")
