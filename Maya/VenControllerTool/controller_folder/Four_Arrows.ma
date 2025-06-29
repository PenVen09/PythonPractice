//Maya ASCII 2024 scene
//Name: Four_Arrows.ma
//Last modified: Sat, Jun 28, 2025 09:16:13 AM
//Codeset: 1252
requires maya "2024";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2024";
fileInfo "version" "2024";
fileInfo "cutIdentifier" "202310181224-69282f2959";
fileInfo "osv" "Windows 10 Home Single Language v2009 (Build: 19045)";
fileInfo "UUID" "B4818E87-43C6-F3BC-5EEE-30ADC24206CC";
createNode transform -n "Four_Arrows";
	rename -uid "F135B423-49E7-47A6-5F06-A89346A5225A";
createNode nurbsCurve -n "Four_ArrowsShape" -p "Four_Arrows";
	rename -uid "22CA4888-4EAA-1248-FC56-51878F18D698";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 24 0 no 3
		25 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
		25
		0 0 -1.000750770419927
		0.40030030816797085 0 -0.60045046225195631
		0.20015015408398543 0 -0.60045046225195631
		0.20015015408398543 0 -0.20015015408398543
		0.60045046225195631 0 -0.20015015408398543
		0.60045046225195631 0 -0.40030030816797085
		1.000750770419927 0 0
		0.60045046225195631 0 0.40030030816797085
		0.60045046225195631 0 0.20015015408398543
		0.20015015408398543 0 0.20015015408398543
		0.20015015408398543 0 0.60045046225195631
		0.40030030816797085 0 0.60045046225195631
		0 0 1.000750770419927
		-0.40030030816797085 0 0.60045046225195631
		-0.20015015408398543 0 0.60045046225195631
		-0.20015015408398543 0 0.20015015408398543
		-0.60045046225195631 0 0.20015015408398543
		-0.60045046225195631 0 0.40030030816797085
		-1.000750770419927 0 0
		-0.60045046225195631 0 -0.40030030816797085
		-0.60045046225195631 0 -0.20015015408398543
		-0.20015015408398543 0 -0.20015015408398543
		-0.20015015408398543 0 -0.60045046225195631
		-0.40030030816797085 0 -0.60045046225195631
		0 0 -1.000750770419927
		;
select -ne :time1;
	setAttr ".o" 7;
	setAttr ".unw" 7;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".fprt" yes;
	setAttr ".rtfm" 1;
select -ne :renderPartition;
	setAttr -s 2 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 5 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
select -ne :standardSurface1;
	setAttr ".bc" -type "float3" 0.40000001 0.40000001 0.40000001 ;
	setAttr ".sr" 0.5;
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :defaultColorMgtGlobals;
	setAttr ".cfe" yes;
	setAttr ".cfp" -type "string" "<MAYA_RESOURCES>/OCIO-configs/Maya2022-default/config.ocio";
	setAttr ".vtn" -type "string" "ACES 1.0 SDR-video (sRGB)";
	setAttr ".vn" -type "string" "ACES 1.0 SDR-video";
	setAttr ".dn" -type "string" "sRGB";
	setAttr ".wsn" -type "string" "ACEScg";
	setAttr ".otn" -type "string" "ACES 1.0 SDR-video (sRGB)";
	setAttr ".potn" -type "string" "ACES 1.0 SDR-video (sRGB)";
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
// End of Four_Arrows.ma
