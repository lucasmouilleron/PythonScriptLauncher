################################################################################
import lib as l

################################################################################
# PARAMS DEFINITIONS
################################################################################
dictParams = {"param1": 8, "param4": "lucas"}
dictParams2 = {"param1": 8, "param4": "lucas"}
l.PSLUpdateGlobalsFromEncodedCallArgs() # Override params if they were provided
################################################################################
# MAIN
################################################################################
print(dictParams)
print(dictParams2)
