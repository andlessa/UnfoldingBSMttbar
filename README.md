# Unfolding BSM @ ttbar
Repository for holding code and data for the BSM ttbar project

## Folders and files

Below we describe the folders stored in this repository. 

 * [processFolders](./processFolders): Contains the \texttt{MadGraph5} process directories for the VLF, scalar, $Z'$, and Standard Model implementations. Within each directory, the corresponding process subfolder includes the input cards used for the generation, as well as the \texttt{Events} folder, which contains the banner and LHE files.
 ---
 * [Distributions](./processFolders/Distributions/): Directory containing the \texttt{.npz} files, organized into separate subfolders for each model.
 ---
  * [Example](./Example.ipynb): Notebook providing a concise guide on how to read the LHE files, compute the relevant distributions, save and reload the results, and generate comparative plots for each model.
 ---
  * [modelFiles](./modelFiles): stores the FeynRules files for the models
 ---
  * [plotting](./plotting): folder storing Jupyter notebooks and code used for plotting
 ---
  * [processFolders](./processFolders): stores several process and parameter cards for generating events with MadGraph
 ---
  * [Recast_CMs](./Recast_CMS): folder to store the recasting codes
 ---
   * [Scripts](./Recast_CMS): folder to store the python Scripts related to event generation and distributions computations
 ---
  * [UFOandFAModels](./Models): stores the UFO and FeynArts output for the models
 ---
  * [xsec_processFolders](./xsec_processFolders): stores several process and parameter cards for generating events with MadGraph. This events was exclusively used in the total cross section analysis
