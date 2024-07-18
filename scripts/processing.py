
#This script contains the functions used to transform spectra prior to computing similarity scores

import scipy.stats
import numpy as np

def wf_transform(spec_mzs, spec_ints, wf_mz, wf_int):
    #This function performs a weight factor transformation on a spectrum
    
    #input:
    #wf_int: float
    #wf_mz: float
    #spec_mzs: 1d np array representing mass/charge values 
    #spec_ints: 1d np array representing intensity values 

    #spec_mzs and spec_ints must be of the same length N

    #output:
    #spec_ints: 1d np array of weight-factor-transformed spectrum intensities

    spec_ints = np.power(spec_mzs, wf_mz) * np.power(spec_ints, wf_int)
    return(spec_ints)


def LE_transform(intensity, thresh, normalization_method):
    #This transformation was presented by: 
    #Li, Y.; Kind, T.; Folz, J.; Vaniya, A.; Mehta, S. S.; Fiehn, O.
    #Spectral entropy outperforms MS/MS dot product similarity for small-molecule compound identification. 
    #Nature Methods 2021, 18, 1524–1531
    
    #input:
    #intensity: 1d np array
    #thresh: nonnegative float
    #normalization_method: either 'standard' or 'softmax'
    
    #output:
    #1d np array of transformed intensities

    intensity_tmp = normalize(intensity, method=normalization_method)
    S = scipy.stats.entropy(intensity_tmp.astype('float'))
    if S > 0 and S < thresh:
        w = (1 + S) / (1 + thresh) 
        intensity = np.power(intensity_tmp, w)
    return intensity 


def normalize(intensities,method='standard'):
    #Normalizes a given vector to sum to 1 so that it represents a probability distribution
    if np.sum(intensities) > 0:
        intensities /= np.sum(intensities)
        if method == 'softmax':
            e_x = np.exp(intensities)
            intensities /= np.sum(intensities)
    return(intensities)


def filter_spec_lcms(spec, mz_min = 0, mz_max = 999999999999, int_min = 0, int_max = 999999999999, is_matched = False):
    #keep points in a given spectrum in a given range of mz values and intensity values

    '''
    spec[np.where(spec[:,0] < mz_min)[0],1] = 0
    spec[np.where(spec[:,0] > mz_max)[0],1] = 0
    spec[spec[:,1] < int_min] = 0
    spec[spec[:,1] > int_max] = 0
    '''
    if is_matched == False:
        spec = spec[spec[:,0] >= mz_min]
        spec = spec[spec[:,0] <= mz_max]
        spec = spec[spec[:,1] >= int_min]
        spec = spec[spec[:,1] <= int_max]
    else:
        spec = spec[spec[:,0] >= mz_min]
        spec = spec[spec[:,0] <= mz_max]
        spec[spec[:,1] >= int_min] = 0
        spec[spec[:,1] <= int_max] = 0
    return(spec)


def filter_spec_gcms(spec, mz_min = 0, mz_max = 999999999999, int_min = 0, int_max = 999999999999):
    #keep points in a given spectrum in a given range of mz values and intensity values
    spec[np.where(spec[:,0] < mz_min)[0],1] = 0
    spec[np.where(spec[:,0] > mz_max)[0],1] = 0
    spec[np.where(spec[:,1] < int_min)[0],1] = 0
    spec[np.where(spec[:,1] > int_max)[0],1] = 0
    return(spec)


def remove_noise(spec, nr):
    #removes points with intensity less than max(intensities)*nr
    if spec.shape[0] > 1:
        if nr is not None:
            spec[np.where(spec[:,1] < np.max(spec[:,1]) * nr)[0]] = 0
            #spec = spec[spec[:,1] >= np.max(spec[:,1]) * nr]
    return(spec)


