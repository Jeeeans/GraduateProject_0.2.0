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
avatar.collideMesh()
avatar.enable(viz.COLLIDE_NOTIFY)

def avatar_move():
	avatar.setVelocity([0,0,-3], viz.ABS_GLOBAL)
	



import random

car = viz.add('soccerball.ive')
car.collideMesh()

car_loc = random.randint(0,4)

if car_loc == 1 :
	car.setPosition(6,0.5,5)
else :
	car.setPosition(-4,.5,5)

def car_move():
	if car_loc%2 == 1:
		#car.setPosition([-.01, 0, 0], viz.ABS_LOCAL)
		#car.setEuler([-2, 0, 0], viz.REL_PARENT)
		car.setVelocity([-1,0,0], viz.ABS_GLOBAL)
	else :
		#car.setPosition([.01, 0, 0], viz.ABS_LOCAL)
		#car.setEuler([2, 0, 0], viz.REL_PARENT)
		car.setVelocity([1,0,0], viz.ABS_GLOBAL)




def onCollideBegin(e):
	if e.obj2 == car:
		print 'collide!'

viz.callback(viz.COLLIDE_BEGIN_EVENT, onCollideBegin)
viz.phys.enable()

vizact.onkeydown(' ', avatar_move)
vizact.onkeydown(' ', car_move)