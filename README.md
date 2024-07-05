# MZsearch
Command-line Python tool to perform spectral library matching to identify chemical compounds with host of preprocessing transformations and similarity measures (Cosine and three entropy-based similarity measures). MZsearch is capable of performing spectral library matching with respect to either gas chromatography - mass spectrometry (GC-MS) or liquid chromatography - mass spectrometry (LC-MS) data.

# Create conda environment and install dependencies
MZsearch requires the Python dependencies Matplotlib, NumPy, Pandas, and SciPy and R libraries MSnbase and optparse. Specifically, this software was validated with python=3.12.4, matplotlib=3.8.4, numpy=1.26.4, pandas=2.2.2, scipy=1.13.1, MSnbase=2.30.1, and optparse=1.7.5, although it may work with other versions of these tools. For instructions on installing conda on your system, see: [https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html). Once conda is installed, you can create a conda environment with the necessary dependencies and activate the conda environment with the commands:
```
conda env create -n mzsearch_env -f environment.yml
conda activate mzsearch_env
```

To return to your base environment, you can deactivate the mzsearch_env environment with the command:
```
conda deactivate
```

# Usage
This repository has two main capabilities:
1. running spectral library matching to identify compounds based off of their mass spectrometry data
2. plotting a query spectrum vs a reference spectrum before and after preprocessing transformations.

These tasks are implemented separately for the cases of (i) GC-MS and (ii) LC-MS data due to the different spectrum preprocessing transformations stemming from a different format in the mass:charge ratios in GC-MS vs LC-MS data. To see all parameters for any of the four main scripts (spec_lib_matching_lcms.py, spec_lib_matching_gcms.py, plot_spectra_lcms.py, plot_spectra_gcms.py), run:
```
python spec_lib_matching_.py -h
python spec_lib_matching_.py -h
python plot_spectra_.py -h
python plot_spectra_gcms.py -h
```
## Run spectral library matching
To run spectral library matching on LC-MS/GC-MS data, one can use:
```
python spec_lib_matching_.py \
  --query_data path_to_query__CSV_file \
  --reference_data path_to_reference__CSV_file

python spec_lib_matching_gcms.py \
  --query_data path_to_query_gcms_CSV_file \
  --reference_data path_to_reference_gcms_CSV_file
```

Example implementations of these scripts with all parameters specified are:
```
python spec_lib_matching_.py \
  --query_data path_to_query__CSV_file \
  --reference_data path_to_reference__CSV_file \
  --likely_reference_IDs None \
  --similarity_measure cosine \
  --spectrum_preprocessing_order FCNMWL \
  --high_quality_reference_library False \
  --mz_min 0\
  --mz_max 999999999999\
  --int_min 0\
  --int_max 999999999999\
  --window_size_centroiding 0.5 \
  --window_size_matching 0.5 \
  --noise_threshold 0 \
  --wf_mz 0 \
  --wf_intensity 1 \
  --LET_threshold 0 \
  --entropy_dimension 1.1 \
  --normalization_method standard \
  --n_top_matches_to_save 1 \
  --print_id_results False \
  --output_identification path_to__identification_results_CSV \
  --output_similarity_scores path_to_CSV_of_all__similarity_scores

python spec_lib_matching_gcms.py \
  --query_data path_to_query_gcms_CSV_file \
  --reference_data path_to_reference_gcms_CSV_file \
  --likely_reference_IDs None \
  --similarity_measure cosine \
  --spectrum_preprocessing_order FNLW \
  --high_quality_reference_library False \
  --mz_min 0\
  --mz_max 999999999999\
  --int_min 0\
  --int_max 999999999999\
  --wf_mz 0 \
  --wf_intensity 1 \
  --entropy_dimension 1.1 \
  --normalization_method standard \
  --n_top_matches_to_save 1 \
  --print_id_results False \
  --output_identification path_to_gcms_identification_results_CSV \
  --output_similarity_scores path_to_CSV_of_all_gcms_similarity_scores
```

