# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 11:42:10 2018

@author: osama
"""
import os
import shutil
from os.path import expanduser



def make_pypi_folders(pypirc_username,pypirc_password,directory_of_new_folder,name_of_project,directory_of_python_files,version_number,author_name_full,author_email,short_description,github_url,python_version,path_readme_source="",invoke_python_by_name='python',license_type="MIT License",operating_system="OS Independent"):
    '''
    pypirc_username: string; username of the account you created at pypi
    pypirc_password: string; username of the account you created at pypi
    directory_of_new_folder : string; path of where you want the new folder to be
    name_of_project: string; name of the project as you wish it to appear on pypi
    directory_of_python_files: (list of) strings; paths to where your python files reside which you want to upload
    version_number: string: version number of this project
    author name full: string; author name in full
    author_email: string; author email ID
    short_description: string; short description of this project
    github_url: string; URL of code of this as hosted on GitHub
    python_version: string;  2 or 3
    invoke_python_by_name (optional if ='python') : string; keyword of how you invoke python files on terminal
    license_type (optional if MIT license): string; type of license
    operating_system (optional if independent) : string; info about on which platforms is this targeted for
    '''
    
    path_first_directory = r''+directory_of_new_folder+'/'+name_of_project+'/'
    path_second_directory = path_first_directory+name_of_project+'/'
    os.makedirs(path_first_directory)
    os.makedirs(path_second_directory)

    if(type(directory_of_python_files)==list):
        for each in directory_of_python_files:
            shutil.copy2(each,path_second_directory)
    else:
        shutil.copy2(directory_of_python_files,path_second_directory)
    
    change_dir(path_first_directory)
    create_init_file(path_second_directory,name_of_project)
    create_readme(path_first_directory,path_readme_source)
    create_setup_py(path_first_directory,name_of_project,version_number,author_name_full,author_email,short_description,github_url,python_version,license_type,operating_system)
    create_license_file(path_first_directory,author_name_full,license_type)
    upload_on_pypi(pypirc_username,pypirc_password,path_first_directory,invoke_python_by_name)
    
    
def create_init_file(path,name_of_project):
    f=open(path+'__init__.py',"w+")
    f.write("name = \""+str(name_of_project)+"\"")
    f.close()
    
def create_setup_py(path,name_of_project,version_number,author_name_full,author_email,short_description,github_url,python_version,license_type,operating_system):
    f= open(path+'setup.py',"w+")
    f.write('import setuptools\nwith open("README.md", "r") as fh:\n\
\tlong_description = fh.read()\n\
setuptools.setup(\n\
\tname="'+name_of_project+'",\n\
\tversion="'+version_number+'",\n\
\tauthor="'+author_name_full+'",\n\
\tauthor_email="'+author_email+'",\n\
\tdescription="'+short_description+'",\n\
\tlong_description=long_description,\n\
\tlong_description_content_type="text/markdown",\n\
\turl="'+github_url+'",\n\
\tpackages=setuptools.find_packages(),\n\
\tclassifiers=[\n\
\t"Programming Language :: Python :: '+str(python_version)+'",\n\
\t"License :: OSI Approved :: '+license_type+'",\n\
\t"Operating System :: '+operating_system+'",\n\
\t],\n\
)')    
    f.close()
    
def create_readme(path_readme_destination,path_readme_source=""):
    if(path_readme_source==""):
        f= open(path_readme_destination+'README.md',"w+")
        f.write("# Example Package \n\
    This is a simple example package. You can use\n\
    [Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)\n\
    to write your content.")
        f.close()
    else:
        shutil.copy2(path_readme_source,path_readme_destination)
        
    
def create_license_file(path,author_name_full,license_type):
    f= open(path+'LICENSE',"w+")
    f.write("MIT License\n\
Copyright (c) [year] ["+author_name_full+"]\n\n\
Permission is hereby granted, free of charge, to any person obtaining a copy\n\
of this software and associated documentation files (the \"Software\"), to deal\n\
in the Software without restriction, including without limitation the rights\n\
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n\
copies of the Software, and to permit persons to whom the Software is\n\
furnished to do so, subject to the following conditions:\n\n\
The above copyright notice and this permission notice shall be included in all\n\
copies or substantial portions of the Software.\n\n\
THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n\
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n\
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n\
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n\
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n\
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n\
SOFTWARE.")
    f.close()
    
def upload_on_pypi(pypirc_username,pypirc_password,setup_py_path,invoke_python_by_name):
    
    make_pypirc_file(pypirc_username,pypirc_password)
    os.system(""+(invoke_python_by_name)+" -m pip install --user --upgrade setuptools wheel >tmp1")
    os.system(""+(invoke_python_by_name)+" setup.py sdist bdist_wheel > tmp2")
    os.system(""+(invoke_python_by_name)+" -m pip install --user --upgrade twine >tmp3")
    status=os.system("twine upload dist/* >tmp4")
    if(status==0):
        print("Succefully uploaded to PyPi!")
    else:
        print("THERE WAS SOME ERROR WITH UPLOADING...")
        print open('tmp1', 'r').read()
        print open('tmp2', 'r').read()
        print open('tmp3', 'r').read()
        print open('tmp4', 'r').read()
    
    os.remove('tmp1')
    os.remove('tmp2')
    os.remove('tmp3')
    os.remove('tmp4')
    
def change_dir(path):
    os.chdir(path)
    
def make_pypirc_file(pypi_username,pypi_password):
    path_home = expanduser("~")
    f= open(path_home+'/.pypirc',"w+")
    f.write("[distutils] \n\
index-servers= \n\
\tpypi \n\
[pypi] \n\
repository: https://upload.pypi.org/legacy/ \n\
username = "+pypi_username+" \n\
password = "+pypi_password+"")

# run_this_file('daroodar')


    
    