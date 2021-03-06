Installation
======================================

Pecos requires Python (2.7, 3.4, or 3.5) along with several Python 
package dependencies.  Information on installing and using Python can be found at 
https://www.python.org/.  Python distributions, such as Anaconda,
are recommended to manage the Python interface.  
Anaconda Python distributions include the Python packages needed to run Pecos.

Pecos can be installed using pip, git, or a downloaded zip file.  
Note that the pip installation will NOT include the examples folder referenced in this manual.

**pip:** To install Pecos using pip::

	pip install pecos 
	
**git**: To install Pecos using git::

	git clone https://github.com/sandialabs/pecos
	cd pecos
	python setup.py install

**zip file**: To install Pecos using a downloaded zip file, go to https://github.com/sandialabs/pecos, 
select the "Clone or download" button and then select "Download ZIP".
This downloads a zip file called pecos-master.zip.
To download a specific release, go to https://github.com/sandialabs/pecos/releases and select a zip file.
The software can then be installed by unzipping the file and running setup.py::

	unzip WNTR-master.zip
	cd WNTR-master
	python setup.py install
		
Required Python package dependencies include:

* Pandas [Mcki13]_: used to analyze and store time series data, 
  http://pandas.pydata.org/
* Numpy [VaCV11]_: used to support large, multi-dimensional arrays and matrices, 
  http://www.numpy.org/
* Jinja [Rona08]_: used to generate HTML templates, 
  http://jinja.pocoo.org/
* Matplotlib [Hunt07]_: used to produce figures, 
  http://matplotlib.org/

Optional Python packages dependencies include:

* sqlalchemy: used to insert collected data into a MySQL database,
  https://www.sqlalchemy.org/
* minimalmodbus: used to read modbus device sensors values, 
  https://minimalmodbus.readthedocs.io
* pyyaml: used to store configuration options in human readable data format,
  http://pyyaml.org/
* PVLIB [SHFH16]_: used to simulate the performance of photovoltaic energy systems,
  http://pvlib-python.readthedocs.io/

All other dependencies are part of the Python Standard Library.

To use Pecos, import the package from a Python console::

	import pecos	