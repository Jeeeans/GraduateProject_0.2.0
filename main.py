import viz
import vizact
viz.go()

#####################BackGround###################

ground = viz.add('art/sphere_ground3.ive')
ground.collidePlane(0,1,0,0)
env = viz.add(viz.ENVIRONMENT_MAP,'sky.jpg')

dome = viz.add('skydome.dlc')
dome.texture(env)

#####################Insight#######################
male = viz.add('vcc_male.cfg')
male.setPosition([1,0,0])
male.setEuler([0,0,0],viz.REL_LOCAL)
male.collideMesh()
#male.enable(viz.PHYSICS)
male.enable(viz.COLLIDE_NOTIFY)

head_bone = male.getBone('Bip01 Head')
head_bone.lock()


#################Avatar Insight####################
def onMouseMove(e):
	#print head_bone.getEuler()
	[x,y,z] = head_bone.getEuler()
	ey = y
	ez = z
	if y +(e.dx*0.5) > -60 and y +(e.dx*0.5) < 60 :
		ey = y +(e.dx*0.2)
	if z - (e.dy*0.5) >-30 and z - (e.dy*0.5) < 20 :
		ez = z - (e.dy*0.2)
	head_bone.setEuler(x, ey, ez)
viz.callback(viz.MOUSE_MOVE_EVENT, onMouseMove)

male.visible(viz.OFF)
view_link = viz.link(head_bone, viz.MainView)
viz.eyeheight(0)

#####################Avatar#####################

avatar = viz.add('soccerball.ive')
avatar.setPosition(1,0.5,11)
avatar.collideSphere()
avatar.enable(viz.COLLIDE_NOTIFY)

import random

car = viz.add('soccerball.ive')
car.collideSphere()

carLoc = random.randint(0,2)
car.setPosition(10,.5,5)


############################Timer#########################
time = 0
def Timer():
	global time
	time = time + 0.01

vizact.ontimer(0.01, Timer)
##########################Training########################
level = 1
stage = 6
carPosition = 0

import viztask

def avatar_move():
	avatar.setVelocity([0,0,level*-1-2], viz.ABS_GLOBAL)
	
	if carLoc%2 == 1:
		car.setVelocity([level*-1-2,0,0], viz.ABS_GLOBAL)
	else :
		car.setVelocity([level+2,0,0], viz.ABS_GLOBAL)
		
def Reset():
	global carLoc
	
	avatar.reset()
	avatar.setPosition(1,0.5,11)
	
	carLoc = random.randint(0,2)
	car.reset()
	car.setPosition(10,.5,5)

def GetCarPosition():
	global carPosition
	carPosition = car.getPosition();
	if carLoc%2 == 1 :
		if carPosition[0]-1 < stage/3 :
			print "1/3!!!!"
		elif carPosition[0]-1 < stage*2/3 :
			print "2/3!!!!"
	else :
		if 1-carPosition[0] < stage/3 :
			print "1/3!!!!"
		elif 1-carPosition[0] < stage*2/3 :
			print "2/3!!!!"
	
def onCollideBegin(e):
	global stage
	global level
	if e.obj2 == car:
		print 'collide!'
		Reset()
		if stage < 6 :
			stage = stage - 1
		else :
			level = level - 1


###############Use Schedule#####################################################
def TestReactionTime():
	global time
	global level
	global stage
	yield viztask.waitKeyDown(' ')
	
	while True:
		yield viztask.waitTime(vizmat.GetRandom(1.5,2.5))
		
		avatar_move()
		
		d = yield viztask.waitDraw()
		
		#Move Car Position
		if carLoc%2 == 1 :
			car.setPosition(1+stage,.5,5)
		else :
			car.setPosition(1-stage,.5,5)
		
		#Save start time
		startTime = time
		
		#Wait for mouse reaction
		
		d = yield viztask.waitAny([viztask.waitMouseDown(viz.MOUSEBUTTON_LEFT), viztask.waitEvent(viz.COLLIDE_BEGIN_EVENT)])
		reactionTime = time - startTime
		if level < 4 :
			level = level + 1
		elif stage > 1 :
			stage = stage - 1
		
		#Calculate reaction time
		

        #Print time

		print 'Reaction time:',reactionTime
		Reset()



##############################################################################

viztask.schedule(TestReactionTime())
vizact.ontimer(0.01, GetCarPosition)
viz.callback(viz.COLLIDE_BEGIN_EVENT, onCollideBegin)		

viz.mouse.setTrap()
viz.mouse.setVisible(viz.OFF)
viz.phys.enable()