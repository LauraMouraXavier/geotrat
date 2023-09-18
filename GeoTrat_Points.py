"""
Model exported as python.
Name : GEOTrat - Points
Group : Mestrado
With QGIS : 32208
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterField
from qgis.core import QgsProcessingParameterCrs
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsProcessingParameterFileDestination
from qgis.core import QgsExpression
import processing


class GeotratPoints(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('opo_1_varivel_medida_em_campo', 'Variable measured in the field', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterField('campo_da_varivel', 'Variable field', type=QgsProcessingParameterField.Numeric, parentLayerParameterName='opo_1_varivel_medida_em_campo', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterField('campodotratamento', 'Treatment field', type=QgsProcessingParameterField.String, parentLayerParameterName='opo_1_varivel_medida_em_campo', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('rea_de_estudo2', 'Study area polygon', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterCrs('sistema_de_coordenadas_projetadas', 'Projected Coordinate System', defaultValue='EPSG:4326'))
        self.addParameter(QgsProcessingParameterNumber('definir_tamanho_do_pixel', 'Pixel size (m)', type=QgsProcessingParameterNumber.Double, minValue=0.1, maxValue=100, defaultValue=None))
        self.addParameter(QgsProcessingParameterEnum('semivariogrammodel', 'Semivariogram model', options=['Linear','Exponential','Gaussian','Spherical'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0]))
        self.addParameter(QgsProcessingParameterRasterDestination('T1', 'T1', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('T2', 'T2', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Gain', 'Gain', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('StatisticsOfGain', 'Statistics of gain', optional=True, fileFilter='HTML files (*.html *.HTML)', createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(25, model_feedback)
        results = {}
        outputs = {}

        # Reproject points
        alg_params = {
            'INPUT': parameters['opo_1_varivel_medida_em_campo'],
            'OPERATION': '',
            'TARGET_CRS': parameters['sistema_de_coordenadas_projetadas'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectPoints'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Reproject area
        alg_params = {
            'INPUT': parameters['rea_de_estudo2'],
            'OPERATION': '',
            'TARGET_CRS': parameters['sistema_de_coordenadas_projetadas'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectArea'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Rename variable field
        alg_params = {
            'FIELD': parameters['campo_da_varivel'],
            'INPUT': outputs['ReprojectPoints']['OUTPUT'],
            'NEW_NAME': 'variavel',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenameVariableField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Rename treatment field
        alg_params = {
            'FIELD': parameters['campodotratamento'],
            'INPUT': outputs['RenameVariableField']['OUTPUT'],
            'NEW_NAME': 'trat',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RenameTreatmentField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Separate T1 and T2
        alg_params = {
            'FIELD': 'trat',
            'INPUT': outputs['RenameTreatmentField']['OUTPUT'],
            'OPERATOR': 0,  # =
            'VALUE': 'T1',
            'FAIL_OUTPUT': QgsProcessing.TEMPORARY_OUTPUT,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SeparateT1AndT2'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Select T2-80%
        alg_params = {
            'INPUT': outputs['SeparateT1AndT2']['FAIL_OUTPUT'],
            'METHOD': 1,  # Percentage of selected features
            'NUMBER': 80
        }
        outputs['SelectT280'] = processing.run('qgis:randomselection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Select T1-80%
        alg_params = {
            'INPUT': outputs['SeparateT1AndT2']['OUTPUT'],
            'METHOD': 1,  # Percentage of selected features
            'NUMBER': 80
        }
        outputs['SelectT180'] = processing.run('qgis:randomselection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Extract T1-80%
        alg_params = {
            'INPUT': outputs['SelectT180']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractT180'] = processing.run('native:saveselectedfeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # KrigO - T1-80%
        alg_params = {
            'BLOCK': False,
            'CV_METHOD': 0,  # [0] none
            'CV_SAMPLES': 10,
            'DBLOCK': 100,
            'FIELD': 'variavel',
            'LOG': False,
            'POINTS': outputs['ExtractT180']['OUTPUT'],
            'SEARCH_POINTS_ALL': 1,  # [1] all points within search distance
            'SEARCH_POINTS_MAX': 20,
            'SEARCH_POINTS_MIN': 16,
            'SEARCH_RADIUS': 1000,
            'SEARCH_RANGE': 1,  # [1] global
            'TARGET_USER_SIZE': parameters['definir_tamanho_do_pixel'],
            'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': outputs['ReprojectArea']['OUTPUT'],
            'TQUALITY': 1,  # [1] Variance
            'VAR_MAXDIST': 0,
            'VAR_MODEL': QgsExpression("CASE\r\nWHEN  @semivariogrammodel  = '0' THEN 'a + b * x'\r\nWHEN @semivariogrammodel  = '1' THEN 'a + b * (1 - (exp(-x/c)))'\r\nWHEN @semivariogrammodel  = '2' THEN 'a + b * (1 - (exp(-x^2/c^2)))'\r\nWHEN @semivariogrammodel  = '3' THEN 'a + b * ((1.5 * (x/c)) - (0.5 * (x^3/c^3)))'\r\nEND").evaluate(),
            'VAR_NCLASSES': 100,
            'VAR_NSKIP': 1,
            'CV_RESIDUALS': QgsProcessing.TEMPORARY_OUTPUT,
            'CV_SUMMARY': QgsProcessing.TEMPORARY_OUTPUT,
            'PREDICTION': QgsProcessing.TEMPORARY_OUTPUT,
            'VARIANCE': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['KrigoT180'] = processing.run('sagang:ordinarykriging', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Extract T1-20%
        alg_params = {
            'INPUT': outputs['SeparateT1AndT2']['OUTPUT'],
            'INTERSECT': outputs['ExtractT180']['OUTPUT'],
            'PREDICATE': [2],  # disjoint
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractT120'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Sample T1
        alg_params = {
            'COLUMN_PREFIX': 'amostra',
            'INPUT': outputs['ExtractT120']['OUTPUT'],
            'RASTERCOPY': outputs['KrigoT180']['PREDICTION'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SampleT1'] = processing.run('native:rastersampling', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Extract T2-80%
        alg_params = {
            'INPUT': outputs['SelectT280']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractT280'] = processing.run('native:saveselectedfeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Error T1
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'erro',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': ' "variavel" -  "amostra1" ',
            'INPUT': outputs['SampleT1']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ErrorT1'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Extract T2-20%
        alg_params = {
            'INPUT': outputs['SeparateT1AndT2']['FAIL_OUTPUT'],
            'INTERSECT': outputs['ExtractT280']['OUTPUT'],
            'PREDICATE': [2],  # disjoint
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractT220'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # KrigO - T2-80%
        alg_params = {
            'BLOCK': False,
            'CV_METHOD': 0,  # [0] none
            'CV_SAMPLES': 10,
            'DBLOCK': 100,
            'FIELD': 'variavel',
            'LOG': False,
            'POINTS': outputs['ExtractT280']['OUTPUT'],
            'SEARCH_POINTS_ALL': 1,  # [1] all points within search distance
            'SEARCH_POINTS_MAX': 20,
            'SEARCH_POINTS_MIN': 16,
            'SEARCH_RADIUS': 1000,
            'SEARCH_RANGE': 1,  # [1] global
            'TARGET_USER_SIZE': parameters['definir_tamanho_do_pixel'],
            'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': outputs['ReprojectArea']['OUTPUT'],
            'TQUALITY': 1,  # [1] Variance
            'VAR_MAXDIST': 0,
            'VAR_MODEL': QgsExpression("CASE\r\nWHEN  @semivariogrammodel  = '0' THEN 'a + b * x'\r\nWHEN @semivariogrammodel  = '1' THEN 'a + b * (1 - (exp(-x/c)))'\r\nWHEN @semivariogrammodel  = '2' THEN 'a + b * (1 - (exp(-x^2/c^2)))'\r\nWHEN @semivariogrammodel  = '3' THEN 'a + b * ((1.5 * (x/c)) - (0.5 * (x^3/c^3)))'\r\nEND").evaluate(),
            'VAR_NCLASSES': 100,
            'VAR_NSKIP': 1,
            'CV_RESIDUALS': QgsProcessing.TEMPORARY_OUTPUT,
            'CV_SUMMARY': QgsProcessing.TEMPORARY_OUTPUT,
            'PREDICTION': QgsProcessing.TEMPORARY_OUTPUT,
            'VARIANCE': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['KrigoT280'] = processing.run('sagang:ordinarykriging', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # SupErro T1
        alg_params = {
            'BLOCK': False,
            'CV_METHOD': 0,  # [0] none
            'CV_SAMPLES': 10,
            'DBLOCK': 100,
            'FIELD': 'erro',
            'LOG': False,
            'POINTS': outputs['ErrorT1']['OUTPUT'],
            'SEARCH_POINTS_ALL': 1,  # [1] all points within search distance
            'SEARCH_POINTS_MAX': 20,
            'SEARCH_POINTS_MIN': 16,
            'SEARCH_RADIUS': 1000,
            'SEARCH_RANGE': 1,  # [1] global
            'TARGET_USER_SIZE': parameters['definir_tamanho_do_pixel'],
            'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': outputs['ReprojectArea']['OUTPUT'],
            'TQUALITY': 1,  # [1] Variance
            'VAR_MAXDIST': 0,
            'VAR_MODEL': 'a + b * x',
            'VAR_NCLASSES': 100,
            'VAR_NSKIP': 1,
            'CV_RESIDUALS': QgsProcessing.TEMPORARY_OUTPUT,
            'CV_SUMMARY': QgsProcessing.TEMPORARY_OUTPUT,
            'PREDICTION': QgsProcessing.TEMPORARY_OUTPUT,
            'VARIANCE': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SuperroT1'] = processing.run('sagang:ordinarykriging', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # T1
        alg_params = {
            'BAND_A': 1,
            'BAND_B': 1,
            'BAND_C': None,
            'BAND_D': None,
            'BAND_E': None,
            'BAND_F': None,
            'EXTRA': '',
            'FORMULA': 'A+B',
            'INPUT_A': outputs['KrigoT180']['PREDICTION'],
            'INPUT_B': outputs['SuperroT1']['PREDICTION'],
            'INPUT_C': None,
            'INPUT_D': None,
            'INPUT_E': None,
            'INPUT_F': None,
            'NO_DATA': None,
            'OPTIONS': '',
            'RTYPE': 5,  # Float32
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['T1'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # Sample T2
        alg_params = {
            'COLUMN_PREFIX': 'amostra',
            'INPUT': outputs['ExtractT220']['OUTPUT'],
            'RASTERCOPY': outputs['KrigoT280']['PREDICTION'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SampleT2'] = processing.run('native:rastersampling', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # T1_rec
        alg_params = {
            'ALPHA_BAND': False,
            'CROP_TO_CUTLINE': True,
            'DATA_TYPE': 0,  # Use Input Layer Data Type
            'EXTRA': '',
            'INPUT': outputs['T1']['OUTPUT'],
            'KEEP_RESOLUTION': False,
            'MASK': outputs['ReprojectArea']['OUTPUT'],
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'SET_RESOLUTION': False,
            'SOURCE_CRS': parameters['sistema_de_coordenadas_projetadas'],
            'TARGET_CRS': None,
            'X_RESOLUTION': parameters['definir_tamanho_do_pixel'],
            'Y_RESOLUTION': parameters['definir_tamanho_do_pixel'],
            'OUTPUT': parameters['T1']
        }
        outputs['T1_rec'] = processing.run('gdal:cliprasterbymasklayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['T1'] = outputs['T1_rec']['OUTPUT']

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # Erro T2
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'erro',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': ' "variavel" -  "amostra1" ',
            'INPUT': outputs['SampleT2']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ErroT2'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # SupErro T2
        alg_params = {
            'BLOCK': False,
            'CV_METHOD': 0,  # [0] none
            'CV_SAMPLES': 10,
            'DBLOCK': 100,
            'FIELD': 'erro',
            'LOG': False,
            'POINTS': outputs['ErroT2']['OUTPUT'],
            'SEARCH_POINTS_ALL': 1,  # [1] all points within search distance
            'SEARCH_POINTS_MAX': 20,
            'SEARCH_POINTS_MIN': 16,
            'SEARCH_RADIUS': 1000,
            'SEARCH_RANGE': 1,  # [1] global
            'TARGET_USER_SIZE': parameters['definir_tamanho_do_pixel'],
            'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': outputs['ReprojectArea']['OUTPUT'],
            'TQUALITY': 1,  # [1] Variance
            'VAR_MAXDIST': 0,
            'VAR_MODEL': 'a + b * x',
            'VAR_NCLASSES': 100,
            'VAR_NSKIP': 1,
            'CV_RESIDUALS': QgsProcessing.TEMPORARY_OUTPUT,
            'CV_SUMMARY': QgsProcessing.TEMPORARY_OUTPUT,
            'PREDICTION': QgsProcessing.TEMPORARY_OUTPUT,
            'VARIANCE': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SuperroT2'] = processing.run('sagang:ordinarykriging', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(21)
        if feedback.isCanceled():
            return {}

        # T2
        alg_params = {
            'BAND_A': 1,
            'BAND_B': 1,
            'BAND_C': None,
            'BAND_D': None,
            'BAND_E': None,
            'BAND_F': None,
            'EXTRA': '',
            'FORMULA': 'A+B',
            'INPUT_A': outputs['KrigoT280']['PREDICTION'],
            'INPUT_B': outputs['SuperroT2']['PREDICTION'],
            'INPUT_C': None,
            'INPUT_D': None,
            'INPUT_E': None,
            'INPUT_F': None,
            'NO_DATA': None,
            'OPTIONS': '',
            'RTYPE': 5,  # Float32
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['T2'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(22)
        if feedback.isCanceled():
            return {}

        # T2_rec
        alg_params = {
            'ALPHA_BAND': False,
            'CROP_TO_CUTLINE': True,
            'DATA_TYPE': 0,  # Use Input Layer Data Type
            'EXTRA': '',
            'INPUT': outputs['T2']['OUTPUT'],
            'KEEP_RESOLUTION': False,
            'MASK': outputs['ReprojectArea']['OUTPUT'],
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'SET_RESOLUTION': False,
            'SOURCE_CRS': parameters['sistema_de_coordenadas_projetadas'],
            'TARGET_CRS': None,
            'X_RESOLUTION': parameters['definir_tamanho_do_pixel'],
            'Y_RESOLUTION': parameters['definir_tamanho_do_pixel'],
            'OUTPUT': parameters['T2']
        }
        outputs['T2_rec'] = processing.run('gdal:cliprasterbymasklayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['T2'] = outputs['T2_rec']['OUTPUT']

        feedback.setCurrentStep(23)
        if feedback.isCanceled():
            return {}

        # Gain
        alg_params = {
            'BAND_A': 1,
            'BAND_B': 1,
            'BAND_C': None,
            'BAND_D': None,
            'BAND_E': None,
            'BAND_F': None,
            'EXTRA': '',
            'FORMULA': 'B-A',
            'INPUT_A': outputs['T1_rec']['OUTPUT'],
            'INPUT_B': outputs['T2_rec']['OUTPUT'],
            'INPUT_C': None,
            'INPUT_D': None,
            'INPUT_E': None,
            'INPUT_F': None,
            'NO_DATA': None,
            'OPTIONS': '',
            'RTYPE': 5,  # Float32
            'OUTPUT': parameters['Gain']
        }
        outputs['Gain'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Gain'] = outputs['Gain']['OUTPUT']

        feedback.setCurrentStep(24)
        if feedback.isCanceled():
            return {}

        # Raster statistics
        alg_params = {
            'BAND': 1,
            'INPUT': outputs['Gain']['OUTPUT'],
            'OUTPUT_HTML_FILE': parameters['StatisticsOfGain']
        }
        outputs['RasterStatistics'] = processing.run('native:rasterlayerstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['StatisticsOfGain'] = outputs['RasterStatistics']['OUTPUT_HTML_FILE']
        return results

    def name(self):
        return 'GEOTrat - Points'

    def displayName(self):
        return 'GEOTrat - Points'

    def group(self):
        return 'Mestrado'

    def groupId(self):
        return 'Mestrado'

    def shortHelpString(self):
        return """<html><body><p>Mapping tool for agricultural experimentation that allows evaluating the efficiency of one treatment over the other through geostatistics.</p>
