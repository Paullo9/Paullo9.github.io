---
title: Connect to OMNI

---


>[!cheatsheet]-
>### Essential Commands
>1. **connect via**: `ssh username@omni.zimt.uni-siegen.de` enter pw


# Overview
The **OMNI Cluster** at the University of Siegen provides high-performance computing resources. This guide covers how to connect to the cluster using SSH.


# Connecting via SSH

To connect to the OMNI Cluster, you need:
- **SSH Client**: Tools like `ssh` (for Linux/macOS) or **PuTTY** (for Windows).

## **1. For Linux/macOS:**
Open your terminal and use the following command:
```bash
ssh g012345@omni.zimt.uni-siegen.de
```
Replace `username` with your actual cluster username (eg. g012345) and insert your password when asked.

>[!Example output]-
>#### In my case I get:
> `PS C:\Users\g031362> ssh g031362@omni.zimt.uni-siegen.de`
>`g031362@omni.zimt.uni-siegen.de's password:`
>`-----------------------------------------------------------`
>`Willkommen auf dem OMNI-Cluster der Universität Siegen..`
>`-----------------------------------------------------------`
>`Wenn Sie neu sind, beachten Sie die Anleitung "Erste Schritte" auf unserer Website:`
>`https://cluster.uni-siegen.de/erste-schritte/`
>`If you are new, please note the English-language "Getting Started" guide:`
>`https://cluster.uni-siegen.de/first-steps/?lang=en`
>`-----------------------------------------------------------`
>`Besuchen Sie uns doch unsere Sprechstunde! Immer montags um 14 Uhr, Details hier:`
>`https://cluster.uni-siegen.de/termine/#sprechstunde`
>`Why not visit us in our consultation hour? Every Monday 2 PM, details here:`
>`https://cluster.uni-siegen.de/termine/?lang=en#consultationhour`
>`-----------------------------------------------------------`
>`Aktuelles (19.Feb.24):`
>`Linaro Forge ist jetzt verfügbar`
>`Vollständige Meldung: https://cluster.uni-siegen.de/linaro-forge-ist-jetzt-verfuegbar/`
>`English news messages: https://cluster.uni-siegen.de/news/?lang=en`
>`-----------------------------------------------------------`

## **2. For Windows:**
1. **Download PuTTY** from the [official website](https://www.putty.org/).
2. Open PuTTY and enter the hostname: `omni.zimt.uni-siegen.de`.
3. Click **Open** and enter your username and password when prompted.

### **Shortcut: configuration file (optional)**
For frequent users, creating an SSH configuration file can simplify the login process:
1. Edit your `~/.ssh/config` file, on your local computer
2. Add the following entry:
   ```text
   Host omni
       HostName omni-cluster.uni-siegen.de
       User g012345
   ```
3. Shortcut: Connect using `ssh omni` instead of `ssh g012345@omni.zimt.uni-siegen.de`is now possible

Here’s a summarized version of the instructions for setting up password-less SSH access in Markdown format:



# Steps to set up password-less SSH access

1. **Generate SSH Key Pair**:
   - Run the following command on your local machine:
     ```bash
     ssh-keygen
     ```
   - This generates a key pair named `id_rsa` (private key) and `id_rsa.pub` (public key) by default.
   - If a key pair already exists, you will receive a warning. You can:
     - Cancel the process with `Ctrl+C` and use the existing key pair.
     - Or specify a new name or path for the new key pair.

2. **Set a Passphrase**:
   - You will be prompted to enter a passphrase. Adding a passphrase provides additional security but requires entering it periodically.

3. **Copy Public Key to the Cluster**:
   - Open the `id_rsa.pub` file with a text editor.
   - Log into the cluster on a new console.
   - Navigate to the `.ssh` directory on the cluster:
     ```bash
     cd ~/.ssh
     ```
   - Open the `authorized_keys` file with a text editor:
     ```bash
     nano authorized_keys
     ```
   - Copy the contents of `id_rsa.pub` into the `authorized_keys` file.

   **Caution**: Ensure you copy the public key (`.pub`) and not the private key. The private key should always remain on your local machine and should not be shared with anyone.

4. **Save and Test**:
   - Save the `authorized_keys` file and log out from the cluster with `exit`.
   - Log back in to test if password-less login is working.

This guide provides a step-by-step process to set up password-less SSH access to the cluster. Ensure that you handle your private key securely and only share the public key with the cluster.

# Troubleshooting

This guide covers basic connection methods to the OMNI Cluster. For additional information or complex configurations, see the [full documentation](https://cluster.uni-siegen.de/omni/usage/connecting/?lang=en).

>[!Next]-
> Next we will take a look at the [[Filesystems and Workspaces]]!