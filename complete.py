import tkinter as tk
import os
import datetime
import zipfile
from cryptography.fernet import Fernet

class CustomCLI():
    def __init__(self, master): #initializing the CLI interface
        self.master = master
        master.title("Custom CLI Simulation")

        # Current directory
        self.current_directory = os.getcwd()

        # History text
        self.history_text = tk.Text(master, height=10, width=80)
        self.history_text.pack(side=tk.TOP, padx=10, pady=10)
        self.history_text.insert(tk.END, f"Current Directory: {self.current_directory}\n\n")

        # Input frame
        input_frame = tk.Frame(master)
        input_frame.pack(side=tk.BOTTOM, padx=10, pady=10)

        # Command Label
        self.command_label = tk.Label(input_frame, text="Command:")
        self.command_label.pack(side=tk.LEFT)

        # Command Entry
        self.command_entry = tk.Entry(input_frame, width=50)
        self.command_entry.pack(side=tk.LEFT, padx=5)

        # Execute Button
        self.execute_button = tk.Button(input_frame, text="Execute", command=self.execute_command)
        self.execute_button.pack(side=tk.LEFT, padx=5)

        # Clear Screen Button
        self.clear_screen_button = tk.Button(input_frame, text="Clear Screen", command=self.clear_screen)
        self.clear_screen_button.pack(side=tk.LEFT, padx=5)

        # Bindings
        self.master.bind('<Return>', lambda event=None: self.execute_command())
        self.master.bind('<Up>', self.navigate_command_history)
        self.master.bind('<Down>', self.navigate_command_history)
        
        # Initialize command history
        self.command_history = []
        self.current_command_index = -1
    
    def encrypt_file(self, file_path):
        try:
            # Generate a Fernet key and save it to a file
            key = Fernet.generate_key()
            with open('encryption_key.key', 'wb') as key_file:
                key_file.write(key)

            # Read the file content
            with open(file_path, 'rb') as file:
                file_data = file.read()

            # Create a Fernet cipher suite and encrypt the file content
            cipher_suite = Fernet(key)
            encrypted_data = cipher_suite.encrypt(file_data)

            # Save the encrypted content to the same file
            with open(file_path, 'wb') as file:
                file.write(encrypted_data)

            self.history_text.insert(tk.END, f"Encrypted file: {file_path}\n")
        except Exception as e:
            self.history_text.insert(tk.END, f"Error encrypting file: {str(e)}\n")
        self.history_text.see(tk.END)

    def decrypt_file(self, file_path):
        try:
            # Read the Fernet key from the key file
            with open('encryption_key.key', 'rb') as key_file:
                key = key_file.read()

            # Read the encrypted file content
            with open(file_path, 'rb') as file:
                encrypted_data = file.read()

            # Create a Fernet cipher suite and decrypt the file content
            cipher_suite = Fernet(key)
            decrypted_data = cipher_suite.decrypt(encrypted_data)

            # Save the decrypted content to the same file
            with open(file_path, 'wb') as file:
                file.write(decrypted_data)

            self.history_text.insert(tk.END, f"Decrypted file: {file_path}\n")
        except Exception as e:
            self.history_text.insert(tk.END, f"Error decrypting file: {str(e)}\n")
        self.history_text.see(tk.END)
    
    def execute_command(self):
        command = self.command_entry.get().lower().strip()

        # Add the executed command to the history
        self.history_text.insert(tk.END, f"Command: {command}\n")
        self.history_text.see(tk.END)

        if command == "clear":
            self.clear_screen()
        elif command.startswith("open "):
            path_to_open = command.split(" ")[1]
            self.open_folder_or_file(path_to_open)
        elif command == "listdirectory":
            self.list_directory()
        elif command.startswith("delete "):
            file_or_folder = command.split(" ")[1]
            self.delete_file_or_folder(file_or_folder)
        elif command.startswith("create "):
            file_or_folder = command.split(" ")[1]
            self.create_file_or_folder(file_or_folder)
        elif command.startswith("rename "):
            names = command.split(" ")[1:]
            if len(names) == 2:
                old_name, new_name = names
                self.rename_file_or_folder(old_name, new_name)
            else:
                self.history_text.insert(tk.END, "Invalid 'rename' command. Format: rename <old_name> <new_name>\n")
                self.history_text.see(tk.END)
        elif command.startswith("search "):
            filename = command.split(" ")[1]
            self.search_file(filename)
        elif command.startswith("encrypt "):
            file_to_encrypt = command.split(" ")[1]
            self.encrypt_file(file_to_encrypt)
        elif command.startswith("decrypt "):
            file_to_decrypt = command.split(" ")[1]
            self.decrypt_file(file_to_decrypt)
        elif command == "viewproperties":
            self.view_properties()
        elif command == "sort size":
            self.sort_by_size()
        elif command == "sort name":
            self.sort_by_name()
        elif command == "sort date":
            self.sort_by_date()
        elif command == "sort type":
            self.sort_by_type()
        elif command.startswith("chdir "):
            path = command.split(" ")[1]
            self.change_directory(path)
        elif command == "chdir\\":
            self.move_to_parent_directory()
        elif command.startswith("viewproperties"):
            _, target_name = command.split(" ", 1)
            self.view_properties(target_name)
        elif command.startswith("chmod "):
            args = command.split(" ")[1:]
            if len(args) == 2:
                file_path, permissions = args
                try:
                    permissions = int(permissions, 8)  # Convert the octal string to an integer
                    self.change_permissions(file_path, permissions)
                except ValueError:
                    self.history_text.insert(tk.END, "Invalid permissions format. Please provide an octal value.\n")
                    self.history_text.see(tk.END)
            else:
                self.history_text.insert(tk.END, "Invalid 'chmod' command. Format: chmod <file_path> <permissions>\n")
                self.history_text.see(tk.END)
        elif command.startswith("compress "):
            file_to_compress = command.split(" ")[1]
            self.compress_file(file_to_compress)
        else:
            self.history_text.insert(tk.END, f"Unknown command: {command}\n")
            self.history_text.see(tk.END)
            if command.startswith("encrypt "):
                file_to_encrypt = command.split(" ")[1]
                self.encrypt_file(file_to_encrypt)
            elif command.startswith("decrypt "):
                command_parts = command.split(" ")
                if len(command_parts) == 3:
                    encrypted_file, output_file = command_parts[1], command_parts[2]
                    self.decrypt_file(encrypted_file, output_file)
                else:
                    self.history_text.insert(tk.END, "Invalid 'decrypt' command. Format: decrypt <encrypted_file> <output_file>\n")
                    self.history_text.see(tk.END)

        # Add the executed command to the history
        self.command_history.insert(0, command)
        self.current_command_index = -1  # Reset the index after a new command

        # Clear the command entry
        self.command_entry.delete(0, tk.END)

    def open_file(self, file_path):
        try:
            os.startfile(file_path)
            self.history_text.insert(tk.END, f"Opened file: {file_path}\n")
        except Exception as e:
            self.history_text.insert(tk.END, f"Error opening file: {str(e)}\n")
        self.history_text.see(tk.END)
        
    def open_folder(self, folder_name):
        folder_path = os.path.join(self.current_directory, folder_name)
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            self.current_directory = folder_path
            self.history_text.insert(tk.END, f"Opened folder: {folder_path}\n")
            os.startfile(folder_path)  # Open the folder using the default file explorer
        else:
            self.history_text.insert(tk.END, f"Folder not found: {folder_name}\n")
        self.history_text.see(tk.END)

    def open_folder_or_file(self, path):
        full_path = os.path.join(self.current_directory, path)

        if os.path.exists(full_path):
            if os.path.isdir(full_path):
                self.open_folder(full_path)
            elif os.path.isfile(full_path):
                self.open_file(full_path)
            else:
                self.history_text.insert(tk.END, f"Not a valid file or folder: {path}\n")
        else:
            self.history_text.insert(tk.END, f"File or folder not found: {path}\n")

        self.history_text.see(tk.END)

    def list_directory(self):
        items = os.listdir(self.current_directory)
        items_str = '\t, '.join(items)
        self.history_text.insert(tk.END, f"Contents of {self.current_directory}:\n\t{items_str}\n")
        self.history_text.see(tk.END)

    def delete_file_or_folder(self, file_or_folder):
        path = os.path.join(self.current_directory, file_or_folder)
        try:
            if os.path.exists(path):
                if os.path.isdir(path):
                    os.rmdir(path)
                    self.history_text.insert(tk.END, f"Deleted folder: {path}\n")
                else:
                    os.remove(path)
                    self.history_text.insert(tk.END, f"Deleted file: {path}\n")
            else:
                self.history_text.insert(tk.END, f"File or folder not found: {file_or_folder}\n")
        except Exception as e:
            self.history_text.insert(tk.END, f"Error deleting {file_or_folder}: {str(e)}\n")
        self.history_text.see(tk.END)

    def create_file_or_folder(self, file_or_folder):
        path = os.path.join(self.current_directory, file_or_folder)
        try:
            if "." in file_or_folder:
                # Create a file
                with open(path, 'w') as f:
                    pass
                self.history_text.insert(tk.END, f"Created file: {path}\n")
            else:
                # Create a folder
                os.mkdir(path)
                self.history_text.insert(tk.END, f"Created folder: {path}\n")
        except Exception as e:
            self.history_text.insert(tk.END, f"Error creating {file_or_folder}: {str(e)}\n")
        self.history_text.see(tk.END)

    def rename_file_or_folder(self, old_name, new_name):
        old_path = os.path.join(self.current_directory, old_name)
        new_path = os.path.join(self.current_directory, new_name)
        try:
            if os.path.exists(old_path):
                os.rename(old_path, new_path)
                self.history_text.insert(tk.END, f"Renamed: {old_path} to {new_path}\n")
            else:
                self.history_text.insert(tk.END, f"File or folder not found: {old_name}\n")
        except Exception as e:
            self.history_text.insert(tk.END, f"Error renaming: {str(e)}\n")
        self.history_text.see(tk.END)

    def search_file(self, filename):
        matches = [f for f in os.listdir(self.current_directory) if filename.lower() in f.lower()]
        if matches:
            self.history_text.insert(tk.END, f"Search results for '{filename}': {', '.join(matches)}\n")
        else:
            self.history_text.insert(tk.END, f"No matches found for '{filename}'\n")
        self.history_text.see(tk.END)

    def change_directory(self, path):
        try:
            os.chdir(path)
            self.current_directory = os.getcwd()
            self.history_text.insert(tk.END, f"Changed directory to: {self.current_directory}\n")
        except Exception as e:
            self.history_text.insert(tk.END, f"Error changing directory: {str(e)}\n")
        self.history_text.see(tk.END)
    
    def move_to_parent_directory(self):
        # Implement your logic to move to the parent directory
        parent_directory = os.path.dirname(self.current_directory)
        os.chdir(parent_directory)
        self.current_directory = os.getcwd()
        self.history_text.insert(tk.END, f"Moved to parent directory: {self.current_directory}\n")
        self.history_text.see(tk.END)
    
    def view_properties(self, target_name):
        try:
            selected_path = os.path.join(self.current_directory, target_name)
            if os.path.exists(selected_path):
                properties_text = f"Properties of: {selected_path}\n"
                properties_text += f"Size: {os.path.getsize(selected_path)} bytes\n"
                properties_text += f"Last Modified: {datetime.datetime.fromtimestamp(os.path.getmtime(selected_path))}\n"
                properties_text += f"Is Directory: {os.path.isdir(selected_path)}\n"
                properties_text += f"Is File: {os.path.isfile(selected_path)}\n"
                self.history_text.insert(tk.END, properties_text)
            else:
                self.history_text.insert(tk.END, f"File or folder not found: {target_name}\n")
        except Exception as e:
            self.history_text.insert(tk.END, f"Error retrieving properties: {str(e)}\n")

        self.history_text.see(tk.END)

    def sort_by_size(self):
        try:
            # Get a list of files in the current directory
            files = [f for f in os.listdir(self.current_directory) if os.path.isfile(os.path.join(self.current_directory, f))]

            # Sort files by size
            sorted_files = sorted(files, key=lambda f: os.path.getsize(os.path.join(self.current_directory, f)))

            # Display the sorted files
            sorted_files_text = f"Sorted by Size:\n\t{', '.join(sorted_files)}\n"
            self.history_text.insert(tk.END, sorted_files_text)
        except Exception as e:
            self.history_text.insert(tk.END, f"Error sorting by size: {str(e)}\n")

        self.history_text.see(tk.END)

    def sort_by_name(self):
        try:
            # Get a list of files in the current directory
            files = [f for f in os.listdir(self.current_directory) if os.path.isfile(os.path.join(self.current_directory, f))]

            # Sort files by name
            sorted_files = sorted(files)

            # Display the sorted files
            sorted_files_text = f"Sorted by Name:\n\t{', '.join(sorted_files)}\n"
            self.history_text.insert(tk.END, sorted_files_text)
        except Exception as e:
            self.history_text.insert(tk.END, f"Error sorting by name: {str(e)}\n")

        self.history_text.see(tk.END)

    def sort_by_date(self):
        try:
            # Get a list of files in the current directory
            files = [f for f in os.listdir(self.current_directory) if os.path.isfile(os.path.join(self.current_directory, f))]

            # Sort files by modification date
            sorted_files = sorted(files, key=lambda f: os.path.getmtime(os.path.join(self.current_directory, f)))

            # Display the sorted files
            sorted_files_text = f"Sorted by Date:\n\t{', '.join(sorted_files)}\n"
            self.history_text.insert(tk.END, sorted_files_text)
        except Exception as e:
            self.history_text.insert(tk.END, f"Error sorting by date: {str(e)}\n")

        self.history_text.see(tk.END)

    def sort_by_type(self):
        try:
            # Get a list of files in the current directory
            files = [f for f in os.listdir(self.current_directory) if os.path.isfile(os.path.join(self.current_directory, f))]

            # Sort files by type (file extension)
            sorted_files = sorted(files, key=lambda f: os.path.splitext(f)[1].lower())

            # Display the sorted files
            sorted_files_text = f"Sorted by Type:\n\t{', '.join(sorted_files)}\n"
            self.history_text.insert(tk.END, sorted_files_text)
        except Exception as e:
            self.history_text.insert(tk.END, f"Error sorting by type: {str(e)}\n")

        self.history_text.see(tk.END)

    def clear_screen(self):
        self.history_text.delete(1.0, tk.END)
        self.history_text.insert(tk.END, f"Current Directory: {self.current_directory}\n\n")

    def navigate_command_history(self, event):
        if event.keysym == "Up":
            if self.current_command_index < len(self.command_history) - 1:
                self.current_command_index += 1
                self.command_entry.delete(0, tk.END)
                self.command_entry.insert(0, self.command_history[self.current_command_index])
        elif event.keysym == "Down":
            if self.current_command_index >= 0:  # Change here
                self.current_command_index -= 1
                self.command_entry.delete(0, tk.END)
                if self.current_command_index >= 0:  # Change here
                    self.command_entry.insert(0, self.command_history[self.current_command_index])
    
    def change_permissions(self, file_path, permissions):
        try:
            os.chmod(file_path, permissions)
            self.history_text.insert(tk.END, f"Changed permissions for {file_path} to {permissions}\n")
        except Exception as e:
            self.history_text.insert(tk.END, f"Error changing permissions: {str(e)}\n")
        self.history_text.see(tk.END)

    def compress_file(self, file_path):
            try:
                # Get the base name of the file or folder
                base_name = os.path.basename(file_path)

                # Create a ZIP file with the same base name
                zip_file_path = os.path.join(self.current_directory, f"{base_name}.zip")
                with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
                    if os.path.isfile(file_path):
                        # If it's a file, add the file to the ZIP archive
                        zip_file.write(file_path, base_name)
                    elif os.path.isdir(file_path):
                        # If it's a directory, add all files and subdirectories to the ZIP archive
                        for foldername, subfolders, filenames in os.walk(file_path):
                            for filename in filenames:
                                file_path = os.path.join(foldername, filename)
                                arcname = os.path.relpath(file_path, foldername)
                                zip_file.write(file_path, arcname)

                self.history_text.insert(tk.END, f"Compressed: {file_path} to {zip_file_path}\n")
            except Exception as e:
                self.history_text.insert(tk.END, f"Error compressing: {str(e)}\n")
            self.history_text.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = CustomCLI(root)
    root.mainloop()