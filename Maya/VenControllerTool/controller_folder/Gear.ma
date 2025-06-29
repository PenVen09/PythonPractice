//Maya ASCII 2024 scene
//Name: Gear.ma
//Last modified: Sat, Jun 28, 2025 08:44:10 PM
//Codeset: 1252
requires maya "2024";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2024";
fileInfo "version" "2024";
fileInfo "cutIdentifier" "202310181224-69282f2959";
fileInfo "osv" "Windows 10 Home Single Language v2009 (Build: 19045)";
fileInfo "UUID" "31F35437-4D4B-CC9F-BACD-96A592D99B17";
createNode transform -n "gear";
	rename -uid "EECAC7CB-4CF3-272C-77BC-ADA9877BB74E";
createNode nurbsCurve -n "gearShape" -p "gear";
	rename -uid "7F3785F8-4693-9505-2F5F-9F83B22315B5";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 36 0 no 3
		37 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29 30 31 32 33 34 35 36
		37
		-0.18314513671588711 0 -1.9688981435835975
		-0.080162230357605044 0 -1.424910142313325
		0.29136268998585652 0 -1.397105097768184
		0.64303172568212918 0 -1.2740896471493144
		0.95486788165797398 0 -1.7315681158569183
		1.3166068046861326 0 -1.4735764149704769
		1.6135439258005473 0 -1.1430580934022687
		1.1939272305203956 0 -0.78187778517239104
		1.3556098461596151 0 -0.44622497721532428
		1.4249099319855256 0 -0.080162614351173764
		1.9770167544414288 0 -0.038844183867340044
		1.9344591432773475 0 0.40342536276371044
		1.7966906553990056 0 0.82583919814592499
		1.2740908453616502 0 0.64303250439346837
		1.064247138807185 0 0.95088032303614445
		0.78187813683708685 0 1.1939274851034107
		1.0221485601850735 0 1.6927255501307752
		0.61785202490742386 0 1.8770034010800105
		0.18314513671588942 0 1.9688983820021759
		0.080162212991029352 0 1.4249104640058996
		-0.29136272471900787 0 1.397105502734753
		-0.64303177778185872 0 1.274090135389879
		-0.95486795112427925 0 1.7315686873714762
		-1.3166068046861279 0 1.4735766533890562
		-1.6135439258005448 0 1.1430583318208474
		-1.1939272478869714 0 0.78187810686496539
		-1.3556098287930369 0 0.44622513235990835
		-1.4249098972523697 0 0.080162686221762661
		-1.9770167023416967 0 0.03884417246393463
		-1.9344588458747152 0 -0.40342655041229425
		-1.7966888454342211 0 -0.82584097189697558
		-1.2740894521947093 0 -0.64303227956864217
		-1.0642471040740267 0 -0.9508802511655553
		-0.78187811947051111 0 -1.1939273299588267
		-1.0221485254519176 0 -1.692725478260187
		-0.6178520249074192 0 -1.8770031626614314
		-0.18314513671588711 0 -1.9688981435835975
		;
createNode nurbsCurve -n "gearCircleShape" -p "gear";
	rename -uid "2D15DAF8-4012-857C-B721-638DF5CC163A";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.7052504624021021 4.318413606889626e-17 -0.70525046240210221
		6.1071590907998213e-17 6.1071590907998213e-17 -0.99737476879894893
		-0.7052504624021021 4.3184136068896248e-17 -0.70525046240210199
		-0.99737476879894937 3.1659620571054249e-33 -5.1704084137723476e-17
		-0.7052504624021021 -4.3184136068896254e-17 0.7052504624021021
		-9.9907712726429024e-17 -6.107159090799825e-17 0.9973747687989496
		0.7052504624021021 -4.3184136068896248e-17 0.70525046240210199
		0.99737476879894937 -8.3283112890990895e-33 1.3601164507019631e-16
		0.7052504624021021 4.318413606889626e-17 -0.70525046240210221
		6.1071590907998213e-17 6.1071590907998213e-17 -0.99737476879894893
		-0.7052504624021021 4.3184136068896248e-17 -0.70525046240210199
		;
select -ne :time1;
	setAttr ".o" 1;
	setAttr ".unw" 1;
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
select -ne :defaultRenderGlobals;
	setAttr ".outf" 8;
select -ne :defaultResolution;
	setAttr ".w" 200;
	setAttr ".h" 200;
	setAttr ".pa" 1.7779999971389771;
	setAttr ".dar" 1.7779999971389771;
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
// End of Gear.ma
