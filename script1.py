################################################################################
import lib as l
import sys

################################################################################
# PARAMS DEFINITIONS
################################################################################
dictParams = {"param1": 8, "param4": "lucas"}
valueParam = "white"
l.PSLUpdateGlobalsFromEncodedCallArgs() # Override params if they were provided
################################################################################
# MAIN
################################################################################
print(sys.argv)
print(dictParams)
print(valueParam)
