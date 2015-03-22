#-*- coding: utf-8 -*-
import viz
import vizact
import vizinput
import vizinfo
import random
import viztask
import vizdlg

viz.go()

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
info = vizinfo.InfoPanel("Task Information.", align=viz.ALIGN_CENTER_CENTER, icon=False)
def showTaskInfo():
	global info
	info.addSeparator()
	taskInfo = "이것은 Virtual Street Task 입니다. 이 테스트는 길을 건너오는 아바타가 차에 치이지 않도록 하는 것이 목적입니다.\n 차가 나오는 방향에 따라 마우스의 왼쪽 또는 오른쪽 버튼을 누르십시오. 차가 왼쪽에서 나타난다면 왼쪽버튼을 오른쪽에서 나타난다면 오른쪽버튼을 누르시면 됩니다. 차가 나오는 방향을 맞추셨다면 점점 난이도가 올라가게 될 것입니다."
	info.addItem(viz.addText(taskInfo))
		
#####################BackGround###################
ground = viz.add('ground.osgb')

ground.collidePlane(0,1,0,0)
#env = viz.add(viz.ENVIRONMENT_MAP,'sky.jpg')

dome = viz.add('skydome.dlc')
#dome.texture(env)

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
headLight = [1,2]
for element in headLight:
	element = viz.addLight()
	element.position(0,0,0,1)
	element.spread(30)
	element.intensity(100)
	element.color(255,0,0)
	viz.link(car, element)

#####################Cross Walk Light####################
greenLight = viz.addLight()
greenLight.color(0,255,0)
greenLight.setPosition(0,0,10)

redLight = viz.addLight()
redLight.color(255,0,0)
redLight.setPosition(0,2,10)

############################Timer#########################
time = 0
def Timer():
	global time
	time = time + 0.01

vizact.ontimer(0.01, Timer)

##########################Functions########################
level = 1
stage = 1
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
	avatar.setPosition(0,0,21-stage)
	
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
			if carPosition[0] < (13-stage)/3 :
				auditoryFlag = True
			elif carPosition[0] < (13-stage)*2/3 :
				visualFlag = True
		else :
			if -1*carPosition[0] < (-13+stage)/3 :
				auditoryFlag = True
			elif -1*carPosition[0] < (-13+stage)*2/3 :
				visualFlag = True
				
def startCalibration() :
	global center
	global calibration
	global text
	center.visible(viz.ON)
	calibration.visible(viz.ON)
	text.visible(viz.ON)
	
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
	elif stage < 6 :
		stage = stage + 1
		
def incorrectReact():
	global level
	global stage
	global taskFail
	if stage > 1 :
		stage = stage - 1
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
	
	global taskFail
	testCount = 0
	leftReactionTime = 0
	rightReactionTime = 0
	
	visualCue = 0
	auditoryCue = 0
	
	waitMouseLEFT = viztask.waitMouseDown(viz.MOUSEBUTTON_LEFT)
	waitMouseRIGHT = viztask.waitMouseDown(viz.MOUSEBUTTON_RIGHT)
	waitCollide = viztask.waitEvent(viz.COLLIDE_BEGIN_EVENT)

	#######User Input########
	viz.MainView.setScene(3)
	viz.mouse.setVisible(viz.ON)
	
	
	
	form = InputForm(title="User Information")

	viz.link(viz.MainWindow.CenterCenter, form)
	
	yield form.show()
	
	if form.accepted:
		name = form.name.get()
		number = form.number.get()
		level = int(form.level.get())
		stage = int(form.stage.get())
		
		######################ResultFile#########################
		fileName = 'result_'+name+'('+number+').txt'
		resultFile = open(fileName, "w")

		result = "Reaction time\tLeft Reaction Time\tRight ReactionTime\n"
		resultFile.write(result)
		print 'name:',name,'level:',level,'stage:',stage
		
	form.remove()
	viz.mouse.setVisible(viz.OFF)
	
	
	showTaskInfo()
	yield viztask.waitTime(4)
	global info
	info.visible(viz.OFF)
	
	viz.MainView.setEuler(calibrationEuler)
	viz.MainView.setScene(1)
	Reset()
	
	startCalibration()
	yield viztask.waitDirector(calibrationCheck)
	
	#Start test from space down
	yield viztask.waitKeyDown(' ')
	
	#test
	while testCount < 10:
		yield viztask.waitTime(vizmat.GetRandom(2,4))
		
		avatar_move()
		
		d = yield viztask.waitDraw()
		
		#Move Car Position
		if carLoc%2 == 1 :
			car.setPosition(13-stage,0.1,10)
		else :
			car.setPosition(-13+stage,0.1,10)
		
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
		
		
		if visualFlag :
			visualCue += 1
			visualFlag = False
		if auditoryFlag :
			auditoryCue += 1
			auditoryFlag = False
			
		
		#print 'Task ',testCount+1,' Traing'
		#print 'Reaction time : ',reactionTime
		#print 'Left Reaction Time : ',leftReactionTime
		#print 'Right Reaction Time : ',rightReactionTime
		
		result = "%f\t\t%f\t\t%f\n" % (reactionTime, leftReactionTime, rightReactionTime)
		resultFile.writelines(result)
		
		
		testCount += 1
		Reset()
		
		startCalibration()
		yield viztask.waitDirector(calibrationCheck)
		
	result = "\nVisualCue : %d\tAuditoryCue : %d\tFailCount : %d\n" % (visualCue, auditoryCue, taskFail)
	resultFile.write(result)
	#print 'vizsualCue : ',visualCue
	#print 'auditorycue : ',auditoryCue
	#print 'FailCount : ',taskFail

viztask.schedule(TestReactionTime())
##############################################################################
vizact.ontimer(0.01, GetCarPosition)	

#don't move out mouse pointer
viz.mouse.setTrap()
#unvisible mouse pointer



viz.phys.enable()