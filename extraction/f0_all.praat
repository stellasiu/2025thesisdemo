writeInfoLine: "Extracting pitch..."

form f0_all
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

	# Create the Pitch Object
	select Sound 'thisSound$'
	pitch = To Pitch... 0.0 75 600

	# Create the output file and write the first line.
	outputPath$ = "REPLACE HERE WITH YOUR DESIRED OUTPUT PATH" + nameFile$ + "f0.csv"
	writeFileLine: "'outputPath$'", "file,phoneme,duration,mean_f0"

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
		    selectObject: pitch
		    f0 = Get mean: thisPhonemeStartTime, thisPhonemeEndTime, "Hertz"

	    # Save to a spreadsheet
		    appendFileLine: "'outputPath$'", 
		                      ...thisSound$, ",",
		                      ...thisPhoneme$, ",",
		                      ...duration, ",",
		                      ...f0


		endif

	endfor

	

endfor



appendInfoLine: newline$, newline$, "Whoo-hoo! It didn't crash!"