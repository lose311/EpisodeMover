import json
import os
import re
import shutil

def move_files():
    """ Move files/folders from source path to the show's directory

    Directory is specified by user, or if possible, loaded from data.json
    """
    if "defaultdirectory" in data:
        print("\n*** Default video source directory:", data["defaultdirectory"])
        srcdir = input("Enter '1' to use default video source directory\n"
                       "Otherwise, please enter the full path where your videos are located.\n"
                       "Example: C:\\user\\downloads\\ \n").strip()
        if srcdir.startswith('1'):
            srcdir = data["defaultdirectory"]
    else:
        srcdir = input("Please enter the full path where your videos are located.\n"
                       "Example: C:\\user\\downloads\\ \n").strip()
    while not os.path.isdir(srcdir):
        srcdir = input("\n*** Invalid directory. Please enter the full path where your "
                        "videos are located.\n Example: C:\\user\\downloads\\ \n").strip()
    data["defaultdirectory"] = srcdir
    save_json()
    print()
    for filename in os.listdir(srcdir):
        # Only look for folders/files in the format "S##E##". Example: "X-Files S01E02"
        if re.search('[sS]\\d{2}[eE]\\d{2}', filename):
            found = False
            filepath = os.path.join(srcdir, filename)
            name = filename.lower()
            for key in data:
                keywords = key.split()
                if all(word in name for word in keywords):
                    found = True
                    try:
                        shutil.move(filepath, data[key])
                    except Exception as e:
                        print("*** Error with {}".format(filename))
                        print("The file might be open in another program")
                        print(repr(e))
                    else:
                        print("*** Moved:", (filename[:41] + "...") if len(filename) > 44 else filename)
                    break
            if not found:
                # Prints the shows that matched the episode formatting, but were not
                # configured to be processed
                print("* Not processed:", (filename[:35] + '...') if len(filename) > 38 else filename)

def add_directory():
    """ Add directories to the data dictionary

    User provides keywords for each show and the directory for that show.
    Keywords are used so 'X.Files', 'X-Files', and 'X Files' will all be
    matched by the keywords 'X' and 'Files'
    """
    showKeywords = input("\nInput mandatory keywords for the show title seperated by a space.\n"
                         "Example: X files\n").lower().strip()
    while re.search('[^A-Za-z0-9 ]+', showKeywords) or showKeywords.startswith('defaultdirectory'):
        showKeywords = input("Invalid keywords, please input alphanumeric characters only\n" +
                             "Input mandatory keywords for the show title seperated by a space.\n"
                             "Example: X files\n").lower().strip()
    while showKeywords.lower() in data:
        showKeywords = input("Show already in database, enter new show keywords:\n")
    showPath = input("\nInput path for the folder for {}:\n".format(showKeywords) +
                     "Example: C:\\videos\\x files\n").strip()
    if not os.path.exists(showPath):
        os.makedirs(showPath)
        print("\n*** Directory did not exist. Created directory: '{}'".format(showPath))
    print("*** Move '{}' shows to directory: '{}'".format(showKeywords, showPath))
    data[showKeywords] = showPath
    save_json()

def remove_directory():
    """ Remove directory from data dictionary

    Remove show/directory from list and update data.json
    """
    count = 1
    # Creates a dict to map user selection numbers to keys of the data dict
    deleteDict = {}
    print('\n')
    for key in sorted(data):
        if not key.startswith('defaultdirectory'):
            print("{}. {} --> {}".format(count, key, data[key]))
            deleteDict[count] = key
            count += 1
    print("{}. Cancel".format(count))
    selection = input("\nSelect the number of the directory you want to delete:\n").strip()
    while (not selection.isdigit()) or (int(selection) not in deleteDict) and \
            (int(selection) != count):
        selection = input("Invalid selection. Select the number of the directory you want "
                          "to delete:\n").strip()
    selection = int(selection)
    if selection != count:
        print("\n*** {} has been deleted".format(deleteDict[selection]))
        del data[deleteDict[selection]]
    save_json()

def prompt():
    """ Prompt user for commands"""
    inpt = -1
    valid_choices = ['1','2','3','4','5']
    while inpt not in valid_choices:
        inpt = input("\nPlease select the number of the operation you wish "
                     "to complete:\n" +
                     "1. Run file mover\n2. Add directories"
                     "\n3. Remove directory\n4. View saved directories\n5. Quit\n").strip()
        if inpt not in valid_choices:
            print("\n*** Invalid choice ***")
    return inpt

def save_json():
    """ Save data to data.json for future use """
    with open(os.path.join(cwd, 'data.json'), 'w') as f:
        json.dump(data, f)

def print_data():
    """ Print data for user to view"""
    print("\n\n*** Loaded data:")
    if "defaultdirectory" in data:
        print("*** Default video source directory:", data["defaultdirectory"])
    for key in sorted(data):
        if key != "defaultdirectory":
            print("{} --> {}".format(key, data[key]))

if __name__ == "__main__":
    data = {}
    cwd = os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(os.path.join(cwd, 'data.json')):
        with open(os.path.join(cwd, 'data.json'), 'r') as f:
             data = json.load(f)
        print_data()

    choices = {
            '1': move_files,
            '2': add_directory,
            '3': remove_directory,
            '4': print_data,
            '5': exit
        }
    
    while True:
        selection = prompt()
        if selection in choices:
            handler = choices[selection]
            handler()
        else:
            print("Sorry, not a valid choice")
