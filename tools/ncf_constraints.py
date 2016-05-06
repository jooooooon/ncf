import re
import subprocess
import json
import os.path
import shutil
import sys
import os
import codecs


### Constraint checking function 

def from_list( parameter, accepted_result):
  return parameter in accepted_result

def max_length( parameter, max_size):
  return parameter.length <= max_size

def min_length( parameter, min_size):
  return parameter.length >= min_size

def match_regexp(parameter, regexp):
  match = re.match(regexp, parameter, re.S)
  return match is not None

def not_match_regexp(parameter, regexp):
  return not match_regexp(parameter, regexp)

string_constraints = {
    "default" : "^\S(.*\S)?$"
  , "allow_whitespace_string" : "^.+$"
  , "allow_empty_string" : "^(\S(.*\S)?)?$"
  , "all" : ".*"
}

def check_parameter(parameter, constraint):
  """Checks that a parameter is ok with the constraint passed as parameter"""

  # First check 'string' constraint
  string_constraint = "default"
  empty_constraint = constraint.get("allow_empty_string", False)
  if constraint.get("allow_whitespace_string", False):
    if empty_constraint:
      string_constraint = "all"
    else:
      string_constraint = "allow_whitespace_string"
  elif empty_constraint:
    string_constraint = "allow_empty_string"
  string_regex = string_constraints[string_constraint]
  result = match_regexp(parameter, string_regex)

  # Check if in list of accepted values
  if result:
    if "list" in constraint:
      result = from_list(parameter, constraint["list"])

  # Check regexps constraints
  if result:
    if "regexp" in constraint:
      result = match_regexp(parameter, constraint["regexp"])

  if result:
    if "not_regexp" in constraint:
      result = not_match_regexp(parameter, constraint["not_regexp"])

  # Check length constraints
  if result:
    if "min" in constraint:
      result = min_length(parameter, constraint["min"])

  if result:
    if "max" in constraint:
      result = max_length(parameter, constraint["max"])
  
  return result


constraint_type = {
    "allow_whitespace_string" : bool
  , "allow_empty_string" : bool
  , "list" : list
  # use unicode for regexps, since they will be parsed as unicode ... 
  , "regexp" : unicode
  , "not_regexp": unicode
  , "max" : int
  , "min" : int
}

def check_constraint_type(key, value):
  return type(value) is constraint_type[key]
