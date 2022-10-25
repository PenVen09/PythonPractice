rollout menu01 "PROJECTION MAPPING WSM"
	
(
	
	label type01 "--- APPLY TO SELECTED OBJ ---"
	
	--spinner mapchannel "mapchannel" range:[1,1000000,1] type:#integer
	pickbutton mycam "SELECT CAMERA" pos:[5,30] width:130 height:30
	Button Applybutton "APPLY" pos:[150,30]width:130 height:30
	on mycam picked cam do 
	(
		mycam.text = cam.name
	)
	on Applybutton pressed do
	(
	try
	for obj in selection do
	(
	addmodifier obj (spacecameramap())
	obj.modifiers[1].cameraNode = mycam.object
	--obj.modifiers[1].channel = mapchannel.value
	)
	
	catch(print"please select CAMERA first")
	
	)
		
	)
	


rollout menu02 "Perspective Match"
	
(
	
	label type01 "--- Perspective ---"
	
	button b2 "SHOW/HIDE VANISHING LINES" pos:[5,30] width:130 height:30
	on b2 pressed do 
	(
		if Perspective_Match.IsMatching() == False then
		Perspective_Match.ShowVanishingLines()
		else
		Perspective_Match.HideVanishingLines()
	)
	
	button b11 "ENABLE/DISABLE 2D PAN ZOOM MODE" pos:[150,30]width:130 height:30
	on b11 pressed do 
	(
		actionMan.executeAction 0 "628"
	)
	
)




rollout menu03 "Cameras In Scene"
	
(
	
	label type01 "--- Lock All Cameras In the Scene ---"
	
	button b9 "LOCK ALL CAMERA" pos:[5,30] width:130 height:30
	on b9 pressed do 
	(
		mySelection = $
		select cameras
		for selCams in selection do
			
		(
			setTransformLockFlags selection #all
			clearselection()
			select mySelection
		)
	)
	
	button b10 "UNLOCK ALL CAMERA" pos:[150,30] width:130 height:30
	on b10 pressed do 
	(
		mySelection = $
		select cameras
		for selCams in selection do
			
		(
			setTransformLockFlags selection #none
			clearselection()
			select mySelection
		)
	)
	
	
	
)

	
MainFloater = newRolloutFloater "Projection Mapping Tools" 300 270
addRollout menu01 mainFloater 
addRollout menu02 mainFloater
addRollout menu03 mainFloater
