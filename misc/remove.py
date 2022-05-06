import os
import glob
import numpy as np

import requests
  
subjects = os.listdir(r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\BIOMARCADORES_BIDS\derivatives\sovaharmony')
#subjects = os.listdir(r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\SRM')
json_remove = []
for sub in subjects:
    suffix = "sub"
    if sub.endswith(suffix,0,3) == True:
        ses = os.listdir(r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\BIOMARCADORES_BIDS\derivatives\sovaharmony'+'/'+sub)
        #ses = os.listdir(r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\SRM'+'/'+sub)
        for v in ses:
            #icpowers_json_files = glob.glob(r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\SRM'+'/'+sub+'/'+v+'\eeg/*_eeg.edf')
            # icpowers_json_files = glob.glob(r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\BIOMARCADORES_BIDS\derivatives\sovaharmony'+'/'+sub+'/'+v+'\eeg/*]_eeg.fif')
            # json_remove.append(icpowers_json_files)
            # icpowers_json_files = glob.glob(r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\BIOMARCADORES_BIDS\derivatives\sovaharmony'+'/'+sub+'/'+v+'\eeg/*]_eeg.json')
            # json_remove.append(icpowers_json_files)
            # icpowers_json_files = glob.glob(r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\BIOMARCADORES_BIDS\derivatives\sovaharmony'+'/'+sub+'/'+v+'\eeg/*]_stats.txt')
            # json_remove.append(icpowers_json_files)
            # icpowers_json_files = glob.glob(r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\BIOMARCADORES_BIDS\derivatives\sovaharmony'+'/'+sub+'/'+v+'\eeg/*]_stats.json')
            # json_remove.append(icpowers_json_files)

            # icpowers_json_files = glob.glob(r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\BIOMARCADORES_BIDS\derivatives\sovaharmony'+'/'+sub+'/'+v+'\eeg/*]_powers.txt')
            # json_remove.append(icpowers_json_files)
            # icpowers_json_files = glob.glob(r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\BIOMARCADORES_BIDS\derivatives\sovaharmony'+'/'+sub+'/'+v+'\eeg/*]_powers.json')
            # json_remove.append(icpowers_json_files)
            # icpowers_json_files = glob.glob(r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\BIOMARCADORES_BIDS\derivatives\sovaharmony'+'/'+sub+'/'+v+'\eeg/*]_powers.json')
            # json_remove.append(icpowers_json_files)
            # icpowers_json_files = glob.glob(r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\BIOMARCADORES_BIDS\derivatives\sovaharmony'+'/'+sub+'/'+v+'\eeg/*]_powers.txt')
            # json_remove.append(icpowers_json_files)

            icpowers_json_files = glob.glob(r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\BIOMARCADORES_BIDS\derivatives\sovaharmony'+'/'+sub+'/'+v+'\eeg/*norm_eeg.fif')
            json_remove.append(icpowers_json_files)
            icpowers_json_files = glob.glob(r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\BIOMARCADORES_BIDS\derivatives\sovaharmony'+'/'+sub+'/'+v+'\eeg/*norm_eeg.json')
            json_remove.append(icpowers_json_files)
            icpowers_json_files = glob.glob(r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\BIOMARCADORES_BIDS\derivatives\sovaharmony'+'/'+sub+'/'+v+'\eeg/*norm_powers.json')
            json_remove.append(icpowers_json_files)
            icpowers_json_files = glob.glob(r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\BIOMARCADORES_BIDS\derivatives\sovaharmony'+'/'+sub+'/'+v+'\eeg/*norm_powers.txt')
            json_remove.append(icpowers_json_files)
print(json_remove)

    
for i in json_remove:
     for j in range(0,2):
         try:
             print(i[j])
             os.remove(i[j])
         except:
          continue 

