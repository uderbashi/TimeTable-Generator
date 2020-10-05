import sys
import matplotlib.pyplot as plt
import matplotlib.transforms as trns
from matplotlib.backends.backend_pdf import PdfPages

# constants that will be used to create the schedule.
DAYS_LIST = ["Mon", "Tue", "Wed", "Thu", "Fri"]
COLOURS = ["limegreen", "royalblue", "mediumorchid", "gold", "pink", "chocolate", "aqua", "lightcoral", "slateblue", "springgreen", "deepskyblue", "plum", "orange", "firebrick", "olive",  "darkcyan"]
START_TIME = 830
END_TIME = 1730

# Classes to be used in the program
class Course:
	def __init__(self, code, name, instructor, colour):
		self.code = code
		self.name = name
		self.instructor = instructor
		self.colour = colour
		self.times = []

class Scheduled:
	def __init__(self, course, day, start, end, place):
		self.course = course
		self.day = day
		self.start = start
		self.end = end
		self.place = place

		self.overlapCols = 1	#how many total columns are there
		self.overlapCol = 0		#in which column is the current one standing
		self.overlapSpan = 1	#how many columns does the entry span horizontally

	def comparator(self):
		return self.day * 10000 + self.start

	def __repr__(self):
		return "The course {c} is occuring on {d} from {b} to {e}".format(c=self.course.code, d=DAYS_LIST[self.day], b=self.start, e=self.end)

def parse(filename):
	courses = []
	lineCount = 0
	newid = 0
	label = ""
	for line in open(filename, "r"):
		lineCount += 1

		line = str.lstrip(line)
		if len(line) == 0 or line[0] == "#":
			continue

		if line[0] == "*":
			label = line[1:]
			label = label.strip()
			continue

		data = line.split(",")
		data = map(str.strip, data)
		data = list(data)
		
		for current in courses:
			if current.code == data[0]:

				if data[1] not in DAYS_LIST:
					msg = "Error on line {lc}: \"{d}\" is not a valid day. Make sure you use a correct 3 letter day format ex \"Mon\" with only the first letter capitalised.".format(lc= lineCount, d = data[1])
					exit(msg)

				if int(data[2]) > END_TIME or int(data[2]) < START_TIME:
					msg = "Error on line {lc}: \"{d}\" is not a valid statring time. Make sure the time is formated with 24hour style HHMM ex \"0930\" and is within the courses time.".format(lc= lineCount, d = data[2])
					exit(msg)

				if int(data[3]) > END_TIME or int(data[3]) < START_TIME:
					msg = "Error on line {lc}: \"{d}\" is not a valid ending time. Make sure the time is formated with 24hour style HHMM ex \"0930\" and is within the courses time.".format(lc= lineCount, d = data[3])
					exit(msg)

				if int(data[3]) <= int(data[2]):
					msg = "Error on line {lc}: \"{d},{dd}\" the ending time should be later than the starting time.".format(lc= lineCount, d = data[2], dd = data[3])
					exit(msg)

				if int(data[2]) % 100 >= 60:
					msg = "Error on line {lc}: \"{d}\" is not a valid time due to the minutes being larger than 59.".format(lc= lineCount, d = data[2])
					exit(msg)

				if int(data[3]) % 100 >= 60:
					msg = "Error on line {lc}: \"{d}\" is not a valid time due to the minutes being larger than 59.".format(lc= lineCount, d = data[3])
					exit(msg)

				current.times.append(Scheduled(current, DAYS_LIST.index(data[1]),int(data[2]),int(data[3]), None if len(data) == 4 else data[4]))
				break
		else:
			courses.append(Course(data[0], data[1], data[2], COLOURS[newid]))
			newid += 1

	for current in courses:
		current.times.sort(key=Scheduled.comparator)

	return courses, label

def fillDays(courses):
	days = [[] for _ in range(len(DAYS_LIST))]

	for current in courses:
		for session in current.times:
			days[session.day].append(session)

	for current in days:
		current.sort(key=Scheduled.comparator)

	return days

def detectOverlap(days):
	overlapping = []

	for day in days:
		overlapping.clear()
		overlapLast = 0
		for current in day:
			if current.start >= overlapLast:
				if len(overlapping) > 1:
					resolveOverlap(overlapping)
				overlapping.clear()
				overlapLast = 0
			overlapping.append(current)
			if current.end > overlapLast:
				overlapLast = current.end
		if len(overlapping) > 1:
			resolveOverlap(overlapping)
			
def resolveOverlap(overlapping):
	colCount = len(overlapping)
	columns = [[] for _ in range(colCount)]
	for i in range(colCount):
		columns[i].append(overlapping[i])

	shiftFlag = True # To enter the loop
	while shiftFlag is True:
		shiftFlag = False
		i = 0
		for current in columns[:colCount]:
			i += 1
			for check in columns[i:]:
				if current[-1].end <= check[0].start:
					colCount -= 1
					current.extend(check)
					columns.remove(check)
					shiftFlag = True

	i = -1
	for col in columns:
		i += 1
		for current in col:
			current.overlapCols = colCount
			current.overlapCol = i

