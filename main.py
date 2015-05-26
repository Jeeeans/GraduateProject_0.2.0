#-*- coding: utf-8 -*-
import viz
import vizact
import vizinput
import vizinfo
import vizshape
import random
import viztask
import vizdlg
import math
import time

viz.go()

level = 1
stage = 6

#####################Input Information Form#####################
class InputForm(vizdlg.Dialog):
	
	def __init__(self,**kw):

		#Initialize base class
		vizdlg.Dialog.__init__(self,**kw)
		
		group = vizdlg.Panel()
		
		row = vizdlg.Panel(layout=vizdlg.LAYOUT_HORZ_BOTTOM, border = False, background = False, margin = 0)
		row.addItem(viz.addText('name'))
		self.name = row.addItem(viz.addTextbox())
		group.addItem(row)
		
		row = vizdlg.Panel(layout=vizdlg.LAYOUT_HORZ_BOTTOM, border = False, background = False, margin = 0)
		row.addItem(viz.addText('number'))
		self.number = row.addItem(viz.addTextbox())
		group.addItem(row)
		
		row = vizdlg.Panel(layout=vizdlg.LAYOUT_HORZ_BOTTOM, border = False, background = False, margin = 0)
		
		row.addItem(viz.addText('level'))
		self.level = row.addItem(viz.addTextbox())
		row.addItem(viz.addText('stage'))
		self.stage = row.addItem(viz.addTextbox())
		
		
		#levelDlg = vizdlg.TickerDialog(label='level',units='',range=(1,4,1))
		#levelDlg.cancel.visible(0)
		#levelDlg.accept.visible(0)
		
		#self.level = row.addItem(levelDlg)
		#self.stage = row.addItem(vizdlg.TickerDialog(label='stage',units='',range=(1,6,1)))
		
		
		group.addItem(row)
		
		self.content.addItem(group)
		self.cancel.visible(0)
		self.accept.message('submit')


################################Task Information############################
#info = vizinfo.InfoPanel("Task Information.", align=viz.ALIGN_CENTER_CENTER, icon=False)

def showTaskInfo():
	global infoText
	
	infoText = viz.addTexQuad(viz.SCREEN)
	infoText.setScale([12,10,0])
	infoText.setPosition([.5,.5,0])
	image = viz.addTexture('art/infoText.jpg')
	image.wrap( viz.WRAP_S, viz.CLAMP_TO_EDGE )
	image.wrap( viz.WRAP_T, viz.CLAMP_TO_EDGE )
	infoText.texture( image, '', 1 )
		

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
	
		viz.MainView.setEuler(mex, mey, mainViewEuler[2], viz.REL_PARENT)


viz.callback(viz.MOUSE_MOVE_EVENT, onMouseMove)
viz.mouse(viz.OFF)

#########################Avatar Move##########################
def move(location):
	global avatar
	global view_link
	global stage
	
	
	#view_link.remove()
	[x,y,z] = avatar.getPosition()
	[xr,yr,zr] = avatar.getEuler()
	
	if location == 'forward':
		avatar.setPosition([0, 0, 0.05], viz.ABS_LOCAL)
		viz.MainView.setPosition([0, 0, 0.05], viz.REL_GLOBAL)
		avatar.state(2)
	elif location == 'back':
		avatar.setPosition([0, 0, -0.05], viz.ABS_LOCAL)
		viz.MainView.setPosition([0, 0, -0.05], viz.REL_GLOBAL)
	elif location == 'left_turn':
		avatar.setEuler([-2, 0, 0], viz.REL_GLOBAL)
	elif location == 'right_turn': 
		avatar.setEuler([2, 0, 0], viz.REL_GLOBAL)
	elif location == 'left':
		avatar.setPosition([-0.05,0,0],viz.ABS_LOCAL)
	elif location == 'right':
		avatar.setPosition([0.05,0,0], viz.ABS_LOCAL)
	
	#print [xr,yr,zr]
	#[xrm,yr,zr] = avatar.getEuler()
	#view_link = viz.link(avatar, viz.MainView, offset=(-1*stage*math.sin(xrm-xr),2,stage* math.cos(xrm-xr)))
	
def stop():
	global avatar
	avatar.clearActions()

vizact.whilekeydown('w', move, 'forward')
vizact.whilekeydown('s', move, 'back')
vizact.whilekeydown('a', move, 'left_turn')
vizact.whilekeydown('d', move, 'right_turn')
vizact.whilekeydown('q', move, 'left')
vizact.whilekeydown('e', move, 'right')
vizact.onkeyup('w', stop)

#####################BackGround###################
ground = viz.add('ground.osgb')
ground.collidePlane(0,1,0,0)
ground.setScale(5,1,5)

