import viz
import vizact
import vizinput
import random
import viztask

viz.go()

#####################BackGround###################
ground = viz.add('ground.osgb')

ground.collidePlane(0,1,0,0)
env = viz.add(viz.ENVIRONMENT_MAP,'sky.jpg')

dome = viz.add('skydome.dlc')
dome.texture(env)

#####################Insight#######################
viz.MainView.setPosition([0,1,0])
mainViewEuler = []
def onMouseMove(e):
	global mainViewEuler
	mainViewEuler = viz.MainView.getEuler()
	mex = mainViewEuler[0]
	mey = mainViewEuler[1]
	if mainViewEuler[0] +(e.dx*0.5) > -60 and mainViewEuler[0] +(e.dx*0.5) < 60 :
		mex = mainViewEuler[0] +(e.dx*0.2)
	if mainViewEuler[1] - (e.dy*0.5) >-30 and mainViewEuler[1] - (e.dy*0.5) < 20 :
		mey = mainViewEuler[1] - (e.dy*0.2)
	
	viz.MainView.setEuler(mex, mey, mainViewEuler[2])


viz.callback(viz.MOUSE_MOVE_EVENT, onMouseMove)
viz.mouse(viz.OFF)
#################Calibration################
calibration = viz.addText('O', viz.WORLD)
calibration.color(255,0,0)
calibration.setPosition(-.25,1,10)
calibration.setScale(.7,.7,.7)
calibrationEuler = []
calibrationEuler = calibration.getEuler()
calibration.visible(viz.OFF)

center = viz.addText('O', viz.SCREEN)
center.setPosition(.475, .5)
center.visible(viz.OFF)

text = viz.addText('빨간원에 하얀원을 맞추십시오.', viz.SCREEN)
text.setPosition(.1,.6)
text.visible(viz.OFF)
#####################Avatar#####################
avatar = viz.add('vcc_male.cfg')
avatar.setEuler(180,0,0)
avatar.clearActions()
avatar.collideSphere()
avatar.enable(viz.COLLIDE_NOTIFY)
avatar.state(1)

#####################Car########################
car = viz.add('mini.osgx')
car.texblend(0.15,'',1)
car.collideBox()

carLoc = random.randint(0,2)
car.setPosition(15,100,5)
######################ResultFile#########################
resultFile = open("result.txt","w")
result = "Reaction time\tLeft Reaction Time\tRight ReactionTime\n"
resultFile.write(result)
############################Timer#########################
time = 0
def Timer():
	global time
	time = time + 0.01

vizact.ontimer(0.01, Timer)

##########################Functions########################
level = 1
stage = 6
carPosition = 0

collideFlag = False
visualFlag = False
auditoryFlag = False


def avatar_move():
	#avatar.setVelocity([0,0,level*-1-2], viz.ABS_GLOBAL)
	avatar.addAction(vizact.move(0,0,level+1, 6))
	avatar.state(2)

	if carLoc%2 == 1:
		#car.setVelocity([level*-1-2,0,0], viz.ABS_GLOBAL)
		car.setEuler([-90,0,0], viz.ABS_GLOBAL)
		car.addAction(vizact.move(0,0,level+1,6))
	else :
		#car.setVelocity([level+2,0,0], viz.ABS_GLOBAL)
		car.setEuler([90,0,0], viz.ABS_GLOBAL)
		car.addAction(vizact.move(0,0,level+1,6))
		
def Reset():
	global carLoc
	global stage
	
	avatar.reset()
	avatar.clearActions()
	avatar.setPosition(0,0,14+stage)
	
	carLoc = random.randint(0,2)
	car.reset()
	car.clearActions()
	car.setPosition(10,100,5)

def GetCarPosition():
	global carPosition
	global visualFlag
	global auditoryFlag
	global stage
	
	carPosition = car.getPosition();

	if carPosition[0] != 10 :
		if carLoc%2 == 1 :
			if carPosition[0] < stage/3 :
				auditoryFlag = True
			elif carPosition[0] < stage*2/3 :
				visualFlag = True
		else :
			if -1*carPosition[0] < stage/3 :
				auditoryFlag = True
			elif -1*carPosition[0] < stage*2/3 :
				visualFlag = True

