################################################################################
import json
import base64
import re
import inspect
import sys
from copy import deepcopy
import arrow
import os

################################################################################
PSL_OVERRIDE_PARAMS_CALL_PREFIX = "--updateGlobals "
PSL_PYTHON_PATH = "python"
DEBUG = True


################################################################################
def PSLLaunch(scriptFile, scriptArgs, globalParams):
    return os.system(PSL_PYTHON_PATH + " " + scriptFile + " " + scriptArgs + " " + PSL_OVERRIDE_PARAMS_CALL_PREFIX + PSLEncodeParamsForCallArgs(globalParams))


################################################################################
def PSLEncodeParamsForCallArgs(params):
    return base64.b64encode(bytes(json.dumps(params), "utf-8")).decode("utf-8")


################################################################################
def PSLUpdateGlobalsFromEncodedCallArgs():
    regexParams = re.compile(PSL_OVERRIDE_PARAMS_CALL_PREFIX + "\s*=?\s*([0-9a-z=]+)", re.S | re.I)
    matches = regexParams.findall(" ".join(sys.argv))
    if len(matches) > 0:
        try:
            debug("Updating global params from call args")
            jsonParams = matches[0]
            params = json.loads(base64.b64decode(jsonParams).decode("utf-8"))
            frame = inspect.currentframe()
            for param in params:
                if param in frame.f_back.f_locals:
                    if isinstance(params[param], dict):
                        debug("Updating global param dict from call args", param, params[param])
                        frame.f_back.f_locals[param] = mergeDictionnaries(frame.f_back.f_locals[param], params[param])
                    else:
                        debug("Updating global param from call args", param, params[param])
                        frame.f_back.f_locals[param] = params[param]
                else:
                    debug("Can't find global param from call args, defining instead of updating", param)
                    frame.f_back.f_locals[param] = params[param]
        except: warning("Can't parse global params overrides from call args")


################################################################################
def mergeDictionnaries(mainDictionnary, overridingDictionnary):
    if not isinstance(overridingDictionnary, dict): return overridingDictionnary
    result = deepcopy(mainDictionnary)
    for k, v in overridingDictionnary.items():
        if k in result and isinstance(result[k], dict): result[k] = mergeDictionnaries(result[k], v)
        else: result[k] = deepcopy(v)
    return result


################################################################################
################################################################################
################################################################################
COLOR_BLUE = '\033[94m'
COLOR_GREEN = '\033[92m'
COLOR_ORANGE = '\033[93m'
COLOR_RED = '\033[91m'
COLOR_NEUTRAL = '\033[0m'
COLOR_BOLD = '\033[1m'
COLOR_UNDERLINE = '\033[4m'


################################################################################
def info(*args):
    printLineColored("[NFO] - " + formatTimestamp(arrow.now().timestamp, "YYYY/MM/DD HH:mm:ss") + " - " + makeMessageFromArgsArray(args), COLOR_BLUE)


################################################################################
def warning(*args):
    printLineColored("[WRN] - " + formatTimestamp(arrow.now().timestamp, "YYYY/MM/DD HH:mm:ss") + " - " + makeMessageFromArgsArray(args), COLOR_ORANGE)


################################################################################
def success(*args):
    printLineColored("[OK!] - " + formatTimestamp(arrow.now().timestamp, "YYYY/MM/DD HH:mm:ss") + " - " + makeMessageFromArgsArray(args), COLOR_GREEN)


################################################################################
def failure(*args):
    printLineColored("[KO!] - " + formatTimestamp(arrow.now().timestamp, "YYYY/MM/DD HH:mm:ss") + " - " + makeMessageFromArgsArray(args), COLOR_RED)
    sys.exit(0)


################################################################################
def debug(*args):
    if DEBUG: printLine("[DBG] - " + formatTimestamp(arrow.now().timestamp, "YYYY/MM/DD HH:mm:ss") + " - " + makeMessageFromArgsArray(args))


################################################################################
def printLine(string):
    print(string)


################################################################################
def printLineColored(string, color):
    printLine(color + string + COLOR_NEUTRAL)


################################################################################
def printSeparator():
    try: rows, columns = os.popen('stty size', 'r').read().split()
    except: columns = 30
    for i in range(0, int(columns)): sys.stdout.write("-")
    print


################################################################################
def formatTimestamp(timestamp, dateFormat="DD-MM-YYYY"):
    return arrow.get(timestamp).format(dateFormat)


################################################################################
def makeMessageFromArgsArray(args):
    cleanedArgs = []
    for arg in args: cleanedArgs.append(dumps(arg).strip('"'))
    return ' / '.join(cleanedArgs)


################################################################################
def dumps(obj):
    return json.dumps(obj, default=JSONPrintSetDefault)


################################################################################
def JSONPrintSetDefault(obj):
    if isinstance(obj, set): return list(obj)
    return str(obj)
