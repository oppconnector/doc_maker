# workflow:

#1: open all files in project folder

#2: covert files to raw text
#3: combine all text into one long string

#4: chunk text
#5: ai embed/vectorize text chunks
#6: save to db (pandas for temporary saving)

#7: open template html document
#8: pull prompts out of html document

#9: answer each prompt with RAG
#10: convert RAG answer to HTML
#11: replace prompt with HTML RAG answer

#12: convert HTML as pdf file
#13: save pdf file with template name and date time stamp 

print("Starting doc_maker.py")

#python libraries:
################################################################################
################################################################################

print("Loading standard python libraries")
#standard python libraries:
import os

print("Loading pip python libraries")
#pip python libraries:

print("Loading custom python libraries")
#custom libraries:
from read_doc import read_doc
from ai import embed

print("All python libraries have been loaded")
################################################################################
################################################################################


#program variables
################################################################################
################################################################################
input_docs_folder_path = "input_docs"

################################################################################
################################################################################







#main program:
################################################################################
################################################################################
def main():
    print("Now running main program")

    #1: open all files in project folder
    input_docs_files_list = list_files_in_folder(input_docs_folder_path)

    all_doc_text = ""
    for doc in input_docs_files_list:
        doc_file_path = f"{input_docs_folder_path}/{doc}"
        print(f"Reading: {doc_file_path}")

        #2: covert files to raw text
        doc_text = read_doc(doc_file_path)
        #print(f"Doc Text: \n{doc_text}")

        #3: combine all text into one long string
        all_doc_text = all_doc_text + f" ||| DOCUMENT:{doc} TEXT>>> " + doc_text

    input("wait")
    print(all_doc_text)
################################################################################
################################################################################





#functions
################################################################################
################################################################################
def list_files_in_folder(folder_path):
    """
    List all files in the specified folder.

    :param folder_path: Path to the folder as a string
    :return: A list of file names in the folder
    """
    try:
        # Use os.listdir to get all entries in the directory
        entries = os.listdir(folder_path)
        
        # Filter out directories, keeping only files
        files = [f for f in entries if os.path.isfile(os.path.join(folder_path, f))]
        
        return files
    except FileNotFoundError:
        print(f"The folder '{folder_path}' does not exist.")
        return []
    except PermissionError:
        print(f"You do not have permission to access '{folder_path}'.")
        return []







################################################################################
################################################################################



#starts main (should always be at the bottom)
################################################################################
################################################################################
if __name__ == "__main__":
    main()
################################################################################
################################################################################