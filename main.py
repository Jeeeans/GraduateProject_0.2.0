import viz
import vizact
viz.go()

#####################BackGround###################

ground = viz.add('art/sphere_ground3.ive')
ground.collidePlane(0,1,0,0)
env = viz.add(viz.ENVIRONMENT_MAP,'sky.jpg')

dome = viz.add('skydome.dlc')
dome.texture(env)

#####################Avatar#######################
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
avatar.setPosition(1,0.5,10)
avatar.collideSphere()
avatar.enable(viz.COLLIDE_NOTIFY)

import random

car = viz.add('soccerball.ive')
car.collideSphere()

car_loc = random.randint(0,4)
car.setPosition(10,.5,5)


def avatar_move():
	avatar.setVelocity([0,0,-3], viz.ABS_GLOBAL)
	
	if car_loc%2 == 1:
		car.setVelocity([-3,0,0], viz.ABS_GLOBAL)
	else :
		car.setVelocity([3,0,0], viz.ABS_GLOBAL)


##########################Training########################

stage = 5
carPosition = 0
import viztask


def Reset():
	global car_loc
	
	avatar.reset()
	avatar.setPosition(1,0.5,10)
	
	car_loc = random.randint(0,4)
	car.reset()
	car.setPosition(10,.5,5)

def GetCarPosition():
	global carPosition
	carPosition = car.getPosition();
	print carPosition
	
def onCollideBegin(e):
	if e.obj2 == car:
		print 'collide!'
		
def TestReactionTime():
	global stage
	yield viztask.waitKeyDown(' ')
	
	while True:
		yield viztask.waitTime(vizmat.GetRandom(1.5,2.5))
		
		avatar_move()
		
		d = yield viztask.waitDraw()
		
		#Move Car Position
		if car_loc%2 == 1 :
			car.setPosition(1+stage,.5,5)
		else :
			car.setPosition(1-stage,.5,5)
		
		#Save start time
		startTime = d.time
		
		#Wait for mouse reaction
		
		#d = yield viztask.waitEvent(viz.COLLIDE_BEGIN_EVENT)
		#d = yield viztask.waitAny([viztask.waitMouseDown(viz.MOUSEBUTTON_LEFT), viztask.waitCall(viz.callback(viz.COLLIDE_BEGIN_EVENT, onCollideBegin)	)])
		d = yield viztask.waitMouseDown(viz.MOUSEBUTTON_LEFT)
		
		
		#Calculate reaction time
		reactionTime = d.time - startTime

        #Print time

		print 'Reaction time:',reactionTime
		Reset()


viz.callback(viz.COLLIDE_BEGIN_EVENT, onCollideBegin)		

viztask.schedule(TestReactionTime())
vizact.ontimer(0.01, GetCarPosition)
viz.phys.enable()