Parameter descriptions are as follows:

--query_data: 
  * LC-MS case: 3-column CSV file of query mass spectrum/spectra to be identified. Each row should correspond to a single ion fragment of a mass spectrum, the left-most column should contain an identifier, the middle columns should correspond the mass:charge ratios, and the right-most column should contain the intensities. For example, if spectrum A has 3 ion fragments, then there would be three rows in this CSV file corresponding to spectrum A. Default: LC-MS GNPS library.
  * GC-MS case: CSV file of query mass spectrum/spectra to be identified. Each row should correspond to a mass spectrum, the left-most column should contain an identifier, and each of the other columns contains the intensity with respect to a single mass/charge ratio. Default: GC-MS NIST WebBook library

--reference_data: same format CSV file as query_data except of reference library spectra.

--likely_reference_IDs: CSV file with one column containing the IDs of a subset of all compounds in the reference_data to be used in spectral library matching. Each ID in this file must be an ID in the reference library. Default: None (i.e. default is to use entire reference library)

--similarity_measure: options are 'cosine', 'shannon', 'renyi', and 'tsallis'.

--spectrum_preprocessing_order: The spectrum preprocessing transformations and the order in which they are to be applied. These transformations are applied prior to computing similarity scores. Format must be a string with 2-6 (LC-MS) or 2-4 (GC-MS) characters chosen from F, N, W, C, M, L representing filtering, noise removal, weight-factor-transformation, centroiding, matching, and low-entropy tranformation, respectively. Matching (M) and centroiding (C) are applicable only to LC-MS data. For example, if \'WCM\' is passed, then each (LC-MS) spectrum will undergo a weight factor transformation, then cleaning, and then matching. Note that if an argument is passed, then \'M\' must be contained in the argument, since matching is a required preprocessing step in spectral library matching of  data. Default: FCNMWL for LC-MS and FNLW for GC-MS.

--high_quality_reference_library: True/False flag indicating whether the reference library is considered to be of high quality. If True, then the spectrum preprocessing transformations of filtering and noise removal are performed only on the query spectrum/spectra. If False, all spectrum preprocessing transformations specified will be applied to both the query and reference spectra. Default: False.

--mz_min: Remove all peaks with mass/charge less than mz_min in each spectrum. Default = 0.

--mz_max: Remove all peaks with mass/charge greater than mz_max in each spectrum. Default = 999999999999.

--int_min: Remove all peaks with intensity less than int_min in each spectrum. Default = 0.

--int_max: Remove all peaks with intensity greater than int_max in each spectrum. Default = 999999999999.

--window_size_centroiding (LC-MS only): Window size parameter used in centroiding a given spectrum. Default = 0.5.

--window_size_matching (LC-MS only): Window size parameter used in matching a query spectrum and a reference library spectrum. Default = 0.5.

--noise_threshold: Ion fragments (i.e. points in a given mass spectrum) with intensity less than max(intensities)*noise_threshold are removed. Default = 0.

--wf_mz: Mass/charge weight factor parameter. Default = 0.

--wf_intensity: Intensity weight factor parameter. Default = 1.

--LET_threshold: Low-entropy transformation threshold parameter. Spectra with Shannon entropy H less than LET_threshold are transformed according to $\text{intensitiesNew}=\text{intensitiesOriginal}^{\frac{1+S}{1+\text{LETthreshold}}}$. Default = 0.

--entropy_dimension: Entropy dimension parameter. Must have positive value other than 1. When the entropy dimension is 1, then Renyi and Tsallis entropy are equivalent to Shannon entropy. Therefore, this parameter only applies to the renyi and tsallis similarity measures. This parameter will be ignored if similarity measure cosine or shannon is chosen. Default = 1.1.

