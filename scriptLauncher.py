################################################################################
import lib as l
import sys
import json
import os
import pipes

################################################################################
# CONFIG
################################################################################
ROOT_FOLDER = os.path.dirname(os.path.realpath(__file__))
ALL_RUNS_KEYWORD = "all"
PARAMS_FILE = "/".join([ROOT_FOLDER, "params.json"])

################################################################################
# LOAD PARAMS FROM JSON FILE
################################################################################
groupNameProvided = sys.argv[1] if len(sys.argv) > 1 else l.failure("Must provide a group name which is a config key", PARAMS_FILE)
try: runnerParams = json.load(open(PARAMS_FILE))
except: l.failure("The config file is absent or syntax is not valid ", PARAMS_FILE)
if groupNameProvided == "all": groupNames = list(runnerParams.keys())
elif groupNameProvided not in runnerParams: l.failure("Group name is not configured", groupNameProvided)
else: groupNames = [groupNameProvided]

################################################################################
# LAUNCH GROUPS AND RUNS
################################################################################
l.printSeparator()
l.info("Running groups", groupNames)
l.printSeparator()
nbRuns = 0
indexOverall = 0
for groupName in groupNames: nbRuns += len(runnerParams[groupName]["runs"])
for groupName in groupNames:
    groupDatas = runnerParams[groupName]
    l.info("Running group", groupName)
    l.printSeparator()
    for index in range(len(groupDatas["runs"])):
        runDatas = groupDatas["runs"][index]
        script = runDatas["script"]
        l.info("Running run", groupName, script, indexOverall + 1, nbRuns)
        returnValue = l.PSLLaunch(pipes.quote("/".join([ROOT_FOLDER, script])), runDatas["args"] if "args" in runDatas else "", l.mergeDictionnaries(groupDatas["globalParams"], runDatas["params"] if "params" in runDatas else {}))
        if returnValue != 0: l.failure("Group failed because of failing script", groupName, script, indexOverall + 1)
        indexOverall += 1
        l.printSeparator()
    l.success("Group run succeded", groupName)
    l.printSeparator()
l.success("Groups finished")
l.printSeparator()
