import unittest
import uuid

from mesa.model import Model
from shapely.geometry import Point

from mesa_geo import AgentCreator, GeoAgent, GeoSpace
from mesa_geo.visualization.modules import MapModule


class TestMapModule(unittest.TestCase):
    def setUp(self) -> None:
        self.model = Model()
        self.model.space = GeoSpace()
        self.agent_creator = AgentCreator(
            agent_class=GeoAgent, model=self.model, crs="epsg:3857"
        )
        self.geometries = [Point(1, 1)] * 7
        self.agents = [
            self.agent_creator.create_agent(
                geometry=geometry, unique_id=uuid.uuid4().int
            )
            for geometry in self.geometries
        ]
        self.model.space.add_agents(self.agents)

    def tearDown(self) -> None:
        pass

    def test_render_agents(self):
        map_module = MapModule(portrayal_method=lambda x: {"color": "red", "radius": 7})
        self.assertDictEqual(
            map_module.render(self.model).get("agents"),
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": (
                                8.983152841195214e-06,
                                8.983152841195177e-06,
                            ),
                        },
                        "properties": {"color": "red", "radius": 7},
                    }
                ]
                * len(self.agents),
            },
        )