--normalization_method: Method used to normalize the intensities of each spectrum so that the intensities sum to 1. Since the objects entropy quantifies the uncertainy of must be probability distributions, the intensities of a given spectrum must sum to 1 prior to computing the entropy of the given spectrum intensities. Options: 'standard' and 'softmax'. Default = standard.

--n_top_matches_to_save: The number of top matches to report. For example, if n_top_matches_to_save=5, then for each query spectrum, the five reference spectra with the largest similarity with the given query spectrum will be reported. Default = 1.

--print_id_results: Flag indicating whether to print the identification results interactively. Regardless of this flag, the results are saved according to the parameter 'output_identification'. Default = False.
--output_identification: Output CSV file containing the most-similar reference spectra for each query spectrum along with the corresponding similarity scores. Default is to save identification output in current working directory (i.e. same directory this script is contained in) with filename 'output_lcms_identification.csv'.

--output_similarity_scores: Output CSV file containing similarity scores between all query spectrum/spectra and all reference spectra. Each row corresponds to a query spectrum, the left-most column contains the query spectrum/spectra identifier, and the remaining column contain the similarity scores with respect to all reference library spectra. If no argument passed, then this CSV file is written to the current working directory with filename 'output_lcms_all_similarity_scores'.csv.



## Plot a query spectrum against a reference spectrum before and after spectrum preprocessing transformations
To plot a query spectrum vs a reference spectrum before and after preprocessing transformations, run:
```
python plot_spectra_lcms.py \
  --query_data path_to_query_lcms_CSV_file \
  --reference_data path_to_reference_lcms_CSV_file \
  --query_spectrum_ID insert_single_ID_from_first_column_of_query_data \
  --reference_spectrum_ID insert_single_ID_from_first_column_of_reference_data \
  --similarity_measure cosine \
  --spectrum_preprocessing_order FCNMWL \
  --high_quality_reference_library False \
  --mz_min 0\
  --mz_max 999999999999\
  --int_min 0\
  --int_max 999999999999\
  --window_size_centroiding 0.5 \
  --window_size_matching 0.5 \
  --noise_threshold 0 \
  --wf_mz 0 \
  --wf_intensity 1 \
  --LET_threshold 0 \
  --entropy_dimension 1.1 \
  --normalization_method standard \
  --save_plots path_to_output_PDF_file

python plot_spectra_gcms.py \
  --query_data path_to_query_gcms_CSV_file \
  --reference_data path_to_reference_gcms_CSV_file \
  --query_spectrum_ID insert_single_ID_from_first_column_of_query_data \
  --reference_spectrum_ID insert_single_ID_from_first_column_of_reference_data \
  --similarity_measure cosine \
  --spectrum_preprocessing_order FNLW \
  --high_quality_reference_library False \
  --mz_min 0\
  --mz_max 999999999999\
  --int_min 0\
  --int_max 999999999999\
  --wf_mz 0 \
  --wf_intensity 1 \
  --LET_threshold 0 \
  --entropy_dimension 1.1 \
  --normalization_method standard \
  --save_plots path_to_output_PDF_file
```

Parameter descriptions are as follows:

--query_data: 
  * LC-MS case: 3-column CSV file of query mass spectrum/spectra to be identified. Each row should correspond to a single ion fragment of a mass spectrum, the left-most column should contain an identifier, the middle columns should correspond the mass:charge ratios, and the right-most column should contain the intensities. For example, if spectrum A has 3 ion fragments, then there would be three rows in this CSV file corresponding to spectrum A. Default: LC-MS GNPS library.
  * GC-MS case: CSV file of query mass spectrum/spectra to be identified. Each row should correspond to a mass spectrum, the left-most column should contain an identifier, and each of the other columns contains the intensity with respect to a single mass/charge ratio. Default: GC-MS NIST WebBook library

--reference_data: Same format CSV file as query_data except of reference library spectra.

--query_spectrum_ID: The identifier of the query spectrum to be plotted. Default: first query spectrum in query_data.

