import os
#def select_character():
def list_subfolders(folder_path = r'character_catalog'):
        subfolders = [f.name for f in os.scandir(folder_path) if f.is_dir()]
        if "__pycache__" in subfolders:
            subfolders.remove("__pycache__")
        return subfolders
def voice_id(file_path):
   """Checks if a file exists at the given path and reads its contents if it does.

   Args:
       file_path (str): The path to the file to check.

   Returns:
       str: The contents of the file if it exists, otherwise None.
   """

   if os.path.exists(file_path) and os.path.isfile(file_path):
       try:
           with open(file_path, 'r') as file:
               data = file.read()
           return data
       except Exception as e:
           #print(f"Error reading file: {e}")
           return "2EiwWnXFnvU5JabPnv8n"
   else:
       #print(f"File not found at path: {file_path}")
       return "2EiwWnXFnvU5JabPnv8n"
    
def read_data_in_subfolder(selected_subfolder,folder_path = r'character_catalog'):
        subfolder_path = os.path.join(folder_path, selected_subfolder)
    
        # Read content of the "system" file
        '''system_file_path = os.path.join(subfolder_path, 'system')
        with open(system_file_path, 'r') as system_file:
             system_content = system_file.read()
            #print("Content of : {}".format( system_content))'''
    
        # Read content of files in the "data" folder
        data_folder = os.path.join(subfolder_path, 'data')
        
    
        
        with open(f'{data_folder}/background.txt', 'r') as data_content:
            background = data_content.read()
            #print(background)
        #with open(f'{data_folder}/talk.csv', 'r') as data_content:
            #talk = data_content.read()
            #print(talk)'''
        #Replace 'C:\\Users\\DELL\\OneDrive\\Desktop\\AR_main\\character_catalog' with the actual path to your main folder
            

        voice=voice_id(f'{data_folder}/voice.txt')     
        #return [background,system_content,selected_subfolder]
        return [background,selected_subfolder,voice]



    
'''# List all subfolders
    subfolders = list_subfolders()
    print("Characters: ")
    for idx, subfolder in enumerate(subfolders, start=1):

        print(f"{idx}. {subfolder}")
    
    # Prompt the user to select a subfolder
    selected_index = int(input("Enter the number of the character you want to talk: "))
    selected_subfolder = subfolders[selected_index - 1]
    
    # Read data inside the selected subfolder
    return read_data_in_subfolder(selected_subfolder)
#l=select_character()
#print(l) '''
