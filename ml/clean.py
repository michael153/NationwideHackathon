import csv
import numpy as np


def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

with open('driving_dataset/maneuver_data/samples_clean_acc.csv', 'w') as w:
	writer = csv.DictWriter(w, fieldnames = ["timestamp", "x_axis", "y_axis", "z_axis", "provider", "run_id", "turn_id", "severity", "aggressive", "direction"])
	writer.writeheader()
	writer = csv.writer(w, delimiter=',')
	with open('driving_dataset/maneuver_data/samples_clean.csv') as file:
		reader = csv.reader(file, delimiter=',')
		for l in reader:
			if l[4] == "acc":
				print("Good: " + str(l))
				writer.writerow(l)