def drawTimetable(days, title):
	fig = plt.figure(figsize=(11.7,8.3), dpi=300)
	for day in days:
		for current in day:
			x1 = current.day + (current.overlapCol / current.overlapCols)
			x2 = x1 + (current.overlapSpan / current.overlapCols)
			ystart = convertTime(current.start)
			yend = convertTime(current.end)
			plt.fill_between([x1, x2], [ystart, ystart], [yend, yend], color=current.course.colour, edgecolor="k", linewidth=1)
			plt.text(x1+0.02, ystart+5, "{0}:{1:02d}".format(current.start//100, current.start%100), va="top", fontsize=7)
			plt.text(x1+0.02, yend-5, "{0}:{1:02d}".format(current.end//100, current.end%100), va="bottom", fontsize=7)
			plt.text(x1+(x2-x1)*0.5, (ystart+yend)*0.5, current.course.code, ha="center", va="center", fontsize=9)

	plotystart = modTime(START_TIME, -30)
	plotyend = modTime(END_TIME, 30)

	ax = fig.gca()
	ax.yaxis.grid()
	ax.set_ylim(plotyend, plotystart)
	ax.set_yticks(range(plotystart, plotyend, 100))
	ax.set_yticklabels(genYLabels())
	ax.xaxis.grid()
	ax.set_xlim(0,len(days))
	ax.set_xticks(range(1, len(days)+1))
	ax.set_xticklabels(DAYS_LIST)
	for label in ax.xaxis.get_majorticklabels():
		label.set_transform(label.get_transform() + trns.ScaledTranslation(-.9, 0, fig.dpi_scale_trans))

	ax2 = ax.twinx().twiny()
	ax2.set_ylim(ax.get_ylim())
	ax2.set_yticks(ax.get_yticks())
	ax2.set_yticklabels(ax.get_yticklabels())
	ax2.set_xlim(ax.get_xlim())
	ax2.set_xticks(ax.get_xticks())
	ax2.set_xticklabels(ax.get_xticklabels())
	for label in ax2.xaxis.get_majorticklabels():
		label.set_transform(label.get_transform() + trns.ScaledTranslation(-.9, 0, fig.dpi_scale_trans))

	ax.set_title(title, fontweight ="bold")

	return fig

def genYLabels():
	labels = []

	labelQty = (convertTime(END_TIME) - convertTime(START_TIME)) // 100 + 1

	start = modTime(START_TIME, -30)

	for x in range(labelQty):
		labels.append("{h}:{m:02d}".format(h=int(start/100), m=start%100))
		start += 100

	return labels

def modTime(time, mod):
	hours = time // 100
	minutes = time % 100

	hmod = mod // 60
	mmod = mod % 60

	hours += hmod
	minutes += mmod

	hours = abs(hours % 24)

	if minutes < 0 :
		hours -= 1
		minutes = minutes + 60
	elif minutes >= 60:
		hours += 1
		minutes = minutes % 60

	return hours * 100 + int((minutes / 60) * 100)

def convertTime(time):
	hours = time // 100
	minutes = time % 100
	
	return hours * 100 + int((minutes / 60) * 100)

def drawTable(courses, title):
	lines = 0
	for current in courses:
		lines += len(current.times)

	cols = ["Course", "Instructor", "Time", "Place"]
	rows = ["" for i in range(lines)]
	vals = [["" for i in range(4)] for j in range(lines)]
	ccolours = [["" for i in range(4)] for j in range(lines)]
	rcolours = ["" for i in range(lines)]

	i = 0
	for current in courses:
		rows[i] = current.code
		vals[i][0] = current.name
		vals[i][1] = current.instructor
		for time in current.times:
			rcolours[i] = current.colour
			ccolours[i] = [current.colour for i in range(4)]
			vals[i][2] = "{d} {sh:02d}:{sm:02d}-{eh:02d}:{em:02d}".format(d=DAYS_LIST[time.day], sh=time.start//100, sm=time.start%100, eh=time.end//100, em=time.end%100)
			vals[i][3] = "" if time.place == None else time.place
			i += 1

	fig = plt.figure(figsize=(11.7,8.3), dpi=300)
	ax = fig.subplots()
	ax.set_axis_off()
	table = ax.table(
		cellText = vals,
		rowLabels = rows,
		colLabels = cols,
		cellColours = ccolours,
		rowColours = rcolours,
		cellLoc ="center",
		colLoc ="center",
		rowLoc ="center",
		loc ="upper left")

	ax.set_title(title, fontweight ="bold")
	return fig

def main():
	if len(sys.argv) == 1 :
		args = ["s.txt"]
		print("Since no input file names were given as arguments, the program is defaulting to open \"s.txt\"")
		print("If you have other file names please provide them as arguments to the program")
		print()
	else:
		args = sys.argv[1:]
	pp = PdfPages("Schedule.pdf")
	for file in args:
		courses, title = parse(file)
		days = fillDays(courses)
		detectOverlap(days)
		ttbl = drawTimetable(days, title)
		tbl = drawTable(courses, title)
		pp.savefig(ttbl)
		pp.savefig(tbl)
	pp.close()

if __name__ == "__main__":
	main()
