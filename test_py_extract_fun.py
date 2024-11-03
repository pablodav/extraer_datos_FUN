# test_extractor.py
import unittest
from main import SwimmingDataExtractor

class TestSwimmingDataExtractor(unittest.TestCase):
    def setUp(self):
        self.sample_data = """
Evento 1 Mujeres 16-18 200 CC Metro Estilo Libre
EdadNombre Equipo Tiempo de Finales Puntos
Piscinas Barriales DE Salto
171 Gallino, Camila 2:27,63 9
Club Nacional Nueva Helvecia
162 Font, Valentina 2:35,49 7

Evento 2 Mixto 16-18 4x50 CC Metro Estilo Libre Relevo
Equipo Relevo Tiempo de Finales Puntos
A
1 Carrasco Lawn Tennis Club 1:56,08 18
1) Cuadra, Sebastian M18 2) Grassi, Valentin M16 3) Estol, Lucia W16 4) Vidiella, Federica W17
        """
        self.extractor = SwimmingDataExtractor(self.sample_data)

    def test_event_extraction(self):
        self.extractor.extract_events()
        self.assertEqual(len(self.extractor.events), 2)
        self.assertEqual(self.extractor.events[0]['number'], 1)
        self.assertEqual(self.extractor.events[0]['type'], 'Mujeres')

    def test_individual_swimmer_extraction(self):
        self.extractor.extract_events()
        self.assertEqual(len(self.extractor.swimmers), 2)
        self.assertEqual(self.extractor.swimmers[0].name, 'Gallino, Camila')
        self.assertEqual(self.extractor.swimmers[0].age, 17)
        self.assertEqual(self.extractor.swimmers[0].points, 9)

    def test_relay_team_extraction(self):
        self.extractor.extract_events()
        self.assertEqual(len(self.extractor.relay_teams), 1)
        relay_team = self.extractor.relay_teams[0]
        self.assertEqual(relay_team.team_name, 'Carrasco Lawn Tennis Club')
        self.assertEqual(len(relay_team.swimmers), 4)
        self.assertEqual(relay_team.swimmers[0]['gender'], 'M')
        self.assertEqual(relay_team.swimmers[0]['age'], 18)

if __name__ == '__main__':
    unittest.main()