>[!cheatsheet]-
>### Essential Commands
>1. **Loading of miniconda3**: `module load miniconda3/4.9.2` only first time
>1. **Initializing conda**: `conda init` only first time
>1. **create environment**: `conda create -n py4dstem` 
>1. **activate environment**: `conda activate py4dstem`
>1. **Installing py4DSTEM**: `conda install -c conda-forge py4dstem pymatgen jupyterlab`
>1. **deactivate environment**: `conda deactivate`
>1. **list packages in environment**: `conda list`
>1. **list environments**: `conda env list`


# Introduction to Conda

Conda, in this case a lightweight version called miniconda3, is an open-source package management and environment management system that allows you to create isolated environments for different projects, managing dependencies and versions efficiently. This is especially useful on shared systems like clusters where multiple users may need different versions of packages or software.

# Initiating and using Conda on the Cluster
Before we can use miniconda3 on the cluster we have to load the module and initiate it. First out of general curiosity we could list which modules are available in the first place by:

1. **Check available modules**:
   ```bash
   module avail
   ```
1. **To search for a specific module use:**
   ```bash
   module spider <module_name>
   ```
1. **For Miniconda:**
   ```bash
   module spider miniconda
   ```
1. **Load Miniconda**: 
   ```bash
   module load miniconda3/4.9.2
   ```

1. **Initialize Conda**: After loading the module, initialize conda. This has to be done, otherwise you need to load the module every time you log onto the cluster.
   ```bash
   conda init
   ```

1. **Verify Conda Activation**: Ensure Conda is active by checking its version.
   ```bash
   conda --version
   ```

# Installing Py4DSTEM

Follow these steps to install Py4DSTEM and its dependencies in a new Conda environment:

1. **Create a New Environment for Py4DSTEM**:
   ```bash
   conda create -n py4dstem
   ```

2. **Activate the New Environment**:
   ```bash
   conda activate py4dstem
   ```

3. **Install Py4DSTEM and Other Dependencies**:
   ```bash
   conda install -c conda-forge py4dstem pymatgen jupyterlab
   ```

# Basic Conda Commands

**Initialize Conda**: Prepares Conda for use, must be done when first set up.
  ```bash
  conda init
  ```

**Create a new environment**: Set up a separate environment for a specific project.
  ```bash
  conda create -n <env_name>
  ```

**Activate an Environment**: Switch to the specified environment.
  ```bash
  conda activate <env_name>
  ```

**Deactivate an Environment**: Switch off currently loaded environment.
  ```bash
  conda deactivate
  ```
  
**Install Packages**: Add packages to the active environment.
  ```bash
  conda install -c <channel> <package_name>
  ```
  **Listing packages**: List of the packages in the current environment
  ```bash
  conda list
```
  **List environments**: List of all the environments
  ```bash
  conda env list
```
**Conda help**: Shows the options of the package and possible commands:
```bash
conda help
```

# Summary
By using Conda on the cluster, you can easily manage dependencies and avoid conflicts by creating isolated environments. This guide helps you load the necessary modules, initialize Conda, and install py4DSTEM along with its required dependencies. Always refer to the [official Py4DSTEM documentation](https://py4dstem.readthedocs.io/) for the most accurate installation instructions and updates.

>[!Next]-
> Now we need to [[Transfer data to the cluster|transfer data to the cluster]]!