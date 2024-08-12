import os 
import logging
from datetime import datetime 
import array as arr

# Set up logging for errors
#log_file = os.path.join(os.path.dirname(__file__), 'script_log.txt')
#logging.basicConfig(filename=log_file, level=logging.DEBUG, 
                   # format='%(asctime)s %(levelname)s:%(message)s')

def get_directory_sizes(project_path):
    project_size = 0  # initialize variable to keep track of total size of files in project
    project_number = 0  # initialize variable to keep track of total number of files in project
    subdir_files = {} #dictionary stores key-value pairs for subdirs and files numbers
    subdir_empties = [] #list stores directories with no files

    #logging.info(f'Starting to analyze directory: {project_path}')

    for root, _, files in os.walk(project_path, topdown=False):
        subdir_count = 0 #reset file count

        #logging.info(f'Analyzing directory: {root}')

        for file in files:  # iterating over files in each project and calculating their sizes

            file_path = os.path.join(root, file)  # concatenate absolute file path
            if len(file_path) > 260: #command to keep chars if too long
                file_path = f"\\\\?\\{file_path}"
            try:
                file_size = os.path.getsize(file_path)  # get size of each file in files
                project_size += file_size  # add to total size of the project
                project_number += 1  # increment number of files in project
                subdir_count +=1
                #logging.debug(f"File: {file} Size: {file_size} bytes")

            except FileNotFoundError:
                logging.error(f"File not found: {file_path}")
            except PermissionError:
                logging.error(f"Permission denied for file: {file_path}")
            except Exception as e:
                logging.error(f"Error accessing file {file_path}: {e}")

        if root != project_path:
            base_dir = os.path.basename(root)
            subdir_files[base_dir] = subdir_count 
            
            if subdir_count == 0:
                subdir_empties.append(base_dir)


    return project_size, project_number, subdir_files, subdir_empties


def generate_report(report_directory, proj_path, proj_size, proj_numb, subdir_files, subdir_empties):

        # create daily report with status of Survey directory
        todays_date = datetime.now().strftime("%y-%m-%d")
        base_name = os.path.basename(proj_path) #extract last part of project path
        report_name = f"{base_name}.html"
        #report_path = os.path.join(proj_path, report_name)  # concat directory file path and name of report
        report_path = os.path.join(report_directory, report_name) #throw all reports into one directory for all the reports
        
        subdir_details = ""
        list_empties =""
        for subdir, counts in subdir_files.items():
            if counts == 0:
                list_empties += f"<p>{subdir}</p>"
            else:
                subdir_details += f"<p>{subdir}: {counts} files</p>"

        #HTML template
        css_path = r"C:\Users\varvara.vorobieva\PyScripts\AuditorDaemon\style.css"
        html_content = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Report for {base_name}</title>
        <link rel="stylesheet" href="{css_path}">
        <script src="script.js"></script>
    </head>
    <body>
        <h1>Report for {base_name}</h1>
        <div class="info">
            <p>Date: {todays_date}</p>
            <p>Directory: {proj_path}</p>
            <p>Size of directory: {proj_numb} files, {proj_size} bytes</p>
        </div>
        <h2>Subdirectory File Distribution</h2>
        <div class="subdir-details"> {subdir_details}</div>
        <h2>Empty Directories</h2>
        <div class="subdir-details"> {list_empties}</div>
    </body>
    </html>"""

        try:
            with open(report_path, 'w') as file:  # write mode
                file.write(html_content) #write all html content
            #logging.info(f"Report written to {report_path}")
        except Exception as e:
            logging.error(f"Error writing report to {report_path}: {e}")

def get_project_sizes(root_dir, report_dir): #main function
    for item in os.listdir(root_dir):
        project = os.path.join(root_dir, item)
        if os.path.isdir(project): #checks if path is directory (sort out files)
            proj_size, proj_numb, subdir_files, subdir_empties = get_directory_sizes(project)
            generate_report(report_dir, project, proj_size, proj_numb, subdir_files, subdir_empties)


# MAIN BLOCK
if __name__ == "__main__":
    root_directory = r"C:\Users\varvara.vorobieva\OneDrive - Paradigm Geospatial\Survey\Projects"
    report_directory = r"C:\Users\varvara.vorobieva\OneDrive - Paradigm Geospatial\Survey\Projects\Active\_DataUseReports"
    get_project_sizes(root_directory, report_directory)