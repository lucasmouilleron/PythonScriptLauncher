Python Script Launcher
======================

PSL : A simple python script launcher with global params overridance.

![Screenshot](http://grabs.lucasmouilleron.com/Screen%20Shot%202016-08-22%20at%2014.37.58.png)

Concept
-------
- It happens you need to run some scripts in a row
- It happens as well you need to run a script with different params contexts
- PSL allows to launch scripts and externally override global params
- In a script, `lib.PSLUpdateGlobalsFromEncodedCallArgs()` hooks PSL in (previously defined global params can be potentially overriden)
- From a launcher script, `lib.PSLLaunch(scriptFile, scriptArgs, globalParams)` will launch the script `scriptFile`, with args `scriptArgs`, and will override global params with `globalParams`
- `globalParams` is a dictionnary of global params :
    - The keys are the name of a script global params
    - If the global param is not defined in the script, no failure
    - If the the global param is defined in the script : 
        - If it is a dictionnary, the dics are merged
        - If not, the value is overriden
- The `globalParams` are actually sent to the script as a base64 encoded string as the named arg `--updateGlobals`


Demo implementation
-------------------
- `scriptLauncher.py` is the launcher script
- `scriptX.py` are test launched scripts
- `params.json` is defining `groups` of `runs`
- A `run` is a python script + its global params overridances
- Tests: 
    - Manual / traditionnal launching : `python script1.py`
    - PSL lauching on all groups : `python scriptLauncher.py all`
    - PSL lauching on a specific group : `python scriptLauncher.py smalls`

Installation
------------
- python 3
- `pip install -r requirements.txt`