concrete = viz.addTexture('art/asphalt.jpg')
concrete.wrap(viz.WRAP_S, viz.REPEAT)
concrete.wrap(viz.WRAP_T, viz.REPEAT)

ground.texture(concrete,'',0)

crossWalk = viz.addTexture('art/crossWalk.png')
crossWalk.wrap(viz.WRAP_S, viz.REPEAT)
crossWalk.wrap(viz.WRAP_T, viz.REPEAT)

crossWalkBase = viz.addTexQuad()
crossWalkBase.setEuler([0, 90, 90])
crossWalkBase.setPosition([0,0.1,0])
crossWalkBase.texture(crossWalk, '', 1)
crossWalkBase.setScale([155, 7, 0])

matrix = vizmat.Transform()
matrix.setScale([20,1,0])

crossWalkBase.texmat(matrix, '', 1)
crossWalkBase.texblend(1,'',1)

env = viz.add(viz.ENVIRONMENT_MAP,'sky.jpg')

dome = viz.add('skydome.dlc')
dome.texture(env)

#####################Avatar#####################
avatar = viz.add('vcc_male.cfg')
avatar.setEuler(0,0,0)
avatar.clearActions()
head_bone = avatar.getBone('Bip01 Head')

viz.MainView.setPosition([0,2,-80 + 1-stage])
global view_link


avatar.collideBox()
avatar.enable(viz.COLLIDE_NOTIFY)
avatar.state(1)

#####################Car########################
car = viz.add('mini.osgx')
car.texblend(0.15,'',1)
car.collideBox()

carLoc = random.randint(0,2)
car.setPosition(20,0,-100)

##auditory que(hoot sound)##
left = viz.add('white_ball.wrl')
left.visible(viz.OFF)
leftSound = left.playsound('art/hoot.wav')
leftSound.stop()
lsl = viz.link(viz.MainView, left)
lsl.preTrans([-13,0,0])

right = viz.add('white_ball.wrl')
right.visible(viz.OFF)
rightSound = right.playsound('art/hoot.wav')
rightSound.stop()
rsl = viz.link(viz.MainView, right)
rsl.preTrans([13,0,0])

##viusal que(head light)##
LeftHeadLight = vizshape.addCone()
LeftHeadLight.setParent(car)
LeftHeadLight.setScale(0.7,6,0.7)
LeftHeadLight.color(viz.YELLOW)
LeftHeadLight.setPosition([-0.6,0.65,2.5], viz.REL_PARENT)
LeftHeadLight.setEuler([-90,0,90], viz.REL_PARENT)
LeftHeadLight.drawOrder(1, '', viz.BIN_TRANSPARENT)
LeftHeadLight.visible(viz.OFF)

RightHeadLight = vizshape.addCone()
RightHeadLight.setParent(car)
RightHeadLight.setScale(0.7,6,0.7)
RightHeadLight.color(viz.YELLOW)
RightHeadLight.setPosition([0.6,0.65,2.5], viz.REL_PARENT)
RightHeadLight.setEuler([-90,0,90], viz.REL_PARENT)
RightHeadLight.drawOrder(1,'',viz.BIN_TRANSPARENT)
RightHeadLight.visible(viz.OFF)

#########################Building##########################
building = viz.add('art/building.osgb')
building.setPosition(-400,-20,1000)
building.setEuler(0,0,0)
building.setScale(.1,.1,.1)

############################Timer#########################
#time = 0
def Timer():
	global time
	time = time + 0.01

#vizact.ontimer(0.01, Timer)

#################Calibration################
calibration = viz.addText('O', viz.WORLD)
calibration.setCenter([0,0,0])
calibration.color(255,0,0)


calibration.setPosition([0,2,-70 + 1-stage])
calibration.setScale(.7,.7,.7)

calibrationEuler = []
calibrationEuler = calibration.getEuler()
calibration.visible(viz.OFF)

center = viz.addText('O', viz.SCREEN)
center.setPosition(.5, .5)
center.visible(viz.OFF)


text = viz.addTexQuad(viz.SCREEN)
text.setPosition([.5,.7, 0])
text.setScale([6,1,0])
image = viz.addTexture('art/calText.png')
image.wrap( viz.WRAP_S, viz.CLAMP_TO_EDGE )
image.wrap( viz.WRAP_T, viz.CLAMP_TO_EDGE )
text.texture( image, '', 1 )
text.visible(viz.OFF)


##########################Functions########################
carPosition = 0

collideFlag = False
visualFlag = False
auditoryFlag = False

