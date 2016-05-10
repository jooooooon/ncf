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
  return len(parameter) <= max_size

def min_length( parameter, min_size):
  return len(parameter) >= min_size

def match_regex(parameter, regex):
  match = re.search(regex, parameter)
  return match is not None

def not_match_regex(parameter, regex):
  return not match_regex(parameter, regex)

def check_parameter(parameter, constraint):
  """Checks that a parameter is ok with the constraint passed as parameter"""

  result = True
  errors = [];

  # First check 'string' constraints
  if not constraint.get("allow_empty_string", False):
    if match_regex(parameter, "^$"):
      errors.append("allow_empty_string")
      result = False

  if not constraint.get("allow_whitespace_string", False):
    if match_regex(parameter, r'^\s') or match_regex(parameter, r'\s+$'):
      errors.append("allow_whitespace_string")
      result = False

  # Check if in list of accepted values
  if "list" in constraint:
    if not from_list(parameter, constraint["list"]):
      errors.append("list")
      result = False

  # Check regexs constraints
  if "regex" in constraint:
    if not match_regex(parameter, constraint["regex"]):
      errors.append("regex")
      result = False

  if "not_regex" in constraint:
    if not not_match_regex(parameter, constraint["not_regex"]):
      errors.append("not_regex")
      result = False

  # Check length constraints
  if "min_length" in constraint:
    if not min_length(parameter, constraint["min_length"]):
      errors.append("min_length")
      result = False

  if "max_length" in constraint:
    if not max_length(parameter, constraint["max_length"]):
      errors.append("max_length")
      result = False
  
  check = {'result': result, 'errors': errors}
  return check


constraint_type = {
    "allow_whitespace_string" : bool
  , "allow_empty_string" : bool
  , "list" : list
  # use unicode for regexs, since they will be parsed as unicode ...
  , "regex" : unicode
  , "not_regex": unicode
  , "max_length" : int
  , "min_length" : int
}

def check_constraint_type(key, value):
  return type(value) is constraint_type[key]
