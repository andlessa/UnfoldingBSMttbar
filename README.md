# Unfolding BSM @ ttbar
Repository for holding code and data for the BSM ttbar project

## Folders and files

Below we describe the folders stored in this repository. 

 * [data_samples](./data_samples/): Folder containing the $p p \rightarrow t \bar{t}$ events at parton level in the LHE format for the  VLF, scalar and $Z'$ models. Note that the events corresponds to the SM plus BSM contribution.
 In addition the SM folder contains the SM-only events.

 * [processFolders](./processFolders): Contains the `MadGraph5` process directories for the VLF, scalar, $Z'$, and Standard Model implementations. Within each directory, the corresponding process subfolder includes the input cards used for the generation, as well as the `Events folder, which contains the banner and LHE files.
 ---
 * [Distributions](./processFolders/Distributions/): Directory containing the `.npz` files, organized into separate subfolders for each model.
 ---
 * [UFO_Models](./UFO_Models): stores UFO for each model. 
 ---
  * [Example](./Example.ipynb): Notebook providing a concise guide on how to read the LHE files, compute the relevant distributions, save and reload the results, and generate comparative plots for each model.