def objectVisible( status ):
	global avatar
	global car
	global building
	global ground
	global dome
	
	if status is "on":
		avatar.visible(viz.ON)
		car.visible(viz.ON)
		building.visible(viz.ON)
		ground.visible(viz.ON)
		crossWalkBase.visible(viz.ON)
		dome.visible(viz.ON)
	elif status is "off":
		avatar.visible(viz.OFF)
		car.visible(viz.OFF)
		building.visible(viz.OFF)
		ground.visible(viz.OFF)
		crossWalkBase.visible(viz.OFF)
		dome.visible(viz.OFF)
		

def avatar_move():
	global avatar
	global car
	global level
	global moveTimer

	
	if carLoc%2 == 1:
		car.setEuler([-90,0,0], viz.ABS_GLOBAL)
	else :
		car.setEuler([90,0,0], viz.ABS_GLOBAL)

		
	def moveF():
		avatar.setPosition([0, 0, 0.02+level*0.01], viz.ABS_LOCAL)
		viz.MainView.setPosition([0, 0, 0.02+level*0.01], viz.REL_GLOBAL)
		avatar.state(2)
		if carLoc%2 == 1:
			car.setPosition([0, 0, 0.01*level+0.02], viz.ABS_LOCAL)
		else :
			car.setPosition([0, 0, 0.01*level+0.02], viz.ABS_LOCAL)
		
	moveTimer = vizact.ontimer(0.01, moveF)
	
		
def AvatarReset():
	global avatar
	
	avatar.reset()
	avatar.clearActions()
	avatar.setPosition(0,0,-80)
	viz.MainView.setPosition([0,2,-80 -stage])

def CarReset():
	global carLoc
	global car
	
	carLoc = random.randint(0,2)
	car.reset()
	car.clearActions()
	car.setPosition(15,0,-100)



def GetCarPosition():
	global car
	global avatar
	global visualFlag
	global auditoryFlag
	global stage
	
	carPosition = car.getPosition();
	[x,y,z] = viz.MainView.getPosition()
	if carPosition[0] != 10 :
		if carLoc%2 == 1 :
			if carPosition[0] < 6 and carPosition[0] > 0:
				auditoryFlag = True
				right.setPosition([13,0,z])
				rightSound.play()
			elif carPosition[0] < 10 and carPosition[0] > 0:
				visualFlag = True
				LeftHeadLight.visible(viz.ON)
				RightHeadLight.visible(viz.ON)
		else :
			if carPosition[0] > -6 and carPosition[0] < 0 :
				auditoryFlag = True
				left.setPosition([-13,0,z])
				leftSound.play()
			elif carPosition[0] > -10 and carPosition[0] < 0:
				visualFlag = True
				LeftHeadLight.visible(viz.ON)
				RightHeadLight.visible(viz.ON)
				
vizact.ontimer(0.01, GetCarPosition)	

def startCalibration() :
	global center
	global calibration
	global text
	global image

	image = viz.addTexture('art/firstCalText.jpg')
	text.texture( image, '', 1 )

	calibration.visible(viz.ON)
	text.visible(viz.ON)
	
	
	
def calibrationCheck() :
	global mainViewEuler
	global calibrationEuler
	
	global calibration
	global center
	global text
	
	center.visible(viz.ON)
	calibration.visible(viz.ON)
	text.visible(viz.ON)
	
	while(True) :
		if mainViewEuler[0] > calibrationEuler[0]-1 and mainViewEuler[0] < calibrationEuler[0]+1 :
			if mainViewEuler[1] > calibrationEuler[1]-1 and mainViewEuler[1] < calibrationEuler[1]+1 :
				if mainViewEuler[2] > calibrationEuler[2]-1 and mainViewEuler[2] < calibrationEuler[2]+1 :
					calibration.visible(viz.OFF)
					center.visible(viz.OFF)
					text.visible(viz.OFF)
					break;

	return True

def correctReact():
	global level
	global stage
	if level < 5 :
		level = level + 1
	elif stage < 6 :
		stage = stage - 1
		level = 1
		
def incorrectReact():
	global level
	global stage
	global taskFail
	if stage < 6 :
		stage = stage + 1
		level = 1
	elif level > 1 :
		level = level - 1
	taskFail += 1
	taskFlag = True
	

