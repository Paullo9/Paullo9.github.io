> [!cheatsheet]-
> # Get the GUI or use the following commands:
> ### Essential Commands
> 1. **pull from main**: `git pull origin main`
> 1. **ckeck status**: `git status`
> 1.  **Add Changes**: `git add .`
> 1. **Commit changes**: `git commit -m "Commit message"`
> 1. **Push Changes** : `git push origin main`

# Update 03.07.2024
To make life easier there is a juypter git GUI available at [GitHub](https://github.com/jupyterlab/jupyterlab-git)
### Easy install of the Jupyterlab-Git Extension:
Install in your conda environment you plan on using to open the jupyter lab, in my case the py4dstem environment.
```
pip install --upgrade jupyterlab jupyterlab-git
```
This will give you something like this:
![[jupyterlabgitgui.png]]
# Basic Git Commands
This guide covers setting up Git on your cluster, generating SSH keys, and basic Git operations for managing your repository. This only applies if you already have a GitHub account and know the basic principles.

## 1. Pull Latest Changes
Fetches and merges changes from the remote repository to your local branch.
```bash
git pull origin main
```

## 2. Check Status
Displays the status of your working directory and staging area.
```bash
git status
```

## 3. Add Changes
Stages all changes in the current directory for the next commit.
```bash
git add .
```

## 4. Commit Changes
Commits the staged changes with a descriptive message.
```bash
git commit -m "Commit message"
```

## 5. Push Changes
Uploads your local branch commits to the remote repository.
```bash
git push origin main
```


# Cloning a Repository to the Cluster

## **1. Configure Git**

**Set Global Username and Email**
Configure your Git user name and email to be used in commits. In my case I use:
```bash
git config --global user.name "Paullo9"
```
```bash
git config --global user.email "paullobpreis@icloud.com"
```

**Verify Configuration**
Check if your configuration is correct:
```bash
git config --list
```

## **2. Generate SSH Keys**

**Generate SSH Keys** for authentication. SSH keys provide a secure way of accessing your GitHub account without entering a password.
```bash
ssh-keygen -t rsa -b 4096 -C "paullobpreis@icloud.com"
```
- Follow the prompts to save the key in the default location (`~/.ssh/id_rsa`).

**Display Your SSH Key**
Show the public key to copy to GitHub:
```bash
cat ~/.ssh/id_rsa.pub
```
- The key will look like this: `SHA256:ABC4YTwMTeC6FKmjdG6uchqxmMrKdBUjFB0SjvjvXkCH7M paullobpreis@icloud.com`

**Add SSH Key to GitHub**
1. Go to **GitHub** -> **Settings** -> **SSH and GPG keys**.
2. Click **New SSH key**, paste the public key, and save it.

## **3. Clone the Repository**

**Clone the Repository** to your cluster.
```bash
git clone git@github.com:Paullo9/4DSTEM.git
```
- This command clones the repository using SSH. Input username and the key if asked for a password.

## **4. Using Git on the Cluster**

- **Navigate to the Repository**: After cloning the folder of the repository should appear in your workspace
  ```bash
  cd 4DSTEM
  ```

- **Make Changes**: Edit files as needed.

- **Add and Commit Changes**:
  ```bash
  git add .
  git commit -m "Detailed commit message"
  ```

- **Push Changes to GitHub**:
  ```bash
  git push origin main
  ```



> [!Next]-
> **Almost done!** Learn how to allocate resources on the cluster and open a [[Open Jupyter Notebook on OMNI|Jupyter Notebook]]!

