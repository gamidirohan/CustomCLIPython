1. Executing Commands:
   - To execute a command, type the command in the "Command" entry field and either press the "Execute" button or press the "Enter" key.

2. Available Commands:
   - open <folder_name>:
     - Opens the specified folder.
     - Example: open Documents

   - listdirectory:
     - Lists the contents of the current directory.

   - clear:
     - Clears the screen.

   - delete <file_or_folder>:
     - Deletes the specified file or folder.
     - Example: delete myfile.txt

   - create <file_or_folder>:
     - Creates a new file or folder.
     - Example: create newfile.txt

   - move <source_path> <destination_path>:
     - Moves a file or folder from the source path to the destination path.
     - Example: move oldfile.txt /path/to/destination

   - rename <old_name> <new_name>:
     - Renames a file or folder.
     - Example: rename oldfile.txt newfile.txt

   - search <filename>:
     - Searches for a file in the current directory.
     - Example: search myfile.txt

   - encrypt <file>:
     - Encrypts the specified file.
     - Example: encrypt sensitive.doc

   - decrypt <file>:
     - Decrypts the specified encrypted file.
     - Example: decrypt sensitive.doc.encrypted

   - viewproperties <file_or_folder>:
     - Displays properties of the specified file or folder.
     - Example: viewproperties myfile.txt

   - sort size:
     - Sort the contents of the current directory based on size.

   - sort name:
     - Sorts the contents of the current directory based on name.

   - sort date:
     - Sorts the contents of the current directory based on modification date.

   - sort type:
     - Sorts the contents of the current directory based on file type.

3. Navigating Command History:
   - Press the Up Arrow key to navigate to previous commands in the command history.
   - Press the Down Arrow key to navigate to the next commands in the command history.

4. Clearing the Screen:
   - Press the "Clear Screen" button to clear the screen, including the result label and command history.

5. Compress file:
   - Compresses file using the zipfile library.

6. Change or set permissions for files:
       Read, Write, and Execute for Owner, and Read for Group and Others (Full Permissions):
       chmod 777 filename

       Read and Write for Owner, and Read for Group and Others:
       chmod 644 filename

       Read and Execute for Owner, and Read for Group and Others:
       chmod 544 filename

       Read and Write for Owner, and Read for Group (Owner has full permissions, Group can read and write, Others have no permissions):
       chmod 664 filename

       Read and Execute for Owner, and Read for Group (Owner can read and execute, Group can read, Others have no permissions):
       chmod 554 filename

       Read, Write, and Execute for Owner, Read and Execute for Group, and Read for Others (Owner has full permissions, Group can read and execute, Others can only read):
       chmod 711 filename

chdir - changing parent directory by giving path
chdir\ - to go to the present directories parent directory
chdir <foldername> - to go to a folder in the parent directory

Operating systems provide various file management features and functionalities to efficiently manage files and data. Here are some of the key file management features offered by operating systems:

1. File Creation: Operating systems allow users to create new files, specifying names, locations, and attributes.

2. File Deletion: Users can delete files, removing them from storage. Many operating systems move deleted files to a recycle bin or trash, allowing for potential recovery.

3. File Copying: Users can make duplicate copies of files, allowing data replication and backup.

4. File Moving: Files can be relocated within the file system, enabling organization and reconfiguration.

5. File Renaming: Users can change the name of files without altering the file's content.

6. File Searching: Operating systems often include search functionality to find files based on various criteria, including name, date, and content.

7. File Metadata: Files store metadata, including attributes like creation date, modification date, and file size.

8. File Permissions: Operating systems enforce file-level security through permissions. Users can specify who can access, modify, or delete files.

9. File Compression: Some operating systems offer file compression utilities to reduce file sizes and save storage space.

10. File Encryption: Certain operating systems support file encryption to protect data from unauthorized access.

11. File Sorting: Users can sort files based on different criteria, such as name, size, date, or type.

12. File and Folder Organization: Folders, directories, and file hierarchies are used to organize files in a structured manner.

These file management features are essential for maintaining an organized and secure file system, ensuring data availability, and facilitating efficient data manipulation and retrieval. The specific capabilities and tools available may vary depending on the operating system in use.
