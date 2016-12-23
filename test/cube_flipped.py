# Simple Python module defining an anonymous list of mold parts

[ ##List of parts (e.g.: friendly names + arguments for calculator.make_part)
    ("Bottom", { "start_edge": ([-1,1,1],[-1,1,-1])
                ,"end_edge": ([-1,-1,1],[-1,-1,-1])
                ,"part_plane": (1,2) # oriented along Y Z plane
                ,"shrink_edges": {"left", "right"}
                ,"shrink_axis": 1 # shrink along Y axis
                ,"thickness_direction_negative": False #model_center_along_negative_x_axis_from_part
                })
    ,("Top-i", { "start_edge": ([1,1,1],[1,1,-1])
              ,"end_edge": ([1,-1,1],[1,-1,-1])
              ,"part_plane": (1,2) #oriented along Y Z plane
              ,"shrink_edges": {"left": 'joint-default', "right": 104+115.4+18.7}#room for other Top parts
              ,"shrink_axis": 1 # shrink along Y axis
              })
    ,("Left", { "start_edge": ([-1,1,1],[-1,1,-1])
               ,"end_edge": ([1,1,1],[1,1,-1])
               ,"part_plane": (0,2) #oriented along X Z plane
               })
    ,("Right-i", { "start_edge": ([-1,-1,1],[-1,-1,-1])
                  ,"end_edge": ([1,-1,1],[1,-1,-1])
                  ,"part_plane": (0,2) #oriented along X Z plane
                  ,"shrink_edges": {'right': 145.8} #room for other Right parts
                  ,"shrink_axis": 0 # shrink along X axis
                  ,"thickness_direction_negative": False
                  })
    ,("Right-ii", { "start_edge": ([-1,-1,1],[-1,-1,-1])
                   ,"end_edge": ([1,-1,1],[1,-1,-1])
                   ,"part_plane": (0,2) #oriented along X Z plane
                   ,"shrink_edges": {'left': 106.3, 'right': 129.4}#room for other Right parts
                   ,"shrink_axis": 0 # shrink along X axis
                   ,"thickness_direction_negative": False
                   })
    ,("Right-iii", { "start_edge": ([-1,-1,1],[-1,-1,-1])
                    ,"end_edge": ([1,-1,1],[1,-1,-1])
                    ,"part_plane": (0,2) #oriented along X Z plane
                    ,"shrink_edges": {'left': 122.7, 'right': 123.5}#room for other Right parts
                    ,"shrink_axis": 0 # shrink along X axis
                    ,"thickness_direction_negative": False
                    })
    ,("Right-iv", { "start_edge": ([-1,-1,1],[-1,-1,-1])
                   ,"end_edge": ([1,-1,1],[1,-1,-1])
                   ,"part_plane": (0,2) #oriented along X Z plane
                   ,"shrink_edges": {'left': 128.6, 'right': 50.7}#room for other Right parts
                   ,"shrink_axis": 0 # shrink along X axis
                   ,"thickness_direction_negative": False
                   })
    ,("Right-v", { "start_edge": ([-1,-1,1],[-1,-1,-1])
                  ,"end_edge": ([1,-1,1],[1,-1,-1])
                  ,"part_plane": (0,2) #oriented along X Z plane
                  ,"shrink_edges": {'left': 50.7}#room for other Right parts
                  ,"shrink_axis": 0 # shrink along X axis
                  ,"thickness_direction_negative": False
                  })
]
