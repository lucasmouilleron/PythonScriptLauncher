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
- In this implementation of `scriptLauncher.py`, `params.json` is used to define `groups` of `runs`
- A `run` is a script + its global params overridances
- A `group` is a set of `runs`
- Therefore the workflow is : 
    - Work on your script and define some params : 
        - `dictParams = {"param1": 8, "param4": "lucas"}`
        - `valueParam = "white"`
    - Allow PSL to hook in and override params if necessary : 
        - `lib.updateGlobalsFromEncodedCallArgs()`
        - Global params defined above can now be overriden
    - Launch your script manually as usual : `python script.py`
    - Or launch from PSL : 
        - Run configuraiton for the script(s) are defined in the `params.json` file
        - `python scriptLauncher.py all`
- Tests: 
    - Manual / traditionnal launching : `python script1.py`
    - PSL lauching on all groups : `python scriptLauncher.py all`
    - PSL lauching on a specific group : `python scriptLauncher.py smalls`

Installation
------------
- python 3
- `pip install -r requirements.txt`