--reference_spectrum_ID: The identifier of the reference spectrum to be plotted. Default: first reference spectrum in reference_data.

--similarity_measure: Options are 'cosine', 'shannon', 'renyi', and 'tsallis'.

--spectrum_preprocessing_order: The LC-MS spectrum preprocessing transformations and the order in which they are to be applied. Note that these transformations are applied prior to computing similarity scores. Format must be a string with 2-4 characters chosen from W, C, M, L representing weight-factor-transformation, cleaning (i.e. centroiding and noise removal), matching, and low-entropy transformation. For example, if \'WCM\' is passed, then each spectrum will undergo a weight factor transformation, then cleaning, and then matching. Note that if an argument is passed, then \'M\' must be contained in the argument, since matching is a required preprocessing step in spectral library matching of LC-MS data. Default: FCNMWL for LC-MS and FNLW for GC-MS .

--high_quality_reference_library: True/False flag indicating whether the reference library is considered to be of high quality. If True, then the spectrum preprocessing transformations of filtering and noise removal are performed only on the query spectrum/spectra. If False, all spectrum preprocessing transformations specified will be applied to both the query and reference spectra. Default: False.

--mz_min: Remove all peaks with mass/charge less than mz_min in each spectrum. Default = 0.

--mz_max: Remove all peaks with mass/charge greater than mz_max in each spectrum. Default = 999999999999.

--int_min: Remove all peaks with intensity less than int_min in each spectrum. Default = 0.

--int_max: Remove all peaks with intensity greater than int_max in each spectrum. Default = 999999999999.

--window_size_centroiding (LC-MS only): Window size parameter used in centroiding a given spectrum. Default = 0.5.

--window_size_matching (LC-MS only): Window size parameter used in matching a query spectrum and a reference library spectrum. Default = 0.5.

--noise_threshold: Ion fragments (i.e. points in a given mass spectrum) with intensity less than max(intensities)*noise_threshold are removed. Default = 0.

--wf_mz: Mass/charge weight factor parameter. Default = 0.

--wf_intensity: Intensity weight factor parameter. Default = 1.

--LET_threshold: Low-entropy transformation threshold parameter. Spectra with Shannon entropy H less than LET_threshold are transformed according to $\text{intensitiesNew}=\text{intensitiesOriginal}^{\frac{1+S}{1+\text{LETthreshold}}}$. Default = 0.

--entropy_dimension: Entropy dimension parameter. Must have positive value other than 1. When the entropy dimension is 1, then Renyi and Tsallis entropy are equivalent to Shannon entropy. Therefore, this parameter only applies to the renyi and tsallis similarity measures. This parameter will be ignored if similarity measure cosine or shannon is chosen. Default = 1.1.

--normalization_method: Method used to normalize the intensities of each spectrum so that the intensities sum to 1. Since the objects entropy quantifies the uncertainy of must be probability distributions, the intensities of a given spectrum must sum to 1 prior to computing the entropy of the given spectrum intensities. Options: 'standard' and 'softmax'. Default = standard.

--save_plots: Output PDF file containing the plots of the query and reference spectra before and after preprocessing transformations. If no argument is passed, then the plots will be saved to the PDF ./query_spec_{query_spectrum_ID}_reference_spec_{reference_spectrum_ID}_plot.pdf in the current working directory.


## Obtain LC-MS library from MGF file
To obtain a CSV file of LC-MS spectra in the format necessary for spectral library matching from raw data in an MGF file, one can run:
```
Rscript get_lcms_library_from_mgf.R \
--input_path path_to_input_mgf_file \
--output_path path_to_output_csv_file
```

Some example MGF files one can use to build a LC-MS library can be found from the Global Natural Products Social Molecular Networking databases here: [https://external.gnps2.org/gnpslibrary](https://external.gnps2.org/gnpslibrary).


# Bugs/Questions?
If you notice any bugs in this software or have any questions, don't hesitate to reach out to fy7392@wayne.edu.






