import open3d as o3d 
import numpy as np

class Open3DDrawer:
    def __init__(self):
        self.geometries = []
        self.visualizer = o3d.visualization.Visualizer()
        self.rendercam = {
            "intrinsic": {
                "w":800,
                "h": 800,
                "fx":10,
                "fy":10,        
                "cx":400,
                "cy":400
            },
            "extrinsic": np.array([[1, 0, 0, 0],
                                    [0, 0, -1, 3],
                                    [0, 1, 0, 10],
                                    [0, 0, 0, 1],
                                    ])
        }

        self.externcam = {
            "intrinsic": {
                "w":800,
                "h": 800,
                "fx":1000,
                "fy":1000,        
                "cx":400,
                "cy":400
            },
            "extrinsic": np.array([[1, 0, 0, 0],
                                    [0, 0, -1, 7],
                                    [0, 1, 0, 10],
                                    [0, 0, 0, 1],
                                    ])
        }


    def draw_groundplane(self):
        mesh_x1 = np.vstack([range(-100,100), -100*np.ones((200,)), np.zeros((200,))]).T
        mesh_x2 = np.vstack([range(-100,100), 100*np.ones((200,)), np.zeros((200,))]).T
        mesh_x = np.vstack((mesh_x1, mesh_x2))
        lines_x = np.array([range(0, 200), range(200,400)]).T

        mesh_y1 = np.vstack([-100*np.ones((200,)), range(-100,100), np.zeros((200,))]).T
        mesh_y2 = np.vstack([100*np.ones((200,)), range(-100,100), np.zeros((200,))]).T
        mesh_y = np.vstack((mesh_y1, mesh_y2))
        lines_y = np.array([range(0, 200), range(200,400)]).T

        lineset_x = o3d.geometry.LineSet()
        lineset_x.points = o3d.utility.Vector3dVector(mesh_x)
        lineset_x.lines = o3d.utility.Vector2iVector(lines_x)
        lineset_y = o3d.geometry.LineSet()
        lineset_y.points = o3d.utility.Vector3dVector(mesh_y)
        lineset_y.lines = o3d.utility.Vector2iVector(lines_y)

        #colors = 0.1*np.ones((200,3))
        #lineset_x.colors = o3d.utility.Vector3dVector(colors)
        #lineset_y.colors = o3d.utility.Vector3dVector(colors)
        self.geometries += [lineset_x, lineset_y]


    def draw_furstum(self):
        """

        """
        points = np.array([
                        [0,0,0],         # camera center
                        [-1,-1,1],       # image plane
                        [-1,1,1],
                        [1,1,1],
                        [1,-1,1]
                        ])
        lines = np.array([[0, 1], [0, 2], [0, 3], [0, 4], [1, 2], [2, 3], [3, 4], [4, 1]])
        lineset = o3d.geometry.LineSet()
        lineset.points = o3d.utility.Vector3dVector(points)
        lineset.lines = o3d.utility.Vector2iVector(lines)
        self.geometries.append(lineset)
    
    def render(self):
        self.visualizer.create_window(window_name="Scene",width=1000, height=1000)
        for geometry in self.geometries:
            self.visualizer.add_geometry(geometry)
        print(self.geometries)
        print(self.visualizer.get_render_option())
        vc = self.visualizer.get_view_control()

        camera_params = vc.convert_to_pinhole_camera_parameters()

        #camera_params.intrinsic.set_intrinsics(self.externcam["intrinsic"]["w"], self.externcam["intrinsic"]["h"], 
        #                                       self.externcam["intrinsic"]["fx"], self.externcam["intrinsic"]["fy"],
        #                                       self.externcam["intrinsic"]["cx"], self.externcam["intrinsic"]["cy"])
        camera_params.extrinsic = self.externcam["extrinsic"]
        print(camera_params.extrinsic)

        # Apply the new parameters back to the view control
        vc.convert_from_pinhole_camera_parameters(camera_params)

        self.visualizer.poll_events()
        self.visualizer.update_renderer()
        self.visualizer.run()
        self.visualizer.destroy_window()


drawer = Open3DDrawer()
drawer.draw_groundplane()
drawer.draw_furstum()

drawer.render()

