#!/usr/bin/env python3

import operator
import re
import csv

def gen_report(log_file):

  # Empty dictionaries
  error = {}
  per_user = {}
  
  with open(log_file) as log:
    for line in log:
      result = re.search(r"ticky: ([A-Z]+) ([\w\' ]+)", line)
      username = re.search(r"\(([\w\.]+)\)", line).group(1)
      log_type = result.group(1)
      message = result.group(2).strip()

      if result is not None:
        if log_type == "ERROR":
          error[message] = error.get(message, 0) + 1
          per_user[username]["ERROR"] = per_user.setdefault(username, {}).get("ERROR", 0) + 1
        elif log_type == "INFO":
          per_user[username]["INFO"] = per_user.setdefault(username, {}).get("INFO", 0) + 1
  
  # The sorting part(after sorting, the dictionaries get converted to list of tuples(key, value) 
  error = sorted(error.items(), key=operator.itemgetter(1), reverse=True)
  per_user = sorted(per_user.items(), key=operator.itemgetter(0))
  
  # Converting to csv files
  with open('error_message.csv', 'w') as error_csv:
    error_csv.write("{}, {}\n".format("Error", "Count"))
    for item in error:
      error_csv.write("{}, {}\n".format(item[0], item[1]))
  with open('user_statistics.csv', 'w') as user_csv:
    user_csv.write("{}, {}, {}\n".format("Username", "INFO", "ERROR"))
    for item in per_user:
      user_csv.write("{}, {}, {}\n".format(item[0], item[1].get("INFO", 0), item[1].get("ERROR", 0)))


gen_report("syslog.log")

