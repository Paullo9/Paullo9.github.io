>[!cheatsheet]-
>### Essential Commands
>1. **Connect to cluster**: `ssh g0123456@omni.zimt.uni-siegen.de`
>1. **Request a node**: `srun -p smp --time=02:00:00 --ntasks-per-node 1 --mem=500GB --pty bash`
>1. **SSH to that node**: In a seperate terminal: `ssh -t -t g123456@omni.zimt.uni-siegen.de -L 8888:localhost:8888 ssh smp-node001  -L 8888:localhost:8888` 
>1. **Activate environment**: `conda activate py4dstem`
>1. **Open Jupyter Lab**: `jupyter lab --no-browser --port=8888`
>1. **Access trough browser**: `http://localhost:8888`
>1. **End Session**: `ctrl + c` and press enter. The server will return `Shutdown this Jupyter server (y/[n])?`

## 1. SSH to the Cluster
Connect to the cluster via SSH.
```bash
ssh g031362@omni.zimt.uni-siegen.de
```
- Enter your password when prompted.
- Clone your code to home directory and store your data on /work or /fast

## 2.  Request a node
Request resources, and start a job interactively on a node.
```bash
srun -p smp --time=02:00:00 --ntasks-per-node 1 --mem=500GB --pty bash
```
- Several options, please see the official [OMNI](https://cluster.uni-siegen.de/omni/usage/queuing-a-job/?lang=en) website and documentation!
- -p: which partition, options are: short, medium, long, smp, gpu
- smp nodes have 1500GB RAM so for big datasets they are preferred
- --time: eg. `12:00:00` partitions often have default times
- --ntasks-per-node: i kept it at one mostly
- --mem: how much RAM we want
- script requests a node with the set parameters
- check the queue of submitted and running jobs with `squeue`to show the queue of a specific user use `seueue -u g0123456`
- once allocated, we can start a notebook on the node, eg. `smp-node001` but first we need to set port forwarding

## 3. SSH Port Forwarding
Open a new terminal tab and set up port forwarding to the node, in this case `smp-node001` and redirect it to port=8888 via the following command:
```bash
ssh -t -t g031362@omni.zimt.uni-siegen.de -L 8888:localhost:8888 ssh smp-node001  -L 8888:localhost:8888
```
- Enter your password, maybe twice

## 4. Activate Conda Environment
Activate the Py4DSTEM Conda environment on the node we just forwarded to.
```bash
conda activate py4dstem
```

## 5. Start Jupyter Lab
Launch Jupyter Lab on the specific port we just set.
```bash
jupyter lab --no-browser --port=8888
```

>[!If error occurs due to a circular import]-
>Try to use conda/pip to update the module causing the error and retry, in my case it was the following that made it work:
> Error: `AttributeError: partially initialized module 'charset_normalizer' has no attribute 'md__mypyc' (most likely due to a circular import)`
> Fix: `pip install --upgrade charset_normalizer requests`

## 6. Open Jupyter Lab in Browser
In your browser, navigate to the port.
```plaintext
http://localhost:8888
```
- If asked, enter the token provided in the terminal, e.g., `http://localhost:8888/lab?token=1af4cf9a84901f6f5cfd7af6af9e6e9d229b1fe086be3e59`.

## 7. Stopping the Server
Go back to terminal with the active server, use `ctrl + c` and press enter. The server will return `Shutdown this Jupyter server (y/[n])?` Close server by confirming with `y` and enter. Exit the node and cluster by typing `exit` in both terminal tabs.


>[!Next]-
> Now we can finally start to use py4DSTEM on the cluster with our own data!