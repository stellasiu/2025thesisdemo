writeInfoLine: "Extracting formants..."

form formants_single
	sentence path REPLACE HERE WITH YOUR FULL DATASET PATH
endform

myList = Create Strings as file list: "myList", path$ + "/" + "*.TextGrid"
nFiles = Get number of strings

# Define the list of vowels you're interested in
vowelList$ = "iy ih eh ey ae aa aw ay ah ao oy ow uh uw ux er ax ix axr ax-h"

for file to nFiles
	selectObject: myList
	nameFile$ = Get string: file
	thisTextGrid = Read from file: path$ + "/" + nameFile$
	thisTextGrid$ = selected$("TextGrid")
	thisSound = Read from file: path$ + "/"+ thisTextGrid$ + ".WAV"
	thisSound$ = selected$("Sound")
# Extract the names of the Praat objects
#thisSound$ = selected$("Sound")
#thisTextGrid$ = selected$("TextGrid")


	# Extract the number of intervals in the phoneme tier
	select TextGrid 'thisTextGrid$'
	numberOfPhonemes = Get number of intervals: 1  
	appendInfoLine: "There are ", numberOfPhonemes, " intervals."

	# Create the Formant Object
	select Sound 'thisSound$'
	To Formant (burg)... 0 5 5000 0.025 50

	# Create the output file and write the first line.
	outputPath$ = "REPLACE HERE WITH YOUR DESIRED OUTPUT PATH" + nameFile$ + "formants.csv"
	writeFileLine: "'outputPath$'", "file,time,phoneme,duration,F1,F2,F3,F4"

# Loop through each interval on the phoneme tier.
	for thisInterval from 1 to numberOfPhonemes
    #appendInfoLine: thisInterval

    # Get the label of the interval
	    select TextGrid 'thisTextGrid$'
	    thisPhoneme$ = Get label of interval: 1, thisInterval
    #appendInfoLine: thisPhoneme$

    # Check if the phoneme is in vowelList$
	    if index(" " + vowelList$ + " ", " " + thisPhoneme$ + " ") > 0

    # Find the midpoint.
	    thisPhonemeStartTime = Get start point: 1, thisInterval
	    thisPhonemeEndTime   = Get end point:   1, thisInterval
	    	duration = thisPhonemeEndTime - thisPhonemeStartTime
	    midpoint = thisPhonemeStartTime + duration/2
      
	    # Extract formant measurements
		    select Formant 'thisSound$'
		    f1 = Get value at time... 1 midpoint Hertz Linear
		    f2 = Get value at time... 2 midpoint Hertz Linear
		    f3 = Get value at time... 3 midpoint Hertz Linear
		    f4 = Get value at time... 4 midpoint Hertz Linear

	    # Save to a spreadsheet
		    appendFileLine: "'outputPath$'", 
		                      ...thisSound$, ",",
		                      ...midpoint, ",",
		                      ...thisPhoneme$, ",",
		                      ...duration, ",",
		                      ...f1, ",", 
		                      ...f2, ",", 
		                      ...f3, ",",
		                      ...f4 

		endif

	endfor

	

endfor



appendInfoLine: newline$, newline$, "Whoo-hoo! It didn't crash!"
