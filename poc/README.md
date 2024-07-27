# WADAS POC

## Dependencies
1. [Pytorch Wildlife](https://github.com/microsoft/CameraTraps)
2. [torch](https://pytorch.org/)
3. [intel-npu-acceleration-library](https://github.com/intel/intel-npu-acceleration-library)

## Environment setup
Reference IDE used for the project is Visual Studio Code, Conda (Miniconda) as package manager.
Instructions will reflect the above mentioned reference environment, users are free to choose any equivalent environment for development and execution of the project.

### Dependencies install ###
   1. Import the WADAS project into your IDE 
   2. Create venv enviromnent (See https://code.visualstudio.com/docs/python/environments for detailed info about how to create virtual environment within VScode, we used conda.)
   3. Install dependencies: 
      a. pip install -r requirements.txt .\poc\requirements.txt (or run Python: Create environment from VScode)
      b. Aditional useful dependencies to tune up jupyter kernels are: ipykernel jupyter
## Run
    1. Open demo.ipynb and make sure you have selected your local kernel (python venv) (in VScode run the command "Select Notebook Kernel")
    2. Run pw_demo.ipynb (animal detection only) OR df_demo.ipynb (animal detection + classification)

NOTE: Depending on the HW you're running the demo on, you could select different kernel to run the model on: npu, cuda or cpu. Make sure you properly configure the environment dependency of your custom kernel first.