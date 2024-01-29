"""
Model exported as python.
Name : GEOTrat - Points 1.1
Group : Mestrado
With QGIS : 32208
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterField
from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterCrs
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsProcessingParameterFileDestination
from qgis.core import QgsExpression
import processing


class GeotratPoints11(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('opo_1_varivel_medida_em_campo', 'Variable measured in the field', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterField('campo_da_varivel', 'Variable field', type=QgsProcessingParameterField.Numeric, parentLayerParameterName='opo_1_varivel_medida_em_campo', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterField('campodotratamento', 'Treatment field', type=QgsProcessingParameterField.String, parentLayerParameterName='opo_1_varivel_medida_em_campo', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterEnum('referencetreatment', 'Reference treatment', options=['T1','T2','T3','T4','T5'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0]))
        self.addParameter(QgsProcessingParameterVectorLayer('rea_de_estudo2', 'Study area polygon', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterCrs('sistema_de_coordenadas_projetadas', 'Projected Coordinate System', defaultValue='EPSG:4326'))
        self.addParameter(QgsProcessingParameterNumber('definir_tamanho_do_pixel', 'Pixel size (m)', type=QgsProcessingParameterNumber.Double, minValue=0.1, maxValue=100, defaultValue=None))
        self.addParameter(QgsProcessingParameterEnum('semivariogrammodel', 'Semivariogram model', options=['Linear','Exponential','Gaussian','Spherical'], allowMultiple=False, usesStaticStrings=False, defaultValue=[0]))
        self.addParameter(QgsProcessingParameterNumber('numberoftreatment', 'Number of treatment', type=QgsProcessingParameterNumber.Integer, minValue=2, maxValue=5, defaultValue=2))
        self.addParameter(QgsProcessingParameterRasterDestination('T1', 'T1', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('T2', 'T2', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('T3', 'T3', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('T4', 'T4', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('T5', 'T5', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('GainT2AndT3', 'Gain (T2 and T3)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('GainT2AndT4', 'Gain (T2 and T4)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('GainT2AndT5', 'Gain (T2 and T5)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('GainT3AndT4', 'Gain (T3 and T4)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('GainT3AndT5', 'Gain (T3 and T5)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('GainT4AndT5', 'Gain (T4 and T5)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('GainT1AndT2', 'Gain (T1 and T2)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('GainT1AndT3', 'Gain (T1 and T3)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('GainT1AndT4', 'Gain (T1 and T4)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('GainT1AndT5', 'Gain (T1 and T5)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('StatisticsOfGainT1AndT2', 'Statistics of gain (T1 and T2)', optional=True, fileFilter='HTML files (*.html *.HTML)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('StatisticsOfGainT4AndT5', 'Statistics of gain (T4 and T5)', optional=True, fileFilter='HTML files (*.html *.HTML)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('StatisticsOfGainT1AndT3', 'Statistics of gain (T1 and T3)', optional=True, fileFilter='HTML files (*.html *.HTML)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('StatisticsOfGainT1AndT4', 'Statistics of gain (T1 and T4)', optional=True, fileFilter='HTML files (*.html *.HTML)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('StatisticsOfGainT1AndT5', 'Statistics of gain (T1 and T5)', optional=True, fileFilter='HTML files (*.html *.HTML)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('StatisticsOfGainT2AndT3', 'Statistics of gain (T2 and T3)', optional=True, fileFilter='HTML files (*.html *.HTML)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('StatisticsOfGainT2AndT4', 'Statistics of gain (T2 and T4)', optional=True, fileFilter='HTML files (*.html *.HTML)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('StatisticsOfGainT2AndT5', 'Statistics of gain (T2 and T5)', optional=True, fileFilter='HTML files (*.html *.HTML)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('StatisticsOfGainT3AndT4', 'Statistics of gain (T3 and T4)', optional=True, fileFilter='HTML files (*.html *.HTML)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('StatisticsOfGainT3AndT5', 'Statistics of gain (T3 and T5)', optional=True, fileFilter='HTML files (*.html *.HTML)', createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(77, model_feedback)
        results = {}
        outputs = {}

        # Conditional T4
        alg_params = {
        }
        outputs['ConditionalT4'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

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

        # Conditional T3
        alg_params = {
        }
        outputs['ConditionalT3'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Reproject points
        alg_params = {
            'INPUT': parameters['opo_1_varivel_medida_em_campo'],
            'OPERATION': '',
            'TARGET_CRS': parameters['sistema_de_coordenadas_projetadas'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectPoints'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
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

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Conditional T5
        alg_params = {
        }
        outputs['ConditionalT5'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
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

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Separate T5
        alg_params = {
            'FIELD': 'trat',
            'INPUT': outputs['RenameTreatmentField']['OUTPUT'],
            'OPERATOR': 0,  # =
            'VALUE': 'T5',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SeparateT5'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Separate T3
        alg_params = {
            'FIELD': 'trat',
            'INPUT': outputs['RenameTreatmentField']['OUTPUT'],
            'OPERATOR': 0,  # =
            'VALUE': 'T3',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SeparateT3'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Select T5-80%
        alg_params = {
            'INPUT': outputs['SeparateT5']['OUTPUT'],
            'METHOD': 1,  # Percentage of selected features
            'NUMBER': 80
        }
        outputs['SelectT580'] = processing.run('qgis:randomselection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Extract T5-80%
        alg_params = {
            'INPUT': outputs['SelectT580']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractT580'] = processing.run('native:saveselectedfeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Separate T2
        alg_params = {
            'FIELD': 'trat',
            'INPUT': outputs['RenameTreatmentField']['OUTPUT'],
            'OPERATOR': 0,  # =
            'VALUE': 'T2',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SeparateT2'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Separate T4
        alg_params = {
            'FIELD': 'trat',
            'INPUT': outputs['RenameTreatmentField']['OUTPUT'],
            'OPERATOR': 0,  # =
            'VALUE': 'T4',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SeparateT4'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Select T3-80%
        alg_params = {
            'INPUT': outputs['SeparateT3']['OUTPUT'],
            'METHOD': 1,  # Percentage of selected features
            'NUMBER': 80
        }
        outputs['SelectT380'] = processing.run('qgis:randomselection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Extract T5-20%
        alg_params = {
            'INPUT': outputs['SeparateT5']['OUTPUT'],
            'INTERSECT': outputs['ExtractT580']['OUTPUT'],
            'PREDICATE': [2],  # disjoint
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractT520'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Separate T1
        alg_params = {
            'FIELD': 'trat',
            'INPUT': outputs['RenameTreatmentField']['OUTPUT'],
            'OPERATOR': 0,  # =
            'VALUE': 'T1',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SeparateT1'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Extract T3-80%
        alg_params = {
            'INPUT': outputs['SelectT380']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractT380'] = processing.run('native:saveselectedfeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # Select T1-80%
        alg_params = {
            'INPUT': outputs['SeparateT1']['OUTPUT'],
            'METHOD': 1,  # Percentage of selected features
            'NUMBER': 80
        }
        outputs['SelectT180'] = processing.run('qgis:randomselection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # KrigO - T3-80%
        alg_params = {
            'BLOCK': False,
            'CV_METHOD': 0,  # [0] none
            'CV_SAMPLES': 10,
            'DBLOCK': 100,
            'FIELD': 'variavel',
            'LOG': False,
            'POINTS': outputs['ExtractT380']['OUTPUT'],
            'SEARCH_POINTS_ALL': 1,  # [1] all points within search distance
            'SEARCH_POINTS_MAX': 20,
            'SEARCH_POINTS_MIN': 16,
            'SEARCH_RADIUS': 1000,
            'SEARCH_RANGE': 1,  # [1] global
            'TARGET_USER_FITS': 0,  # [0] nodes
            'TARGET_USER_SIZE': parameters['definir_tamanho_do_pixel'],
            'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': outputs['ReprojectArea']['OUTPUT'],
            'TQUALITY': 1,  # [1] Variance
            'VAR_MAXDIST': 0,
            'VAR_MODEL': QgsExpression("CASE\r\nWHEN  @semivariogrammodel  = '0' THEN 'a + b * x'\r\nWHEN @semivariogrammodel  = '1' THEN 'a + b * (1 - (exp(-x/c)))'\r\nWHEN @semivariogrammodel  = '2' THEN 'a + b * (1 - (exp(-x^2/c^2)))'\r\nWHEN @semivariogrammodel  = '3' THEN 'a + b * ((1.5 * (x/c)) - (0.5 * (x^3/c^3)))'\r\nEND").evaluate(),
            'VAR_NCLASSES': 100,
            'VAR_NSKIP': 1,
            'PREDICTION': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['KrigoT380'] = processing.run('sagang:ordinarykriging', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # Select T2-80%
        alg_params = {
            'INPUT': outputs['SeparateT2']['OUTPUT'],
            'METHOD': 1,  # Percentage of selected features
            'NUMBER': 80
        }
        outputs['SelectT280'] = processing.run('qgis:randomselection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # KrigO - T5-80%
        alg_params = {
            'BLOCK': False,
            'CV_METHOD': 0,  # [0] none
            'CV_SAMPLES': 10,
            'DBLOCK': 100,
            'FIELD': 'variavel',
            'LOG': False,
            'POINTS': outputs['ExtractT580']['OUTPUT'],
            'SEARCH_POINTS_ALL': 1,  # [1] all points within search distance
            'SEARCH_POINTS_MAX': 20,
            'SEARCH_POINTS_MIN': 16,
            'SEARCH_RADIUS': 1000,
            'SEARCH_RANGE': 1,  # [1] global
            'TARGET_USER_FITS': 0,  # [0] nodes
            'TARGET_USER_SIZE': parameters['definir_tamanho_do_pixel'],
            'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': outputs['ReprojectArea']['OUTPUT'],
            'TQUALITY': 1,  # [1] Variance
            'VAR_MAXDIST': 0,
            'VAR_MODEL': QgsExpression("CASE\r\nWHEN  @semivariogrammodel  = '0' THEN 'a + b * x'\r\nWHEN @semivariogrammodel  = '1' THEN 'a + b * (1 - (exp(-x/c)))'\r\nWHEN @semivariogrammodel  = '2' THEN 'a + b * (1 - (exp(-x^2/c^2)))'\r\nWHEN @semivariogrammodel  = '3' THEN 'a + b * ((1.5 * (x/c)) - (0.5 * (x^3/c^3)))'\r\nEND").evaluate(),
            'VAR_NCLASSES': 100,
            'VAR_NSKIP': 1,
            'PREDICTION': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['KrigoT580'] = processing.run('sagang:ordinarykriging', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(21)
        if feedback.isCanceled():
            return {}

        # Select T4-80%
        alg_params = {
            'INPUT': outputs['SeparateT4']['OUTPUT'],
            'METHOD': 1,  # Percentage of selected features
            'NUMBER': 80
        }
        outputs['SelectT480'] = processing.run('qgis:randomselection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(22)
        if feedback.isCanceled():
            return {}

        # Extract T3-20%
        alg_params = {
            'INPUT': outputs['SeparateT3']['OUTPUT'],
            'INTERSECT': outputs['ExtractT380']['OUTPUT'],
            'PREDICATE': [2],  # disjoint
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractT320'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(23)
        if feedback.isCanceled():
            return {}

        # Extract T4-80%
        alg_params = {
            'INPUT': outputs['SelectT480']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractT480'] = processing.run('native:saveselectedfeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(24)
        if feedback.isCanceled():
            return {}

        # Extract T1-80%
        alg_params = {
            'INPUT': outputs['SelectT180']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractT180'] = processing.run('native:saveselectedfeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(25)
        if feedback.isCanceled():
            return {}

        # Sample T3
        alg_params = {
            'COLUMN_PREFIX': 'amostra',
            'INPUT': outputs['ExtractT320']['OUTPUT'],
            'RASTERCOPY': outputs['KrigoT380']['PREDICTION'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SampleT3'] = processing.run('native:rastersampling', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(26)
        if feedback.isCanceled():
            return {}

        # Erro T3
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'erro',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': ' "variavel" -  "amostra1" ',
            'INPUT': outputs['SampleT3']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ErroT3'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(27)
        if feedback.isCanceled():
            return {}

        # Extract T2-80%
        alg_params = {
            'INPUT': outputs['SelectT280']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractT280'] = processing.run('native:saveselectedfeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(28)
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
            'TARGET_USER_FITS': 0,  # [0] nodes
            'TARGET_USER_SIZE': parameters['definir_tamanho_do_pixel'],
            'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': outputs['ReprojectArea']['OUTPUT'],
            'TQUALITY': 1,  # [1] Variance
            'VAR_MAXDIST': 0,
            'VAR_MODEL': QgsExpression("CASE\r\nWHEN  @semivariogrammodel  = '0' THEN 'a + b * x'\r\nWHEN @semivariogrammodel  = '1' THEN 'a + b * (1 - (exp(-x/c)))'\r\nWHEN @semivariogrammodel  = '2' THEN 'a + b * (1 - (exp(-x^2/c^2)))'\r\nWHEN @semivariogrammodel  = '3' THEN 'a + b * ((1.5 * (x/c)) - (0.5 * (x^3/c^3)))'\r\nEND").evaluate(),
            'VAR_NCLASSES': 100,
            'VAR_NSKIP': 1,
            'PREDICTION': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['KrigoT280'] = processing.run('sagang:ordinarykriging', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(29)
        if feedback.isCanceled():
            return {}

        # Sample T5
        alg_params = {
            'COLUMN_PREFIX': 'amostra',
            'INPUT': outputs['ExtractT520']['OUTPUT'],
            'RASTERCOPY': outputs['KrigoT580']['PREDICTION'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SampleT5'] = processing.run('native:rastersampling', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(30)
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
            'TARGET_USER_FITS': 0,  # [0] nodes
            'TARGET_USER_SIZE': parameters['definir_tamanho_do_pixel'],
            'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': outputs['ReprojectArea']['OUTPUT'],
            'TQUALITY': 1,  # [1] Variance
            'VAR_MAXDIST': 0,
            'VAR_MODEL': QgsExpression("CASE\r\nWHEN  @semivariogrammodel  = '0' THEN 'a + b * x'\r\nWHEN @semivariogrammodel  = '1' THEN 'a + b * (1 - (exp(-x/c)))'\r\nWHEN @semivariogrammodel  = '2' THEN 'a + b * (1 - (exp(-x^2/c^2)))'\r\nWHEN @semivariogrammodel  = '3' THEN 'a + b * ((1.5 * (x/c)) - (0.5 * (x^3/c^3)))'\r\nEND").evaluate(),
            'VAR_NCLASSES': 100,
            'VAR_NSKIP': 1,
            'PREDICTION': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['KrigoT180'] = processing.run('sagang:ordinarykriging', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(31)
        if feedback.isCanceled():
            return {}

        # Extract T4-20%
        alg_params = {
            'INPUT': outputs['SeparateT4']['OUTPUT'],
            'INTERSECT': outputs['ExtractT480']['OUTPUT'],
            'PREDICATE': [2],  # disjoint
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractT420'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(32)
        if feedback.isCanceled():
            return {}

        # KrigO - T4-80%
        alg_params = {
            'BLOCK': False,
            'CV_METHOD': 0,  # [0] none
            'CV_SAMPLES': 10,
            'DBLOCK': 100,
            'FIELD': 'variavel',
            'LOG': False,
            'POINTS': outputs['ExtractT480']['OUTPUT'],
            'SEARCH_POINTS_ALL': 1,  # [1] all points within search distance
            'SEARCH_POINTS_MAX': 20,
            'SEARCH_POINTS_MIN': 16,
            'SEARCH_RADIUS': 1000,
            'SEARCH_RANGE': 1,  # [1] global
            'TARGET_USER_FITS': 0,  # [0] nodes
            'TARGET_USER_SIZE': parameters['definir_tamanho_do_pixel'],
            'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': outputs['ReprojectArea']['OUTPUT'],
            'TQUALITY': 1,  # [1] Variance
            'VAR_MAXDIST': 0,
            'VAR_MODEL': QgsExpression("CASE\r\nWHEN  @semivariogrammodel  = '0' THEN 'a + b * x'\r\nWHEN @semivariogrammodel  = '1' THEN 'a + b * (1 - (exp(-x/c)))'\r\nWHEN @semivariogrammodel  = '2' THEN 'a + b * (1 - (exp(-x^2/c^2)))'\r\nWHEN @semivariogrammodel  = '3' THEN 'a + b * ((1.5 * (x/c)) - (0.5 * (x^3/c^3)))'\r\nEND").evaluate(),
            'VAR_NCLASSES': 100,
            'VAR_NSKIP': 1,
            'PREDICTION': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['KrigoT480'] = processing.run('sagang:ordinarykriging', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(33)
        if feedback.isCanceled():
            return {}

        # SupErro T3
        alg_params = {
            'BLOCK': False,
            'CV_METHOD': 0,  # [0] none
            'CV_SAMPLES': 10,
            'DBLOCK': 100,
            'FIELD': 'erro',
            'LOG': False,
            'POINTS': outputs['ErroT3']['OUTPUT'],
            'SEARCH_POINTS_ALL': 1,  # [1] all points within search distance
            'SEARCH_POINTS_MAX': 20,
            'SEARCH_POINTS_MIN': 16,
            'SEARCH_RADIUS': 1000,
            'SEARCH_RANGE': 1,  # [1] global
            'TARGET_USER_FITS': 0,  # [0] nodes
            'TARGET_USER_SIZE': parameters['definir_tamanho_do_pixel'],
            'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': outputs['ReprojectArea']['OUTPUT'],
            'TQUALITY': 1,  # [1] Variance
            'VAR_MAXDIST': 0,
            'VAR_MODEL': 'a + b * x',
            'VAR_NCLASSES': 100,
            'VAR_NSKIP': 1,
            'PREDICTION': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SuperroT3'] = processing.run('sagang:ordinarykriging', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(34)
        if feedback.isCanceled():
            return {}

        # Extract T1-20%
        alg_params = {
            'INPUT': outputs['SeparateT1']['OUTPUT'],
            'INTERSECT': outputs['ExtractT180']['OUTPUT'],
            'PREDICATE': [2],  # disjoint
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractT120'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(35)
        if feedback.isCanceled():
            return {}

        # Extract T2-20%
        alg_params = {
            'INPUT': outputs['SeparateT2']['OUTPUT'],
            'INTERSECT': outputs['ExtractT280']['OUTPUT'],
            'PREDICATE': [2],  # disjoint
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractT220'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(36)
        if feedback.isCanceled():
            return {}

        # Erro T5
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'erro',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': ' "variavel" -  "amostra1" ',
            'INPUT': outputs['SampleT5']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ErroT5'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(37)
        if feedback.isCanceled():
            return {}

        # SupErro T5
        alg_params = {
            'BLOCK': False,
            'CV_METHOD': 0,  # [0] none
            'CV_SAMPLES': 10,
            'DBLOCK': 100,
            'FIELD': 'erro',
            'LOG': False,
            'POINTS': outputs['ErroT5']['OUTPUT'],
            'SEARCH_POINTS_ALL': 1,  # [1] all points within search distance
            'SEARCH_POINTS_MAX': 20,
            'SEARCH_POINTS_MIN': 16,
            'SEARCH_RADIUS': 1000,
            'SEARCH_RANGE': 1,  # [1] global
            'TARGET_USER_FITS': 0,  # [0] nodes
            'TARGET_USER_SIZE': parameters['definir_tamanho_do_pixel'],
            'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': outputs['ReprojectArea']['OUTPUT'],
            'TQUALITY': 1,  # [1] Variance
            'VAR_MAXDIST': 0,
            'VAR_MODEL': 'a + b * x',
            'VAR_NCLASSES': 100,
            'VAR_NSKIP': 1,
            'PREDICTION': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SuperroT5'] = processing.run('sagang:ordinarykriging', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(38)
        if feedback.isCanceled():
            return {}

        # Sample T4
        alg_params = {
            'COLUMN_PREFIX': 'amostra',
            'INPUT': outputs['ExtractT420']['OUTPUT'],
            'RASTERCOPY': outputs['KrigoT480']['PREDICTION'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SampleT4'] = processing.run('native:rastersampling', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(39)
        if feedback.isCanceled():
            return {}

        # T5
        alg_params = {
            'BAND_A': 1,
            'BAND_B': 1,
            'BAND_C': None,
            'BAND_D': None,
            'BAND_E': None,
            'BAND_F': None,
            'EXTRA': '',
            'FORMULA': 'A+B',
            'INPUT_A': outputs['KrigoT580']['PREDICTION'],
            'INPUT_B': outputs['SuperroT5']['PREDICTION'],
            'INPUT_C': None,
            'INPUT_D': None,
            'INPUT_E': None,
            'INPUT_F': None,
            'NO_DATA': None,
            'OPTIONS': '',
            'RTYPE': 5,  # Float32
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['T5'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(40)
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

        feedback.setCurrentStep(41)
        if feedback.isCanceled():
            return {}

        # Erro T4
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'erro',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': ' "variavel" -  "amostra1" ',
            'INPUT': outputs['SampleT4']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ErroT4'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(42)
        if feedback.isCanceled():
            return {}

        # SupErro T4
        alg_params = {
            'BLOCK': False,
            'CV_METHOD': 0,  # [0] none
            'CV_SAMPLES': 10,
            'DBLOCK': 100,
            'FIELD': 'erro',
            'LOG': False,
            'POINTS': outputs['ErroT4']['OUTPUT'],
            'SEARCH_POINTS_ALL': 1,  # [1] all points within search distance
            'SEARCH_POINTS_MAX': 20,
            'SEARCH_POINTS_MIN': 16,
            'SEARCH_RADIUS': 1000,
            'SEARCH_RANGE': 1,  # [1] global
            'TARGET_USER_FITS': 0,  # [0] nodes
            'TARGET_USER_SIZE': parameters['definir_tamanho_do_pixel'],
            'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': outputs['ReprojectArea']['OUTPUT'],
            'TQUALITY': 1,  # [1] Variance
            'VAR_MAXDIST': 0,
            'VAR_MODEL': 'a + b * x',
            'VAR_NCLASSES': 100,
            'VAR_NSKIP': 1,
            'PREDICTION': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SuperroT4'] = processing.run('sagang:ordinarykriging', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(43)
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

        feedback.setCurrentStep(44)
        if feedback.isCanceled():
            return {}

        # T5_rec
        alg_params = {
            'ALPHA_BAND': False,
            'CROP_TO_CUTLINE': True,
            'DATA_TYPE': 0,  # Use Input Layer Data Type
            'EXTRA': '',
            'INPUT': outputs['T5']['OUTPUT'],
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
            'OUTPUT': parameters['T5']
        }
        outputs['T5_rec'] = processing.run('gdal:cliprasterbymasklayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['T5'] = outputs['T5_rec']['OUTPUT']

        feedback.setCurrentStep(45)
        if feedback.isCanceled():
            return {}

        # T3
        alg_params = {
            'BAND_A': 1,
            'BAND_B': 1,
            'BAND_C': None,
            'BAND_D': None,
            'BAND_E': None,
            'BAND_F': None,
            'EXTRA': '',
            'FORMULA': 'A+B',
            'INPUT_A': outputs['KrigoT380']['PREDICTION'],
            'INPUT_B': outputs['SuperroT3']['PREDICTION'],
            'INPUT_C': None,
            'INPUT_D': None,
            'INPUT_E': None,
            'INPUT_F': None,
            'NO_DATA': None,
            'OPTIONS': '',
            'RTYPE': 5,  # Float32
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['T3'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(46)
        if feedback.isCanceled():
            return {}

        # T3_rec
        alg_params = {
            'ALPHA_BAND': False,
            'CROP_TO_CUTLINE': True,
            'DATA_TYPE': 0,  # Use Input Layer Data Type
            'EXTRA': '',
            'INPUT': outputs['T3']['OUTPUT'],
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
            'OUTPUT': parameters['T3']
        }
        outputs['T3_rec'] = processing.run('gdal:cliprasterbymasklayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['T3'] = outputs['T3_rec']['OUTPUT']

        feedback.setCurrentStep(47)
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

        feedback.setCurrentStep(48)
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
            'TARGET_USER_FITS': 0,  # [0] nodes
            'TARGET_USER_SIZE': parameters['definir_tamanho_do_pixel'],
            'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': outputs['ReprojectArea']['OUTPUT'],
            'TQUALITY': 1,  # [1] Variance
            'VAR_MAXDIST': 0,
            'VAR_MODEL': 'a + b * x',
            'VAR_NCLASSES': 100,
            'VAR_NSKIP': 1,
            'PREDICTION': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SuperroT2'] = processing.run('sagang:ordinarykriging', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(49)
        if feedback.isCanceled():
            return {}

        # T4
        alg_params = {
            'BAND_A': 1,
            'BAND_B': 1,
            'BAND_C': None,
            'BAND_D': None,
            'BAND_E': None,
            'BAND_F': None,
            'EXTRA': '',
            'FORMULA': 'A+B',
            'INPUT_A': outputs['KrigoT480']['PREDICTION'],
            'INPUT_B': outputs['SuperroT4']['PREDICTION'],
            'INPUT_C': None,
            'INPUT_D': None,
            'INPUT_E': None,
            'INPUT_F': None,
            'NO_DATA': None,
            'OPTIONS': '',
            'RTYPE': 5,  # Float32
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['T4'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(50)
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

        feedback.setCurrentStep(51)
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
            'TARGET_USER_FITS': 0,  # [0] nodes
            'TARGET_USER_SIZE': parameters['definir_tamanho_do_pixel'],
            'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': outputs['ReprojectArea']['OUTPUT'],
            'TQUALITY': 1,  # [1] Variance
            'VAR_MAXDIST': 0,
            'VAR_MODEL': 'a + b * x',
            'VAR_NCLASSES': 100,
            'VAR_NSKIP': 1,
            'PREDICTION': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SuperroT1'] = processing.run('sagang:ordinarykriging', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(52)
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

        feedback.setCurrentStep(53)
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

        feedback.setCurrentStep(54)
        if feedback.isCanceled():
            return {}

        # T4_rec
        alg_params = {
            'ALPHA_BAND': False,
            'CROP_TO_CUTLINE': True,
            'DATA_TYPE': 0,  # Use Input Layer Data Type
            'EXTRA': '',
            'INPUT': outputs['T4']['OUTPUT'],
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
            'OUTPUT': parameters['T4']
        }
        outputs['T4_rec'] = processing.run('gdal:cliprasterbymasklayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['T4'] = outputs['T4_rec']['OUTPUT']

        feedback.setCurrentStep(55)
        if feedback.isCanceled():
            return {}

        # Gain 9
        alg_params = {
            'BAND_A': 1,
            'BAND_B': 1,
            'BAND_C': None,
            'BAND_D': None,
            'BAND_E': None,
            'BAND_F': None,
            'EXTRA': '',
            'FORMULA': QgsExpression("CASE\r\nWHEN   @referencetreatment   = '2' THEN 'A-B'\r\nWHEN   @referencetreatment   = '4' THEN 'B-A'\r\nEND").evaluate(),
            'INPUT_A': outputs['T3_rec']['OUTPUT'],
            'INPUT_B': outputs['T5_rec']['OUTPUT'],
            'INPUT_C': None,
            'INPUT_D': None,
            'INPUT_E': None,
            'INPUT_F': None,
            'NO_DATA': None,
            'OPTIONS': '',
            'RTYPE': 5,  # Float32
            'OUTPUT': parameters['GainT3AndT5']
        }
        outputs['Gain9'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['GainT3AndT5'] = outputs['Gain9']['OUTPUT']

        feedback.setCurrentStep(56)
        if feedback.isCanceled():
            return {}

        # Gain 8
        alg_params = {
            'BAND_A': 1,
            'BAND_B': 1,
            'BAND_C': None,
            'BAND_D': None,
            'BAND_E': None,
            'BAND_F': None,
            'EXTRA': '',
            'FORMULA': QgsExpression("CASE\r\nWHEN   @referencetreatment   = '2' THEN 'A-B'\r\nWHEN   @referencetreatment   = '3' THEN 'B-A'\r\nEND").evaluate(),
            'INPUT_A': outputs['T3_rec']['OUTPUT'],
            'INPUT_B': outputs['T4_rec']['OUTPUT'],
            'INPUT_C': None,
            'INPUT_D': None,
            'INPUT_E': None,
            'INPUT_F': None,
            'NO_DATA': None,
            'OPTIONS': '',
            'RTYPE': 5,  # Float32
            'OUTPUT': parameters['GainT3AndT4']
        }
        outputs['Gain8'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['GainT3AndT4'] = outputs['Gain8']['OUTPUT']

        feedback.setCurrentStep(57)
        if feedback.isCanceled():
            return {}

        # Gain 10
        alg_params = {
            'BAND_A': 1,
            'BAND_B': 1,
            'BAND_C': None,
            'BAND_D': None,
            'BAND_E': None,
            'BAND_F': None,
            'EXTRA': '',
            'FORMULA': QgsExpression("CASE\r\nWHEN   @referencetreatment   = '3' THEN 'A-B'\r\nWHEN   @referencetreatment   = '4' THEN 'B-A'\r\nEND").evaluate(),
            'INPUT_A': outputs['T4_rec']['OUTPUT'],
            'INPUT_B': outputs['T5_rec']['OUTPUT'],
            'INPUT_C': None,
            'INPUT_D': None,
            'INPUT_E': None,
            'INPUT_F': None,
            'NO_DATA': None,
            'OPTIONS': '',
            'RTYPE': 5,  # Float32
            'OUTPUT': parameters['GainT4AndT5']
        }
        outputs['Gain10'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['GainT4AndT5'] = outputs['Gain10']['OUTPUT']

        feedback.setCurrentStep(58)
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

        feedback.setCurrentStep(59)
        if feedback.isCanceled():
            return {}

        # Gain 2
        alg_params = {
            'BAND_A': 1,
            'BAND_B': 1,
            'BAND_C': None,
            'BAND_D': None,
            'BAND_E': None,
            'BAND_F': None,
            'EXTRA': '',
            'FORMULA': QgsExpression("CASE\r\nWHEN   @referencetreatment   = '0' THEN 'A-B'\r\nWHEN   @referencetreatment   = '2' THEN 'B-A'\r\nEND").evaluate(),
            'INPUT_A': outputs['T1_rec']['OUTPUT'],
            'INPUT_B': outputs['T3_rec']['OUTPUT'],
            'INPUT_C': None,
            'INPUT_D': None,
            'INPUT_E': None,
            'INPUT_F': None,
            'NO_DATA': None,
            'OPTIONS': '',
            'RTYPE': 5,  # Float32
            'OUTPUT': parameters['GainT1AndT3']
        }
        outputs['Gain2'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['GainT1AndT3'] = outputs['Gain2']['OUTPUT']

        feedback.setCurrentStep(60)
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

        feedback.setCurrentStep(61)
        if feedback.isCanceled():
            return {}

        # Gain 7
        alg_params = {
            'BAND_A': 1,
            'BAND_B': 1,
            'BAND_C': None,
            'BAND_D': None,
            'BAND_E': None,
            'BAND_F': None,
            'EXTRA': '',
            'FORMULA': QgsExpression("CASE\r\nWHEN   @referencetreatment   = '1' THEN 'A-B'\r\nWHEN   @referencetreatment   = '4' THEN 'B-A'\r\nEND").evaluate(),
            'INPUT_A': outputs['T2_rec']['OUTPUT'],
            'INPUT_B': outputs['T5_rec']['OUTPUT'],
            'INPUT_C': None,
            'INPUT_D': None,
            'INPUT_E': None,
            'INPUT_F': None,
            'NO_DATA': None,
            'OPTIONS': '',
            'RTYPE': 5,  # Float32
            'OUTPUT': parameters['GainT2AndT5']
        }
        outputs['Gain7'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['GainT2AndT5'] = outputs['Gain7']['OUTPUT']

        feedback.setCurrentStep(62)
        if feedback.isCanceled():
            return {}

        # Stats (T4 and T5)
        alg_params = {
            'BAND': 1,
            'INPUT': outputs['Gain10']['OUTPUT'],
            'OUTPUT_HTML_FILE': parameters['StatisticsOfGainT4AndT5']
        }
        outputs['StatsT4AndT5'] = processing.run('native:rasterlayerstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['StatisticsOfGainT4AndT5'] = outputs['StatsT4AndT5']['OUTPUT_HTML_FILE']

        feedback.setCurrentStep(63)
        if feedback.isCanceled():
            return {}

        # Gain 1
        alg_params = {
            'BAND_A': 1,
            'BAND_B': 1,
            'BAND_C': None,
            'BAND_D': None,
            'BAND_E': None,
            'BAND_F': None,
            'EXTRA': '',
            'FORMULA': QgsExpression("CASE\r\nWHEN   @referencetreatment   = '0' THEN 'A-B'\r\nWHEN   @referencetreatment   = '1' THEN 'B-A'\r\nEND").evaluate(),
            'INPUT_A': outputs['T1_rec']['OUTPUT'],
            'INPUT_B': outputs['T2_rec']['OUTPUT'],
            'INPUT_C': None,
            'INPUT_D': None,
            'INPUT_E': None,
            'INPUT_F': None,
            'NO_DATA': None,
            'OPTIONS': '',
            'RTYPE': 5,  # Float32
            'OUTPUT': parameters['GainT1AndT2']
        }
        outputs['Gain1'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['GainT1AndT2'] = outputs['Gain1']['OUTPUT']

        feedback.setCurrentStep(64)
        if feedback.isCanceled():
            return {}

        # Stats (T3 and T5)
        alg_params = {
            'BAND': 1,
            'INPUT': outputs['Gain9']['OUTPUT'],
            'OUTPUT_HTML_FILE': parameters['StatisticsOfGainT3AndT5']
        }
        outputs['StatsT3AndT5'] = processing.run('native:rasterlayerstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['StatisticsOfGainT3AndT5'] = outputs['StatsT3AndT5']['OUTPUT_HTML_FILE']

        feedback.setCurrentStep(65)
        if feedback.isCanceled():
            return {}

        # Gain 5
        alg_params = {
            'BAND_A': 1,
            'BAND_B': 1,
            'BAND_C': None,
            'BAND_D': None,
            'BAND_E': None,
            'BAND_F': None,
            'EXTRA': '',
            'FORMULA': QgsExpression("CASE\r\nWHEN   @referencetreatment   = '1' THEN 'A-B'\r\nWHEN   @referencetreatment   = '2' THEN 'B-A'\r\nEND").evaluate(),
            'INPUT_A': outputs['T2_rec']['OUTPUT'],
            'INPUT_B': outputs['T3_rec']['OUTPUT'],
            'INPUT_C': None,
            'INPUT_D': None,
            'INPUT_E': None,
            'INPUT_F': None,
            'NO_DATA': None,
            'OPTIONS': '',
            'RTYPE': 5,  # Float32
            'OUTPUT': parameters['GainT2AndT3']
        }
        outputs['Gain5'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['GainT2AndT3'] = outputs['Gain5']['OUTPUT']

        feedback.setCurrentStep(66)
        if feedback.isCanceled():
            return {}

        # Stats (T3 and T4)
        alg_params = {
            'BAND': 1,
            'INPUT': outputs['Gain8']['OUTPUT'],
            'OUTPUT_HTML_FILE': parameters['StatisticsOfGainT3AndT4']
        }
        outputs['StatsT3AndT4'] = processing.run('native:rasterlayerstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['StatisticsOfGainT3AndT4'] = outputs['StatsT3AndT4']['OUTPUT_HTML_FILE']

        feedback.setCurrentStep(67)
        if feedback.isCanceled():
            return {}

        # Stats (T1 and T2)
        alg_params = {
            'BAND': 1,
            'INPUT': outputs['Gain1']['OUTPUT'],
            'OUTPUT_HTML_FILE': parameters['StatisticsOfGainT1AndT2']
        }
        outputs['StatsT1AndT2'] = processing.run('native:rasterlayerstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['StatisticsOfGainT1AndT2'] = outputs['StatsT1AndT2']['OUTPUT_HTML_FILE']

        feedback.setCurrentStep(68)
        if feedback.isCanceled():
            return {}

        # Stats (T2 and T5)
        alg_params = {
            'BAND': 1,
            'INPUT': outputs['Gain7']['OUTPUT'],
            'OUTPUT_HTML_FILE': parameters['StatisticsOfGainT2AndT5']
        }
        outputs['StatsT2AndT5'] = processing.run('native:rasterlayerstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['StatisticsOfGainT2AndT5'] = outputs['StatsT2AndT5']['OUTPUT_HTML_FILE']

        feedback.setCurrentStep(69)
        if feedback.isCanceled():
            return {}

        # Gain 4
        alg_params = {
            'BAND_A': 1,
            'BAND_B': 1,
            'BAND_C': None,
            'BAND_D': None,
            'BAND_E': None,
            'BAND_F': None,
            'EXTRA': '',
            'FORMULA': QgsExpression("CASE\r\nWHEN   @referencetreatment   = '0' THEN 'A-B'\r\nWHEN   @referencetreatment   = '4' THEN 'B-A'\r\nEND").evaluate(),
            'INPUT_A': outputs['T1_rec']['OUTPUT'],
            'INPUT_B': outputs['T5_rec']['OUTPUT'],
            'INPUT_C': None,
            'INPUT_D': None,
            'INPUT_E': None,
            'INPUT_F': None,
            'NO_DATA': None,
            'OPTIONS': '',
            'RTYPE': 5,  # Float32
            'OUTPUT': parameters['GainT1AndT5']
        }
        outputs['Gain4'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['GainT1AndT5'] = outputs['Gain4']['OUTPUT']

        feedback.setCurrentStep(70)
        if feedback.isCanceled():
            return {}

        # Stats (T1 and T3)
        alg_params = {
            'BAND': 1,
            'INPUT': outputs['Gain2']['OUTPUT'],
            'OUTPUT_HTML_FILE': parameters['StatisticsOfGainT1AndT3']
        }
        outputs['StatsT1AndT3'] = processing.run('native:rasterlayerstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['StatisticsOfGainT1AndT3'] = outputs['StatsT1AndT3']['OUTPUT_HTML_FILE']

        feedback.setCurrentStep(71)
        if feedback.isCanceled():
            return {}

        # Gain 6
        alg_params = {
            'BAND_A': 1,
            'BAND_B': 1,
            'BAND_C': None,
            'BAND_D': None,
            'BAND_E': None,
            'BAND_F': None,
            'EXTRA': '',
            'FORMULA': QgsExpression("CASE\r\nWHEN   @referencetreatment   = '1' THEN 'A-B'\r\nWHEN   @referencetreatment   = '3' THEN 'B-A'\r\nEND").evaluate(),
            'INPUT_A': outputs['T2_rec']['OUTPUT'],
            'INPUT_B': outputs['T4_rec']['OUTPUT'],
            'INPUT_C': None,
            'INPUT_D': None,
            'INPUT_E': None,
            'INPUT_F': None,
            'NO_DATA': None,
            'OPTIONS': '',
            'RTYPE': 5,  # Float32
            'OUTPUT': parameters['GainT2AndT4']
        }
        outputs['Gain6'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['GainT2AndT4'] = outputs['Gain6']['OUTPUT']

        feedback.setCurrentStep(72)
        if feedback.isCanceled():
            return {}

        # Gain 3
        alg_params = {
            'BAND_A': 1,
            'BAND_B': 1,
            'BAND_C': None,
            'BAND_D': None,
            'BAND_E': None,
            'BAND_F': None,
            'EXTRA': '',
            'FORMULA': QgsExpression("CASE\r\nWHEN   @referencetreatment   = '0' THEN 'A-B'\r\nWHEN   @referencetreatment   = '3' THEN 'B-A'\r\nEND").evaluate(),
            'INPUT_A': outputs['T1_rec']['OUTPUT'],
            'INPUT_B': outputs['T4_rec']['OUTPUT'],
            'INPUT_C': None,
            'INPUT_D': None,
            'INPUT_E': None,
            'INPUT_F': None,
            'NO_DATA': None,
            'OPTIONS': '',
            'RTYPE': 5,  # Float32
            'OUTPUT': parameters['GainT1AndT4']
        }
        outputs['Gain3'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['GainT1AndT4'] = outputs['Gain3']['OUTPUT']

        feedback.setCurrentStep(73)
        if feedback.isCanceled():
            return {}

        # Stats (T2 and T4)
        alg_params = {
            'BAND': 1,
            'INPUT': outputs['Gain6']['OUTPUT'],
            'OUTPUT_HTML_FILE': parameters['StatisticsOfGainT2AndT4']
        }
        outputs['StatsT2AndT4'] = processing.run('native:rasterlayerstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['StatisticsOfGainT2AndT4'] = outputs['StatsT2AndT4']['OUTPUT_HTML_FILE']

        feedback.setCurrentStep(74)
        if feedback.isCanceled():
            return {}

        # Stats (T2 and T3)
        alg_params = {
            'BAND': 1,
            'INPUT': outputs['Gain5']['OUTPUT'],
            'OUTPUT_HTML_FILE': parameters['StatisticsOfGainT2AndT3']
        }
        outputs['StatsT2AndT3'] = processing.run('native:rasterlayerstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['StatisticsOfGainT2AndT3'] = outputs['StatsT2AndT3']['OUTPUT_HTML_FILE']

        feedback.setCurrentStep(75)
        if feedback.isCanceled():
            return {}

        # Stats (T1 and T5)
        alg_params = {
            'BAND': 1,
            'INPUT': outputs['Gain4']['OUTPUT'],
            'OUTPUT_HTML_FILE': parameters['StatisticsOfGainT1AndT5']
        }
        outputs['StatsT1AndT5'] = processing.run('native:rasterlayerstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['StatisticsOfGainT1AndT5'] = outputs['StatsT1AndT5']['OUTPUT_HTML_FILE']

        feedback.setCurrentStep(76)
        if feedback.isCanceled():
            return {}

        # Stats (T1 and T4)
        alg_params = {
            'BAND': 1,
            'INPUT': outputs['Gain3']['OUTPUT'],
            'OUTPUT_HTML_FILE': parameters['StatisticsOfGainT1AndT4']
        }
        outputs['StatsT1AndT4'] = processing.run('native:rasterlayerstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['StatisticsOfGainT1AndT4'] = outputs['StatsT1AndT4']['OUTPUT_HTML_FILE']
        return results

    def name(self):
        return 'GEOTrat - Points 1.1'

    def displayName(self):
        return 'GEOTrat - Points 1.1'

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
<h3>Reference treatment</h3>
<p>Select reference treatment, if you select T1, the gain will be calculated as T1 - T2, if you select T2, the gain will be calculated as T2 - T1.</p>
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
<br><p align="right">Algorithm author: Xavier, L. C. M. and Martins, G.D. (2023)</p><p align="right">Help author: xavier.lauramoura@gmail.com
deroco@ufu.br</p><p align="right">Algorithm version: 1.0
Developed QGIS version: 3.22.8
Requires installation: SAGA and SAGA Next Gen</p></body></html>"""

    def helpUrl(self):
        return 'to be made available'

    def createInstance(self):
        return GeotratPoints11()
