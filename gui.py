from os.path import isfile
import PySimpleGUI as sg
from re import match
import scheduleGenerator


HOURS = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
MINUTES = [0,15,30,45,"--",1,2,3,4,5,6,7,8,9,10,11,12,13,14,16,17,18,19,20,21,22,23,24,25,26,27,28,29,31,32,33,34,35,36,37,38,39,40,41,42,43,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

def make_main():
	main_layout = [
		[sg.Text("Schedule Generator GUI", justification='center', font=("Helvetica", 25))],
		[sg.Frame(layout=[
			[sg.Column([
				[sg.Text("Starting Time:")],
				[sg.Text("Ending Time:")]
			]),
			sg.Column([
				[sg.Combo(HOURS, size=(3, 1), readonly=True, default_value=8, key='shours')],
				[sg.Combo(HOURS, size=(3, 1), readonly=True, default_value=18, key='ehours')]
			]),
			sg.Column([
				[sg.Combo(MINUTES, size=(3, 1), readonly=True, default_value=0, key='smins')],
				[sg.Combo(MINUTES, size=(3, 1), readonly=True, default_value=0, key='emins')]
			]),
			sg.Column([
				[sg.Text("Starting Day:")],
				[sg.Text("Ending Day:")]
			]),
			sg.Column([
				[sg.Combo(DAYS, size=(4, 1), readonly=True, default_value='Mon', key='sday')],
				[sg.Combo(DAYS, size=(4, 1), readonly=True, default_value='Fri', key='eday')]
			])]
		], title='Options', relief=sg.RELIEF_SUNKEN)],
		[sg.Frame(layout=[
			[
				sg.Listbox([], size=(60, 6), key='fileList'),
				sg.Column([
					[sg.Input(key='mainBrowse', visible=False, enable_events=True), sg.FileBrowse(size=(8,1), file_types=(('Text Files (.txt)', '*.txt'),))],
					[sg.Button("Create", size=(8,1), key='fileCreate')],
					[sg.Button("Remove", size=(8,1), key='fileRemove')]
				])
			]
		], title='Input Files', relief=sg.RELIEF_SUNKEN)],
		[sg.Frame(layout=[
			[sg.Text('Path', size=(55, 1), key='pdfPath'), sg.Input(key='pdfBrowse', visible=False, enable_events=True), sg.FolderBrowse(size=(8,1))],
			[
				sg.InputText('Schedule', key='pdfName'),
				sg.Text('.pdf')
			]
		], title='Output File', relief=sg.RELIEF_SUNKEN)],
		[
			sg.Button("Generate", key='gen', size=(8,1)),
			sg.Exit(size=(8,1))
		]
	]
	return sg.Window('Schedule Generator GUI', main_layout, finalize=True)

def make_schedule():
	schedule_layout = [
		[sg.Text("Schedule Creator GUI", justification='center', font=("Helvetica", 25))],
		[sg.InputText("Schedule Name", key='sname')],
		[sg.Frame(layout=[
			[
				sg.Listbox([], size=(60, 5), key='courseList'),
				sg.Column([
					[sg.Button("Create", size=(8,1), key='courseCreate')],
					[sg.Button("Remove", size=(8,1), key='courseRemove')]
				])
			]
		], title='Courses', relief=sg.RELIEF_SUNKEN)],
		[sg.Frame(layout=[
			[
				sg.Listbox([], size=(60, 5), key='timeList'),
				sg.Column([
					[sg.Button("Create", size=(8,1), key='timeCreate')],
					[sg.Button("Remove", size=(8,1), key='timeRemove')]
				])
			]
		], title='Course Times', relief=sg.RELIEF_SUNKEN)],
		[sg.Frame(layout=[
			[sg.Text('Path', size=(55, 1), key='txtPath'), sg.Input(key='pdfBrowse', visible=False, enable_events=True), sg.FolderBrowse(size=(8,1))],
			[
				sg.InputText('Schedule', key='txtName'),
				sg.Text('.txt')
			]
		], title='Output File', relief=sg.RELIEF_SUNKEN)],
		[
			sg.Button("Generate", size=(8,1), key='txtGen'),
			sg.Cancel(size=(8,1))
		]
	]
	return sg.Window('Schedule Creator GUI', schedule_layout, finalize=True)

def make_add_course():
	add_course_layout = [
		[sg.Text("New Course")],
		[
			sg.Column([
				[sg.Text("Code:")],
				[sg.Text("Name:")],
				[sg.Text("Lecturer:")]
			]),
			sg.Column([
				[sg.InputText('Code', size=(32, 1), key='courseCode', tooltip="Must be unique")],
				[sg.InputText('Name', size=(32, 1), key='courseName')],
				[sg.InputText('Lecturer', size=(32, 1), key='courseLec')]
			])
		],
		[sg.Submit(key='courseSubmit', size=(8,1)), sg.Cancel(size=(8,1))]
	]
	return sg.Window('New Course', add_course_layout, finalize=True)

def make_add_time():
	add_time_layout = [
		[sg.Text("New Time")],
		[
			sg.Column([
				[sg.Text("Code:")],
				[sg.Text("Day:")],
				[sg.Text("Start Time:")],
				[sg.Text("End Time:")],
				[sg.Text("Location:")]
			]),
			sg.Column([
				[sg.Combo([], size=(10, 1), readonly=True, key='timeCode', tooltip="If a course was addded after this window is opened\nplease reopen the window to refresh the window.")],
				[sg.Combo(DAYS, size=(4, 1), readonly=True, default_value='Mon', key='timeDay')],
				[sg.Combo(HOURS, size=(3, 1), readonly=True, default_value=8, key='timeSHours'), sg.Combo(MINUTES, size=(3, 1), readonly=True, default_value=0, key='timeSMins')],
				[sg.Combo(HOURS, size=(3, 1), readonly=True, default_value=9, key='timeEHours'), sg.Combo(MINUTES, size=(3, 1), readonly=True, default_value=0, key='timeEMins')],
				[sg.InputText('', size=(16, 1), key='timeLoc'), sg.Text("(optional)")]
			])
		],
		[sg.Text("Make sure the details above are within\nthe boundries set in the main window.", text_color='white',background_color='black')],
		[sg.Submit(key='timeSubmit', size=(8,1)), sg.Cancel(size=(8,1))]
	]
	return sg.Window('New Time', add_time_layout, finalize=True)

def main():
	sg.theme('Dark Blue 3')
	main_window = make_main()
	schedule_window = None
	add_course_window = None
	add_time_window = None

	while True:
		window, event, values = sg.read_all_windows()
		
		if event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel':
			popup = sg.popup_yes_no('Are you sure you want to close this window?')
			if popup == 'Yes':
				window.close()
				if window == main_window:
					break
				if window == schedule_window:
					if add_course_window != None:
						add_course_window.close()
					if add_time_window != None:
						add_time_window.close()

		# Main Events
		if event == 'mainBrowse':
			tempList = window['fileList'].get_list_values()
			tempFile = values['mainBrowse']
			if tempFile not in tempList:
				tempList.append(tempFile)
			window['fileList'].update(values=tempList)

		if event == 'fileCreate':
			if schedule_window != None:
				if schedule_window.was_closed():
					schedule_window = None
				else:
					sg.popup_error('This window is opened')
					continue

			schedule_window = make_schedule()

		if event == 'fileRemove':
			tempList = window['fileList'].get_list_values()
			tempFile = values['fileList']
			for current in tempFile:
				tempList.remove(current)
			window['fileList'].update(values=tempList)

		if event == 'pdfBrowse':
			window['pdfPath'].update(value=values['pdfBrowse'] + '/')

		if event == 'gen':
			# check empty feild 
			if window['pdfName'].get() == '' or window['fileList'].get_list_values() == []:
				sg.popup_error('Filename and file list cannot be empty')
				continue
			if values['smins'] == '--' or values['emins'] == '--':
				sg.popup_error("Please specify the minutes feild (don't leave it at '--')")
				continue
			if not match("^[A-Za-z0-9_-]*$" ,window['pdfName'].get()):
				sg.popup_error("Filename can only contain letters, numbers, _, and -")
				continue

			daysArg = DAYS.index(values['eday']) - DAYS.index(values['sday']) + 1
			if daysArg < 0:
				daysArg += 7
			
			outArg = values['pdfName']
			if window['pdfPath'].get() != 'Path':
				outArg = window['pdfPath'].get() + outArg
			print(outArg)
			print(window['pdfPath'].get())
			#check bad input
			if not match("^[A-Za-z0-9_-]*$", values['pdfName']):
				sg.popup_error("Filename can only contain letters, numbers, _, and -")
				continue
			#check duplicated file
			if isfile(outArg+'.pdf'):
				popup = sg.popup_yes_no('A file with this name already exists. Do you want to override it?')
				if popup == 'No':
					continue
			
			args = ['-s', str(values['shours']*100+values['smins']), '-e', str(values['ehours']*100+values['emins']), '-f', values['sday'], '-d', str(daysArg), '-o', outArg]
			tempList = window['fileList'].get_list_values()
			for current in tempList:
				args.append(current)

			try:
				scheduleGenerator.main(args)
			except SystemExit as e:
				sg.popup_error(e)

			sg.popup("Generated successfully!")

		# Schedule Events
		if event == 'courseCreate':
			if add_course_window != None:
				if add_course_window.was_closed():
					add_course_window = None
				else:
					sg.popup_error('This window is opened')
					continue

			add_course_window = make_add_course()

		if event == 'courseRemove':
			tempList = window['courseList'].get_list_values()
			tempCourse = values['courseList']
			for current in tempCourse:
				tempList.remove(current)
			window['courseList'].update(values=tempList)

		if event == 'timeCreate':
			if add_time_window != None:
				if add_time_window.was_closed():
					add_time_window = None
				else:
					sg.popup_error('This window is opened')
					continue

			add_time_window = make_add_time()
			tempList = schedule_window['courseList'].get_list_values()
			tempList = [current.partition(',')[0] for current in tempList]
			add_time_window['timeCode'].update(values=tempList, set_to_index=0)

		if event == 'timeRemove':
			tempList = window['timeList'].get_list_values()
			tempTime = values['timeList']
			for current in tempTime:
				tempList.remove(current)
			window['timeList'].update(values=tempList)

		if event == 'txtBrowse':
			window['txtPath'].update(value=values['txtBrowse'] + '/')

		if event == 'txtGen':
			#check empty inputs
			if values['sname'] == '' or values['txtName'] == '':
				sg.popup_error('Filename and Schedule name cannot be empty')
				continue
			if window['courseList'].get_list_values() == [] or window['timeList'].get_list_values() == []:
				sg.popup_error('Course list and file list cannot be empty')
				continue

			outArg = values['txtName'] + ".txt"
			if window['txtPath'].get() != 'Path':
				outArg = window['txtPath'].get() + outArg
			#check bad input
			if not match("^[A-Za-z0-9_-]*$", values['txtName']):
				sg.popup_error("Filename can only contain letters, numbers, _, and -")
				continue
			#check duplicated file
			if isfile(outArg):
				popup = sg.popup_yes_no('A file with this name already exists. Do you want to override it?')
				if popup == 'No':
					continue

			with open(outArg, 'w') as file:
				file.write("* " + values['sname'] + '\n')
				tempList = schedule_window['courseList'].get_list_values()
				file.writelines("%s\n" % current for current in tempList)
				tempList = schedule_window['timeList'].get_list_values()
				file.writelines("%s\n" % current for current in tempList)

			sg.popup("Generated successfully!")

		if event == 'courseSubmit':
			#check for empty feilds
			if values['courseCode'] == '' or values['courseName'] == '' or values['courseLec'] == '':
				sg.popup_error('Feilds cannot be empty')
				continue

			# check commas
			if ',' in values['courseCode']+values['courseName']+values['courseLec']:
				sg.popup_error('Feilds cannot contain a comma (,)')
				continue

			#check for repeating course codes
			tempList = schedule_window['courseList'].get_list_values()
			tempList = [current.partition(',')[0] for current in tempList]
			if values['courseCode'] in tempList:
				sg.popup_error('Course code must be unique')
				continue

			tempCourse = ''
			tempCourse += values['courseCode']+','
			tempCourse += values['courseName']+','
			tempCourse += values['courseLec']

			tempList = schedule_window['courseList'].get_list_values()
			tempList.append(tempCourse)
			schedule_window['courseList'].update(values=tempList)
			window.close()

		if event == 'timeSubmit':
			#check for empty feilds
			if values['timeCode'] == '':
				sg.popup_error('The code is empty, please add a new course before adding time.')
				window.close()
			if values['timeSMins'] == '--' or values['timeEMins'] == '--':
				sg.popup_error("Please specify the minutes feild (don't leave it at '--')")
				continue

			#check beginning time and end time
			if values['timeSHours']*100+values['timeSMins'] >= values['timeEHours']*100+values['timeEMins']:
				sg.popup_error("Ending time can't be earlier than starting time")
				continue
			
			tempTime = values['timeCode'] + ',' + values['timeDay'] + ',' + str(values['timeSHours']*100+values['timeSMins']) + ',' + str(values['timeEHours']*100+values['timeEMins'])
			if values['timeLoc'] != '':
				tempTime += ',' + values['timeLoc']

			tempList = schedule_window['timeList'].get_list_values()
			tempList.append(tempTime)
			schedule_window['timeList'].update(values=tempList)
			window.close()

if __name__ == '__main__':
	main()