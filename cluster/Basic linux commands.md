>[!cheatsheet]-
> ### Essential Commands
> 1. **cd** - Change Directory: `cd [dir]` (e.g., `cd /home/user`)
> 1. **ls** - List Files: `ls [options] [dir]` (e.g., `ls -a`)
> 1. **pwd** - Print Working Directory: `pwd`
> 1. **cp** - Copy Files: `cp [options] src dest` (e.g., `cp -r dir1 dir2`)
> 1. **mv** - Move/Rename Files: `mv [options] src dest` (e.g., `mv old.txt new.txt`)
> 1. **rm** - Remove Files: `rm [options] file` (e.g., `rm -r dir`)
> 1. **touch** - Create File: `touch filename` (e.g., `touch new.txt`)
> 1. **mkdir** - Make Directory: `mkdir [options] dir` (e.g., `mkdir -p /new/dir`)
> 1. **ls -l** - Detailed List: `ls -l [dir]`
> 1. **stat** - File Status: `stat file` (e.g., `stat file.txt`)

Understanding Linux commands is essential for efficient file management and system navigation on the cluster. Here’s a  guide to some fundamental Linux commands with examples and practical usage tips.

# 1. `cd` - Change Directory

**Description**: The `cd` command is used to change the current working directory.

**Syntax**: `cd [directory_path]`

**Examples**:
- `cd /home/user/Documents` – Changes to the `Documents` directory in the specified path.
- `cd ..` – Moves up one level in the directory tree.
- `cd ~` – Moves to the user's home directory.

**Tips**:
- Use `cd -` to switch back to the previous directory.
- `cd /` takes you to the root directory.


# 2. `ls` - List Directory Contents

**Description**: The `ls` command lists files and directories in the current directory.

**Syntax**: `ls [options] [directory_path]`

**Examples**:
- `ls` – Lists contents of the current directory.
- `ls /home/user/Documents` – Lists contents of the `Documents` directory.

**Tips**:
- Use `ls -a` to list all files, including hidden ones.
- Combine with `grep` to search for specific file types: `ls | grep .txt`.



# 3. `pwd` - Print Working Directory

**Description**: The `pwd` command prints the full path of the current working directory.

**Syntax**: `pwd`

**Examples**:
- `pwd` – Displays the current directory path.

**Tips**:
- Handy for confirming your current location in the file system hierarchy.



# 4. `cp` - Copy Files and Directories

**Description**: The `cp` command copies files or directories from one location to another.

**Syntax**: `cp [options] source destination`

**Examples**:
- `cp file.txt /home/user/backup/` – Copies `file.txt` to the `backup` directory.
- `cp -r /source/directory /destination/directory` – Recursively copies a directory.

**Tips**:
- Use `cp -i` for interactive mode, prompting before overwriting files.
- `cp -v` displays detailed output of the copy operation.



# 5. `mv` - Move or Rename Files

**Description**: The `mv` command moves or renames files or directories.

**Syntax**: `mv [options] source destination`

**Examples**:
- `mv oldname.txt newname.txt` – Renames `oldname.txt` to `newname.txt`.
- `mv file.txt /home/user/Documents/` – Moves `file.txt` to the `Documents` directory.

**Tips**:
- Use `mv -i` to avoid overwriting existing files without confirmation.



# 6. `rm` - Remove Files or Directories

**Description**: The `rm` command removes files or directories.

**Syntax**: `rm [options] file`

**Examples**:
- `rm file.txt` – Removes `file.txt`.
- `rm -r /home/user/old_folder` – Recursively removes a directory and its contents.

**Tips**:
- Use `rm -i` for interactive mode, prompting before each removal.
- Be cautious with `rm -rf`, as it forcefully removes files without confirmation.



# 7. `touch` - Create a New File

**Description**: The `touch` command creates an empty file or updates the timestamp of an existing file.

**Syntax**: `touch filename`

**Examples**:
- `touch newfile.txt` – Creates an empty file named `newfile.txt`.

**Tips**:
- Useful for quickly creating files without content for testing or scripting.



# 8. `mkdir` - Make Directory

**Description**: The `mkdir` command creates a new directory.

**Syntax**: `mkdir [options] directory_name`

**Examples**:
- `mkdir new_directory` – Creates a directory named `new_directory`.
- `mkdir -p /home/user/new/dir/structure` – Creates nested directories.

**Tips**:
- Use `mkdir -p` to create parent directories if they do not exist.



# 9. `ls -l` - Detailed Directory Listing

**Description**: The `ls -l` command lists directory contents with detailed information.

**Syntax**: `ls -l [directory_path]`

**Examples**:
- `ls -l` – Lists contents with details such as permissions, owner, size, and date.

**Tips**:
- Combine with `grep` to filter detailed listings: `ls -l | grep .txt`.



# 10. `stat` - File Status

**Description**: The `stat` command provides detailed information about a file or directory.

**Syntax**: `stat [file]`

**Examples**:
- `stat file.txt` – Displays detailed information about `file.txt`.

**Tips**:
- Useful for getting inode numbers, block size, and access times.


>[!Next]-
> Next we will try and [[Connect to OMNI|connect to the cluster]]!