<h2>Input parameters</h2>
<h3>Variable measured in the field</h3>
<p>Point-type geometry vector that represents the variable measured in the field.</p>
<h3>Variable field</h3>
<p>Numeric type field that indicates the value measured in the field of the variable of interest. </p>
<h3>Treatment field</h3>
<p>Text type field (T1/T2) that indicates which treatment the measured value belongs to. T1 must be the control treatment and T2 the treatment to be evaluated.</p>
<h3>Study area polygon</h3>
<p>Polygon type geometry vector representing the study area.</p>
<h3>Projected Coordinate System</h3>
<p>Projected coordinate system that the study area is located.</p>
<h3>Pixel size (m)</h3>
<p>Pixel size in meters that will be the spacial resolution of the output surfaces. It is suggested that the value be approximated by the average distance between the entry points.</p>
<h3>Semivariogram model</h3>
<p>Model to be used for the kriging semivariogram. Choose from the options: linear, exponential, gaussian and spherical.</p>
<h2>Outputs</h2>
<h3>T1</h3>
<p>Estimated surface in raster format for the study area, simulating as if the area had been treated entirely with T1.</p>
<h3>T2</h3>
<p>Estimated surface in raster format for the study area, simulating as if the area had been treated entirely with T2.</p>
<h3>Gain</h3>
<p>Surface in raster format that represents the estimated gain of T2 over T1. This surface is in the same unit of measurement as the input data.</p>
<h3>Statistics of gain</h3>
<p>HTML file that contains descriptive statistics for the gain surface.</p>
<br><p align="right">Algorithm author: Xavier, L. C. M. and Martins, G.D. (2023)</p><p align="right">Help author: xavier.lauramoura@gmail.com
deroco@ufu.br</p><p align="right">Algorithm version: 1.0
Developed QGIS version: 3.22.8
Requires installation: SAGA and SAGA Next Gen</p></body></html>"""

    def helpUrl(self):
        return 'to be made available'

    def createInstance(self):
        return GeotratPoints()
