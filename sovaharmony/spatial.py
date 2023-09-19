from scipy.io import loadmat
import sovaflow.utils as us
import matplotlib.pyplot as plt
import os
import numpy as np

F = ['FP1', 'FPZ', 'FP2', 'AF3', 'AF4', 'F7', 'F5', 'F3', 'F1', 'FZ', 'F2', 'F4', 'F6', 'F8'] 
T = ['FT7', 'FC5', 'FC6', 'FT8', 'T7', 'C5', 'C6', 'T8', 'TP7', 'CP5', 'CP6', 'TP8']
C = ['FC3', 'FC1', 'FCZ', 'FC2', 'FC4', 'C3', 'C1', 'CZ', 'C2', 'C4', 'CP3', 'CP1', 'CPZ', 'CP2', 'CP4'] 
PO = ['P7', 'P5', 'P3', 'P1', 'PZ', 'P2', 'P4', 'P6', 'P8', 'PO7', 'PO5', 'PO3', 'POZ', 'PO4', 'PO6', 'PO8', 'CB1', 'O1', 'OZ', 'O2', 'CB2']
ROIs = [F,C,PO,T]

# A ROI COULD BE A SPATIAL FILTER

# TODO: Pass spatial filters to sovaharmony

def get_spatial_filter(name='62x19',portables=False,montage_select=None):
    """
    Returns the default spatial filter of the module.
    Parameters:
        None
    
    Returns:
        A,W tuple of np.ndarrays
        Mixing and Demixing Matrices of the default spatial filter of the module.
    """
    if name is None:
        return None
    # How sure are we that the order of the channels of matlab is the same as of python?
    mat_contents = loadmat(os.path.join(os.path.dirname(os.path.abspath(__file__)),'spatial_filters','spatial_filter__'+name+'.mat'))
    W = mat_contents['W']
    A = mat_contents['A']
    ch_names = [x[0] for x in mat_contents['ch_names'][0,:].tolist()]
    sf = {'A':A,'W':W,'ch_names':ch_names,'name':name}
    if portables:
        channels_reduction={'cresta':['F3','F4','C3','C4','P3','P4','O1','O2'],
                            'openBCI':['FP1','FP2','C3','C4','P7','P8','O2','O1'],# #https://docs.openbci.com/Deprecated/UltracortexMark3_NovaDep/
                            'paper':['F3','F4','C3','C4','TP7','TP8','O1','O2'] # En el paper esta T3 y T4, lo cambiamos por TP7 y TP8
                            # Quantitative electroencephalography in mild cognitive impairment: longitdinal changes and possible prediction of ALzheimer's disease
                            }
        montage_select=montage_select
        sf['ch_names']=[x.replace(' ','') for x in sf['ch_names']]
        index_ch_portables=[sf['ch_names'].index(channels_reduction[montage_select][i]) for i in range(len(channels_reduction['cresta']))]
        comp_select=[0,1,2,3,4,6,7,9]
        A=sf['A'][index_ch_portables,:] # Select channels, rows
        A=A[:,[comp_select]] # Select components, columns
        A=np.squeeze(A)
        W=sf['W'][:,index_ch_portables] # Select channels, rows
        W=W[[comp_select],:] # Select components, columns
        W=np.squeeze(W)
        sf={'A':A,'W':W,'ch_names':channels_reduction[montage_select],'name':montage_select}
        return sf
    else:   
        return sf

def plot_spatial_filter(name='62x19'):
    #ch_names = [us.chn_name_mapping(x) for x in ch_names]
    montage_kind = 'standard_1020'
    A,W,ch_names = get_spatial_filter(name)
    #%% Todas las componentes
    figMany = us.topomap(A,W,ch_names,cmap='seismic',show=False)
    plt.show()
