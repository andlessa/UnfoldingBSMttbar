# Unfolding BSM @ ttbar
Repository for holding code and data for the BSM ttbar project

## Folders and files

Below we describe the folders stored in this repository. 

 * [processFolders](./processFolders): Contains the \texttt{MadGraph5} process directories for the VLF, scalar, $Z'$, and Standard Model implementations. Within each directory, the corresponding process subfolder includes the input cards used for the generation, as well as the \texttt{Events} folder, which contains the banner and LHE files.
 ---
 * [Distributions](./processFolders/Distributions/): Directory containing the \texttt{.npz} files, organized into separate subfolders for each model.
 ---
 * [UFO_Models](./UFO_Models): stores UFO for each model. 
 ---
  * [Example](./Example.ipynb): Notebook providing a concise guide on how to read the LHE files, compute the relevant distributions, save and reload the results, and generate comparative plots for each model.
