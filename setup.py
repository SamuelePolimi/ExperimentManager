from distutils.core import setup

#This is a list of files to install, and where
#(relative to the 'root' dir, where setup.py is)
#You could be more specific.
files = ["core/*", "utils/*"]

setup(name = "expman",
    version = "1.0.0",
    description = "ExperimentManager: make easier your experiments.",
    author = "Samuele Tosatto",
    author_email = "samuele.tosatto@gmail.com",
    url = "https://github.com/SamuelePolimi/ExperimentManager",
    #Name the folder where your packages live:
    #(If you have other packages (dirs) or modules (py files) then
    #put them into the package directory - they will be found 
    #recursively.)
    packages = ['ExpMan'],
    #'package' package must contain files (see list above)
    #I called the package 'package' thus cleverly confusing the whole issue...
    #This dict maps the package name =to=> directories
    #It says, package *needs* these files.
    package_data = {'ExpMan' : files },
    #'runner' is in the root.
    scripts = ["runner"],
    long_description = """"""  #TODO: add long descr
    #
    #This next part it for the Cheese Shop, look a little down the page.
    #classifiers = []     
) 
