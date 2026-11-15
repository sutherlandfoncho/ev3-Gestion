"""Pruebas de lógica de la demo. Ejecutar desde 02_Prototipo_Datos_Simulados:
python -m unittest discover -s tests -v
"""
import unittest
from pathlib import Path
import sys
import tempfile
import pandas as pd

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.generar_datos import generar
from src.procesar_modelo import preparar, evaluar,FEATURES

class TestDemo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory()
        cls.base=Path(cls.tmp.name)
        cls.a,cls.b=generar(cls.base/'datos')
        cls.gps=pd.read_csv(cls.a,dtype={'recorrido':str})
        cls.bip=pd.read_csv(cls.b,dtype={'recorrido':str})
    @classmethod
    def tearDownClass(cls): cls.tmp.cleanup()
    def test_fuentes_son_solo_simuladas(self):
        self.assertTrue(self.gps.tipo_dato.eq('SIMULADO_NO_REAL').all())
        self.assertTrue(self.bip.tipo_dato.eq('SIMULADO_NO_REAL').all())
    def test_sin_identificadores_de_pasajeros(self):
        self.assertFalse(any(x in self.bip.columns for x in ['id_pasajero','card_id','nombre','rut','user_id']))
    def test_unicidad_clave_agregacion(self):
        self.assertFalse(self.bip.duplicated(['fecha','recorrido','franja']).any())
    def test_sin_filtracion_de_objetivo(self):
        self.assertNotIn('minutos_observados_gps',FEATURES)
        self.assertNotIn('validaciones_agregadas',FEATURES)
    def test_generacion_rezago(self):
        d=preparar(self.gps,self.bip)
        self.assertEqual(len(d),len(self.gps))
        self.assertEqual(d['demanda_rezago_7d'].isna().sum(),0)
    def test_rechazo_campo_personal(self):
        b=self.bip.copy(); b['id_pasajero']='SIMULADO'
        with self.assertRaises(ValueError): preparar(self.gps,b)
    def test_entrenamiento_y_archivos(self):
        m=evaluar(self.a,self.b,self.base/'resultado')
        self.assertGreater(m['registros_prueba'],0)
        self.assertTrue((self.base/'resultado/predicciones_SIMULADAS.csv').exists())
        self.assertLess(m['mae_modelo_min'],m['mae_baseline_min'])
        self.assertIn('mae_regresion_lineal_min',m)
        self.assertGreater(m['mae_regresion_lineal_min'],0)
    def test_lineal_presente_en_salidas(self):
        m=evaluar(self.a,self.b,self.base/'resultado')
        r=pd.read_csv(self.base/'resultado/predicciones_SIMULADAS.csv')
        self.assertIn('prediccion_lineal_min',r.columns)
        self.assertGreater(m['mae_regresion_lineal_min'],0)

if __name__=='__main__': unittest.main()
