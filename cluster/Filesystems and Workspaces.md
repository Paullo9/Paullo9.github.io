>[!cheatsheet]-
>> Using the Home directory to store code and the work/fast for datasets seems to be best practice!
> ### Essential Commands
> 1. **create workspace with several options**: `ws_allocate <WS name> <duration> -r <days> -m <email>`
> 2. **create a /fast workspace with several options**: `ws_allocate -F fast <WS name> <duration>`
> 3. **List Workspaces**: `ws_list`
> 4. **Access /xnas **: `kinit` enter password then `cd /xnas`

# Overview

The cluster offers multiple file systems to cater to various storage needs:

- **Home Directory** (`/home/<YourUsername>`): Default storage for users' data, limited to 100 GB. Snapshots are taken daily and stored for 30 days, accessible at `/home/.snapshot`.
- **Workspace Directory** (`/work`): For short-term storage of large data sets. Workspaces are created under `/work/ws-tmp/` and are not size-limited but have a time limit of 30 days, extendable up to three times. No automatic backups are provided.

- **Burst Buffer Directory** (`/fast`): Located on SSDs, this is a 32 TB partition for high-speed data operations. Data should be moved to regular workspaces after computations due to the buffer's instability and limited size.

- **Groupspaces** (`/group`): For team or departmental use, managed by group leaders. Accessible from both login and compute nodes. Limited to 100 GB.

- **NAS/XNAS Directories** (`/nas` and `/xnas`): Available for data transfer but not suitable for computations or software installations. Accessible via login nodes.

Every login and compute node accesses the same file systems.

# Workspaces
## Create and extend workspaces

**Recommended function to create workspaces **:
```bash
ws_allocate <WS name> <duration> -r <days> -m <email>
```

This command creates a workspace with the name `<WS name>`  and a `<duration>` of max 30 days. You can use the `-m` option to set your email address and the `-r` option to specify how many days before expiration you want to receive a warning.

**Extend workspace**: you can extend your workspace by 30 days up to three times 
```bash
ws_extend <WS name> <duration>
```

## List workspaces
**List Workspaces**: get a list of all your workspaces
```bash
ws_list
```

## Release workspaces
**Release Workspace**: data will be instantly unavailable but not deleted for approx. 10 days
```bash
ws_release <Workspace name>
```

## Restore workspaces
**Restore Workspace**: released workspaces and expired workspaces can be restored by following command within 10 days
```bash
ws_restore <user>-<old-workspace>-<number> <new-workspace>
```

# Creating a fast workspace: Burst Buffer

- **Path**: `/fast`
- **Size**: 32 TB
- **Usage**: when fast readout speeds are needed
```bash
ws_allocate -F fast <WS name> <duration>
```
**Exending the /fast workspace:** also three times, 30 days
```bash
ws_extend -F [work|fast] <WS name>  <duration>

```

# Groupspaces (maybe relevant in the future)

- **Request**: via `support@zimt.uni-siegen.de`
- **Path**: `/group/<AG-Name>`
- **Limit**: 100 GB
- **Permissions**: Managed with `chmod` and `chgrp`.

# NAS/XNAS

**Access**: to acess the XNAS use the following command:
```bash
kinit
```
You will be asked to enter your Password. After that try to navigate to the xnas by:
```
cd /xnas
```
List the folders available to you by `ls`


>[!Next]-
> Next we should set up our [[Setting up py4dstem with miniconda3|environment]]!