def centroid_spectrum(spec, window_size):
    #This function was presented by: 
    #Li, Y.; Kind, T.; Folz, J.; Vaniya, A.; Mehta, S. S.; Fiehn, O.
    #Spectral entropy outperforms MS/MS dot product similarity for small-molecule compound identification. 
    #Nature Methods 2021, 18, 1524–1531

    #input:
    #spectrum: nx2 np array with first column being mass/charge and second column being intensity
    #window_size: window-size parameter

    #output:
    #centroided spectrum

    spec = spec[np.argsort(spec[:,0])]

    #Fast check is the spectrum needs centroiding
    mz_array = spec[:, 0]
    need_centroid = 0
    if mz_array.shape[0] > 1:
        mz_delta = mz_array[1:] - mz_array[:-1]
        if np.min(mz_delta) <= window_size:
            need_centroid = 1

    if need_centroid:
        intensity_order = np.argsort(-spec[:, 1])
        spec_new = []
        for i in intensity_order:
            mz_delta_allowed = window_size

            if spec[i, 1] > 0:
                #Find left bound for current peak
                i_left = i - 1
                while i_left >= 0:
                    mz_delta_left = spec[i, 0] - spec[i_left, 0]
                    if mz_delta_left <= mz_delta_allowed:
                        i_left -= 1
                    else:
                        break
                i_left += 1

                #Find right bound for current peak
                i_right = i + 1
                while i_right < spec.shape[0]:
                    mz_delta_right = spec[i_right, 0] - spec[i, 0]
                    if mz_delta_right <= mz_delta_allowed:
                        i_right += 1
                    else:
                        break

                #Merge those peaks
                intensity_sum = np.sum(spec[i_left:i_right, 1])
                intensity_weighted_sum = np.sum(spec[i_left:i_right, 0] * spec[i_left:i_right, 1])

                spec_new.append([intensity_weighted_sum / intensity_sum, intensity_sum])
                spec[i_left:i_right, 1] = 0

        spec_new = np.array(spec_new)
        #spec_new = spec_new[np.argsort(spec_new[:, 0])]
        if spec_new.shape[0] > 1:
            spec_new = spec_new[np.argsort(spec_new[:, 0])]
            return spec_new
        else:
            return np.array([[0,0]])
    else:
        return spec



def match_peaks_in_spectra(spec_a, spec_b, window_size):
    #This function was presented by: 
    #Li, Y.; Kind, T.; Folz, J.; Vaniya, A.; Mehta, S. S.; Fiehn, O.
    #Spectral entropy outperforms MS/MS dot product similarity for small-molecule compound identification. 
    #Nature Methods 2021, 18, 1524–1531

    #This function matches two spectra to find common peaks in order
    #to obtain two lists of intensities of the same length

    #input:
    #spec_a: nx2 np array with first column being mass/charge and second column being intensity
    #spec_b: mx2 np array with first column being mass/charge and second column being intensity
    #window_size: window-size parameter

    #output:
    #kx3 np array with first column being mass/charge, second column being matched intensities of spec_a, and third column being matched intensities of spec_b

    a = 0
    b = 0

    spec_merged = []
    peak_b_int = 0.

    while a < spec_a.shape[0] and b < spec_b.shape[0]:
        mass_delta = spec_a[a, 0] - spec_b[b, 0]
        
        if mass_delta < -window_size:
            # Peak only existed in spec a.
            spec_merged.append([spec_a[a, 0], spec_a[a, 1], peak_b_int])
            peak_b_int = 0.
            a += 1
        elif mass_delta > window_size:
            # Peak only existed in spec b.
            spec_merged.append([spec_b[b, 0], 0., spec_b[b, 1]])
            b += 1
        else:
            # Peak existed in both spec.
            peak_b_int += spec_b[b, 1]
            b += 1

    if peak_b_int > 0.:
        spec_merged.append([spec_a[a, 0], spec_a[a, 1], peak_b_int])
        peak_b_int = 0.
        a += 1

    if b < spec_b.shape[0]:
        spec_merged += [[x[0], 0., x[1]] for x in spec_b[b:]]

    if a < spec_a.shape[0]:
        spec_merged += [[x[0], x[1], 0.] for x in spec_a[a:]]

    if spec_merged:
        spec_merged = np.array(spec_merged, dtype=np.float64)
    else:
        spec_merged = np.array([[0., 0., 0.]], dtype=np.float64)
    return spec_merged



