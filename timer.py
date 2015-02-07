import viztask
startTime = 0;
reactionTime = 0;

def StartTime():
	global startTime
	#Wait for next frame to be drawn to screen
	d = yield viztask.waitDraw()

	#Save start time
	startTime = d.time
	
def CalculateReactionTime():
	global reactionTime
	global startTime
	#Wait for mouse reaction
	d = yield viztask.waitMouseDown(viz.MOUSEBUTTON_LEFT)

	#Calculate reaction time
	reactionTime = d.time - startTime
	
	

#####################################Example#####################################
def TestReactionTime():
    while True:
        #Wait random amount of time
        yield viztask.waitTime( vizmat.GetRandom(1.5,2.5) )


        #Wait for next frame to be drawn to screen
        d = yield viztask.waitDraw()

        #Save start time
        startTime = d.time

        #Wait for mouse reaction
        d = yield viztask.waitMouseDown(None)

        #Calculate reaction time
        reactionTime = d.time - startTime

        #Print time
        print 'Reaction time:',reactionTime

viztask.schedule( TestReactionTime() )