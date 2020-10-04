# A Timetable Generator
If you are bored of adding your time tiles manually, having a bad visibility of courses, or having an issue with displaying conflicting courses, this is the tool for you.

It generates a PDF file with colorful tiles to make everything easy to see. `Schedule.pdf` is a demonstration generated from `s.txt` which has the detailed instructions to set your schedule.

# How to use
The script is written with Python 3 and requires matplotlib library installed. 
After setting your input file(s) as explained in  `s.txt`, you can run the script by typing

    python3 scheduleGenerator.py file1.txt file2.txt file3.txt
where `file1.txt file2.txt file3.txt` are the list of the files you have.
If no files were given as an argument the script will default to process `s.txt`.
The script will end up generating `Schedule.pdf`containing the schedule(s) indicated by the files.

# Special Thanks
Special thanks to Jacob from StudyGizmo on his hints about overlap resolution. 
