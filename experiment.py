from psychopy import visual, core, event, gui
import os
class Experiment:
	'''
	This is a class representing a psychology experiment
	'''
	def __init__(self, win_size, win_fullscr, input_fields, exp_name):
		input_fields.update({'subject_num' : int})
		self.subject_data = self.user_input(input_fields)
		self.win = visual.Window(
				size = win_size,
				units = 'px',
				fullscr = win_fullscr)
		self.exp_name = exp_name

	def user_input(self, fields):
		'''
		user_input(fields) - generates a user dialog box for data input
			Inputs: [fields] is a tuple dictionary of string value names and 
			their type conversion
			Requires: All user input must be present and be properly typed
		'''
		dlg = gui.Dlg()
		for k, v in fields.items():
			dlg.addField(k)
		dlg.show()

		data = {}
		count = 0
		for k, v in fields.items():
			try:
				data[k] = v(dlg.data[count])
				count += 1
			except ValueError:
				print "ERROR: Input entered is either missing or not of \
					correct form. Check your %s" % k
				core.quit()
		return data

	def shutdown(self):
		'''
		shutdown() - Closes the current window and quits out of psychopy.
		'''
		self.win.close()
		core.quit()

	def get_keypress(self):
		'''
		get_keypress() - gets the string representation of a keypress
			Returns: string representation of a key or None if no key is
			currently pressed
		'''
		keys = event.getKeys()
		if keys:
			return keys[0]
		else:
			return None

	def data_write(self, data, dir):
		'''
		data_write(data, dir, exp_data) - writes a tab delimited txt file to 
		a unique file name based on the subject data provided
			Inputs: [data] is a 2-D array where each element in the outer list 
			is a data entry with multiple data values. [dir] is a string 
			representation of a file directory to save the data in. 
			Requires: [dir] must be a valid directory
		'''
		subject_info = ''
		for k, v in self.subject_data.items():
			subject_info += k + '_' + str(v)+'_'

		data_path = dir + subject_info + 'Data.txt'

		if not os.path.exists(data_path):
			file = open(data_path, 'w')
			for line in data:
				line_str = ''
				for element in line:
					line_str += str(element) + '\t'
				file.write(line_str + '\n')
			file.close()
		else:
			print "ERROR: Filename " + data_path + " already exists"
			self.shutdown()