###############################Training##############################
taskFail = 0
taskFlag = False
def TestReactionTime():
	global level
	global stage
	
	global visualFlag
	global auditoryFlag
	global taskFlag
	
	global taskFail
	global moveTimer
	
	testCount = 0
	leftReactionTime = 0
	leftCount = 0
	totalLeft = 0
	rightReactionTime = 0
	rightCount = 0
	totalRight = 0
	
	visualCue = 0
	auditoryCue = 0
	
	waitMouseLEFT = viztask.waitMouseDown(viz.MOUSEBUTTON_LEFT)
	waitMouseRIGHT = viztask.waitMouseDown(viz.MOUSEBUTTON_RIGHT)
	waitCollide = viztask.waitEvent(viz.COLLIDE_BEGIN_EVENT)
	waitTime = viztask.waitTime(4)
	#######User Input########
	objectVisible("off")
	viz.mouse.setVisible(viz.ON)
	
	
	
	form = InputForm(title="User Information")

	viz.link(viz.MainWindow.CenterCenter, form)
	
	yield form.show()
	
	if form.accepted:
		name = form.name.get()
		number = form.number.get()
		level = int(form.level.get())
		stage = 7-int(form.stage.get())
		
		######################ResultFile#########################
		fileName = 'result_'+name+'('+number+').txt'
		resultFile = open(fileName, "w")

		result = "%s\t%s\t%s\t%s\t%s\t%s\n" % ("reation time", "left reation time", "right reation time", "visual que", "auditory que", "task Fail")
		resultFile.write(result)
		
	form.remove()
	
	
	
	viz.mouse.setVisible(viz.OFF)
	#info를 보여준다.
	global infoText
	yield viztask.waitDirector(showTaskInfo)
	
	yield viztask.waitKeyDown(' ')
	
	infoText.visible(viz.OFF)
	
	
	yield viztask.waitDirector(startCalibration)
	yield viztask.waitKeyDown(' ')
	
	viz.MainView.setEuler(0,0,0)
	calibration.visible(viz.OFF)
	text.visible(viz.OFF)
	
	image = viz.addTexture('art/calText.png')
	text.texture( image, '', 1 )
	
	CarReset()
	AvatarReset()
	
	avatar_move()
	moveTimer.remove()
	
	objectVisible("on")
	
	#Start test from space down
	yield viztask.waitKeyDown(' ')
	vizact.ontimer(0.01, GetCarPosition)
	#test
	while testCount < 30:
		while level < 5:
			yield viztask.waitTime(vizmat.GetRandom(1,4))
			moveTimer.remove()
			avatar_move()
			
			d = yield viztask.waitDraw()
			
			#Move Car Position
			global avatar
			[x,y,z] = avatar.getPosition()
			if carLoc%2 == 1 :
				car.setPosition(13,0,z+10)
			else :
				car.setPosition(-13,0,z+10)
				
			
			#Save start time
			startTime = time.time()
			
			#Wait for mouse reaction or collide event
			d = yield viztask.waitAny([waitMouseLEFT, waitMouseRIGHT, waitCollide])

			reactionTime = time.time() - startTime
			leftReactionTime=0
			rightReactionTime=0
			
			if carLoc%2 == 1:
				rightSound.stop()
			else :
				leftSound.stop()
			LeftHeadLight.visible(viz.OFF)
			RightHeadLight.visible(viz.OFF)
			
			
			if d.condition is waitMouseLEFT:
				if carLoc%2 == 1:
					incorrectReact()
					rightReactionTime = reactionTime
				else :
					correctReact()
					leftReactionTime = reactionTime
					leftCount += 1
					totalLeft += reactionTime
			elif d.condition is waitMouseRIGHT:
				if carLoc%2 == 1:
					correctReact()
					rightReactionTime = reactionTime
					rightCount += 1
					totalRight += reactionTime
				else :
					incorrectReact()
					leftReactionTime = reactionTime
			elif d.condition is waitCollide:
				if stage < 6 :
					stage = stage + 1
					level = 1
				elif level > 1 :
					level = level - 1
				taskFail += 1
				taskFlag = True
			
			
			if visualFlag :
				visualCue += 1
			if auditoryFlag :
				auditoryCue += 1
				
			
			result = "%.3f\t%.3f\t%.3f\t%s\t%s\t%s\n" % (reactionTime, leftReactionTime, rightReactionTime, visualFlag, auditoryFlag, taskFlag)
			resultFile.writelines(result)
			visualFlag = False
			auditoryFlag = False
			taskFlag = False
			
			
			
			CarReset()
			testCount += 1
		
		
		AvatarReset()
		level = 1
		stage -= 1
		avatar.clearActions()
		avatar.state(1)
		moveTimer.remove()
		if testCount != 30 :
			yield viztask.waitDirector(calibrationCheck)
		
	LtoR = ((totalLeft/leftCount) + (totalLeft%leftCount))/((totalRight/rightCount)+(totalRight%rightCount))
	VC = visualCue/30 + visualCue%30
	AC = auditoryCue/30 + auditoryCue%30
	TF = taskFail/30 + taskFail%30
	result = "Left to Right Ration : %.3f\nVisualCue Rate : %.3f\nAuditoryCue Rate : %.3f\nFail Rate : %.3f\n" % (LtoR, VC, AC, TF)
	resultFile.write(result)

viztask.schedule(TestReactionTime())
##############################################################################
	

#don't move out mouse pointer
viz.mouse.setTrap()


viz.phys.enable()