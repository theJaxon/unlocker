#Tech Preview SMC
##Darwin

	0ee83c0: 5945 4b23 0432 3369 7580 0000 0000 0000  YEK#.23iu.......
	0eec7f0: 5945 4b23 0432 3369 7580 0000 0000 0000  YEK#.23iu.......

	015f380: d401 0000 c745 a030 4b53 4f48 8d1d 9405  .....E.0KSOH....
	015f410: 4848 83c0 4881 fb30 4b53 4f75 e348 89f9  HH..H..0KSOu.H..
	015f440: 488d 4db0 4889 dfbe 304b 534f 4c89 e2e8  H.M.H...0KSOL...

	0eec740: 304b 534f 202a 3868 6380 0000 0000 0000  0KSO *8hc.......
	0ef4200: 304b 534f 202a 3868 6390 0000 0000 0000  0KSO *8hc......

	015f4c0: c048 81fb 314b 534f 75e7 4889 f948 01c1  .H..1KSOu.H..H..
	015f500: 004c 8d75 acbf 314b 534f e952 ffff ff31  .L.u..1KSO.R...1
	
	0eec780: 0000 0000 0000 0000 314b 534f 202a 3868  ........1KSO *8h
	0ef4240: 0000 0000 0000 0000 314b 534f 202a 3868  ........1KSO *8h

##Linux

	0f82800: 5945 4b23 0432 3369 7580 0000 0000 0000  YEK#.23iu.......
	0f8a2c0: 5945 4b23 0432 3369 7580 0000 0000 0000  YEK#.23iu.......
	
	03bbde0: 3b48 8b00 8138 304b 534f 0f84 a002 0000  ;H...80KSO......
	03bbe00: 8b32 4889 d048 83c2 4881 fe30 4b53 4f0f  .2H..H..H..0KSO.
	03bc050: efc7 4424 1430 4b53 4f49 89d8 e8af 1ece  ..D$.0KSOI......
	
	0f8a210: 304b 534f 202a 3868 6390 0000 0000 0000  0KSO *8hc.......
	0f8e640: 304b 534f 202a 3868 6380 0000 0000 0000  0KSO *8hc.......
	
	03bc070: ba01 0000 0048 89ef c744 2414 314b 534f  .....H...D$.1KSO
	03bc0c0: 0f84 56fd ffff 488b 0081 3831 4b53 4f74  ..V...H...81KSOt
	03bc0e0: 8b1a 4889 d048 83c2 4881 fb31 4b53 4f74  ..H..H..H..1KSOt
	
	0f8a250: 0000 0000 0000 0000 314b 534f 202a 3868  ........1KSO *8h
	0f8e680: 0000 0000 0000 0000 314b 534f 202a 3868  ........1KSO *8h


###Exports

	appleSMCKeyTableV0 - 158A2A0
	appleSMCKeyTableV1 - 15827E0

###Header

	0x00 08 ptr  Offset of #KEY
	0x08 04 int  Count of all keys
	0x0C 04 int  Count of keys - OSK0/1
	
###Key

	0x00 04 int  Key name (byte reversed e.g. #KEY is #YEK)
	0x04 01 byte Length of returned data
	0x05 04 int  Data type of returned data (byte reversed e.g. ui32 is 23iu)
	0x09 01 byte Flag R/W
	0x0a 06 byte Padding
	0x10 08 ptr  Internal VMware routine
	0x18 48 byte Data

##Windows

	0c9a910: 5945 4b23 0432 3369 7580 0000 0000 0000  YEK#.23iu.......
	0ca23d0: 5945 4b23 0432 3369 7580 0000 0000 0000  YEK#.23iu.......
	
	04c1630: 304b 534f 4889 4424 20e8 e232 b7ff 4183  0KSOH.D$ ..2..A.
	04c16a0: 8138 304b 534f 745b ffc1 4883 c048 3bca  .80KSOt[..H..H;.
	
	0ca2320: 304b 534f 202a 3868 6390 0000 0000 0000  0KSO *8hc.......
	0ca6750: 304b 534f 202a 3868 6380 0000 0000 0000  0KSO *8hc.......
	
	04c1650: 4102 488b cfc7 4424 3431 4b53 4f48 8944  A.H...D$41KSOH.D
	04c17a0: ffff ff48 8b00 8138 314b 534f 740f ffc3  ...H...81KSOt...
	
	0ca2360: 0000 0000 0000 0000 314b 534f 202a 3868  ........1KSO *8h
	0ca6790: 0000 0000 0000 0000 314b 534f 202a 3868  ........1KSO *8h

OSK0/1 keys return 32 bytes:

	ourhardworkbythesewordsguardedpl
	easedontsteal(c)AppleComputerInc