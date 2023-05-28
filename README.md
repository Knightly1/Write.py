Write.py
=========

Write.py is a simple Python module for logging text. It is designed to be easy to use and to have a very simple syntax.  It is a wrapper around the Python module colorlog which is itself a wrapper around the Python module logging.

Installation
------------
To install Write.py, clone the repository and run the following command:
```bash
pip install -r requirements.txt
```

Usage
-----
A simple example of usage is as follows:
```python
from write import Write

log = Write()

log.info("Hello world")
```
This will output a colored line that looks like the following:
```
INFO  :: Hello world
```

The default log level is INFO.  You can change the log level by passing the level parameter to the Write constructor.  For example:
```python
from write import Write

log = Write(log_level="debug")

log.debug("Hello world")
```

You can disable color output by passing the use_colors parameter to the Write constructor.  For example:
```python
from write import Write

log = Write(use_colors=False)

log.info("Hello world")
```

You can enable timestamps by passing the date_format parameter to the Write constructor.  For example:
```python
from write import Write

log = Write(date_format="%Y-%m-%d %H:%M:%S")

log.info("Hello world")
```

You can also format the output by passing the format_string parameter to the Write constructor.  For example:
```python
from write import Write

log = Write(format_string="%(asctime)s---%(levelname)s---%(message)s")

log.info("Hello world")
```

And all of the options above can be combined.  For example:
```python
from write import Write

log = Write(log_level="debug", use_colors=False, date_format="%Y-%m-%d %H:%M:%S", format_string="%(asctime)s---%(levelname)s---%(message)s")

log.debug("Hello world")
```

Logging Levels
--------------
The default logging levels are:
* `trace` - Usually used for debugging as the author
* `debug` - Usually used for debugging with the end user
* `info` - Usually used for logging the execution of a program
* `warn` - Usually used for logging a warning that something might be wrong
* `error` - Usually used for logging an error that something went wrong
* `fatal` - Used for logging an error that something went wrong and the program will exit
* `help` - Used for logging a help message for the end user
