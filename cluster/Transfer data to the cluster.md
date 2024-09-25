>[!cheatsheet]-
>### Essential Commands
>1. **Secure Copy Protocol (SCP)**: `scp data.txt username@omni.zimt.uni-siegen.de:/home/your_username/`
>21. ** rsync for Data Synchronization**: `rsync data.txt username@omni.zimt.uni-siegen.de:/home/your_username/`

# Methods to Transfer Data

## 1. Secure Copy Protocol (SCP)

- **Description**: Transfer files securely between your PC and the cluster.
- **Command**: `scp [options] local_path user@remote_host:remote_path`
- **Example**: 
  ```bash
  scp data.txt username@omni.zimt.uni-siegen.de:/home/your_username/
  ```
- **Options**: 
  - `-r`: Recursively transfer directories.
  - `-P port`: Specify a different port.

## 2. rsync for Data Synchronization

- **Description**: Synchronize files and directories efficiently.
- **Command**: `rsync [options] local_path user@remote_host:remote_path`
- **Example**: 
  ```bash
  rsync -avz project/ username@omni.zimt.uni-siegen.de:/home/your_username/project/
  ```
- **Options**: 
  - `-a`: Archive mode
  - `-v`: Verbose
  - `-z`: Compress files

## 3. FileZilla (Graphical Transfer)

- **Description**: Use FileZilla for an easy, graphical file transfer via SFTP.
- **Download**: [FileZilla](https://filezilla-project.org/)
- **Steps**:
  - Enter `sftp://omni-cluster.uni-siegen.de` in Host
  - Enter your username and password
  - Connect and drag files to transfer

## 4. MobaXterm for Windows

- **Description**: Use MobaXterm for integrated SSH and SFTP.
- **Download**: [MobaXterm](https://mobaxterm.mobatek.net/)
- **Steps**:
  - Create a new **SFTP session**.
  - Enter the cluster’s login details.
  - Transfer files using the file explorer.

## 5. NAS/XNAS for Data Transfer

- **Description**: Use NAS/XNAS storage services from login nodes.
- **Commands**:
  - **Login**:
    ```bash
    ssh username@omni.zimt.uni-siegen.de
    ```
  - **Mount Paths**:
		- **Login**: `kinit`
		-  **XNAS**: `cd /xnas`
  - **Example**:
    ```bash
    scp data.txt /nas/your_username/
    ```

# Summary Table

| Tool/Command | Description                                   | Example|
|--------------|-----------------------------------------------|------------------------------------------|
| `scp`        | Securely copy files to/from the cluster       | `scp file.txt user@cluster:/home/user/`|
| `rsync`      | Synchronize directories and files             | `rsync -avz dir/ user@cluster:/home/user/dir/` |
| FileZilla    | Graphical file transfer using SFTP            | Use GUI to connect to cluster|
| MobaXterm    | Integrated SSH and SFTP client for Windows    | Use SFTP session to connect and transfer files|
| NAS/XNAS     | Network storage for easier data transfer      | `scp file.txt /nas/...`  |

# Shortcut JupyterHub

An easy way to upload data is to drag and drop it to the barely functional [OMNI Jupyter Hub](https://omni.zimt.uni-siegen.de/) provided by ZIMT. It is a quick and easy way to access your home on the cluster.


>[!Next]-
> We should really look at [[Version control with Git]]!