def calibrationCheck() :
	global mainViewEuler
	global calibrationEuler
	
	global calibration
	global center
	global text
	
	print mainViewEuler
	print calibrationEuler
	
	while(True) :
		if mainViewEuler[0] > calibrationEuler[0]-1 and mainViewEuler[0] < calibrationEuler[0]+1 and mainViewEuler[1] > calibrationEuler[1]-1 and mainViewEuler[1] < calibrationEuler[1]+1 and mainViewEuler[2] > calibrationEuler[2]-1 and mainViewEuler[2] < calibrationEuler[2]+1:
			calibration.visible(viz.OFF)
			center.visible(viz.OFF)
			text.visible(viz.OFF)
			break;
			
	return True

def correctReact():
	global level
	global stage
	if level < 4 :
		level = level + 1
	elif stage > 1 :
		stage = stage - 1
		
def incorrectReact():
	global level
	global stage
	global taskFail
	if stage < 6 :
		stage = stage + 1
	elif level > 1 :
		level = level - 1
	taskFail += 1
###############################Training##############################
taskFail = 0
def TestReactionTime():
	global time
	global level
	global stage
	
	global visualFlag
	global auditoryFlag
	
	global center
	global calibration
	global text
	
	global taskFail
	testCount = 0
	leftReactionTime = 0
	rightReactionTime = 0
	
	visualCue = 0
	auditoryCue = 0
	
	waitMouseLEFT = viztask.waitMouseDown(viz.MOUSEBUTTON_LEFT)
	waitMouseRIGHT = viztask.waitMouseDown(viz.MOUSEBUTTON_RIGHT)
	waitCollide = viztask.waitEvent(viz.COLLIDE_BEGIN_EVENT)

	Reset()
	#Start test from space down
	yield viztask.waitKeyDown(' ')
	
	while testCount < 10:
		yield viztask.waitTime(vizmat.GetRandom(2,4))
		
		avatar_move()
		
		d = yield viztask.waitDraw()
		
		#Move Car Position
		if carLoc%2 == 1 :
			car.setPosition(6+stage,0,10)
		else :
			car.setPosition(-6-stage,0,10)
		
		#Save start time
		startTime = time
		
		#Wait for mouse reaction or collide event
		d = yield viztask.waitAny([waitMouseLEFT, waitMouseRIGHT, waitCollide])
		reactionTime = time - startTime
		if d.condition is waitMouseLEFT:
			if carLoc%2 == 1:
				incorrectReact()
				leftReactionTime = 0
				rightReactionTime = reactionTime
			else :
				correctReact()
				leftReactionTime = reactionTime
				rightReactionTime = 0
		elif d.condition is waitMouseRIGHT:
			if carLoc%2 == 1:
				correctReact()
				leftReactionTime = 0
				rightReactionTime = reactionTime
			else :
				incorrectReact()
				leftReactionTime = reactionTime
				rightReactionTime = 0
		elif d.condition is waitCollide:
			if stage < 6 :
				stage = stage + 1
			elif level > 1 :
				level = level - 1
			taskFail += 1
		
		
		#Calculate reaction time
		
		if visualFlag :
			visualCue += 1
			visualFlag = False
		if auditoryFlag :
			auditoryCue += 1
			auditoryFlag = False
			
		
		print 'Task ',testCount+1,' Traing'
		print 'Reaction time : ',reactionTime
		print 'Left Reaction Time : ',leftReactionTime
		print 'Right Reaction Time : ',rightReactionTime
		
		result = "%f\t\t%f\t\t%f\n" % (reactionTime, leftReactionTime, rightReactionTime)
		resultFile.writelines(result)
		
		
		testCount += 1
		Reset()
		
		center.visible(viz.ON)
		calibration.visible(viz.ON)
		text.visible(viz.ON)
		yield viztask.waitDirector(calibrationCheck)
		
	result = "\nVisualCue : %d\tAuditoryCue : %d\tFailCount : %d\n" % (visualCue, auditoryCue, taskFail)
	resultFile.write(result)
	print 'vizsualCue : ',visualCue
	print 'auditorycue : ',auditoryCue
	print 'FailCount : ',taskFail

viztask.schedule(TestReactionTime())
##############################################################################
vizact.ontimer(0.01, GetCarPosition)	

#don't move out mouse pointer
viz.mouse.setTrap()
#unvisible mouse pointer
viz.mouse.setVisible(viz.OFF)


viz.phys.enable()