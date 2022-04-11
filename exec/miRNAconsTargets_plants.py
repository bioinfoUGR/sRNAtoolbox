#!/usr/bin/python3

import argparse, os.path, sys, re, time
from queue import Queue
from threading import Thread

parser = argparse.ArgumentParser(description='Arguments (positional) for miRNAconstargets (plants):')
parser.add_argument('microRNA_file', help='The microRNA input file in fasta format.')
parser.add_argument('target_file',help='The target sequences (3p UTR) in fasta format.')
parser.add_argument('output_directory', help='Output directory.')
parser.add_argument('threads', help='Number of threads that should be used.')
parser.add_argument('program_string', help='Each available program is identified by a string. TAPIR_FASTA, TAPIR_HYBRID, and PSROBOT do exit. To use all, specify: \'TAPIR_FASTA:TAPIR_HYBRID:PSROBOT\'')
parser.add_argument('program_parameters', nargs='?', default='', help='The parameters need to be given in the same order enclosed in simple quotation marks like: \'arguments passed to TAPIR_FASTA:arguments passed to PSROBOT\' for program_string \'TAPIR_FASTA:PSROBOT\'')
args = parser.parse_args()

wd = args.output_directory
if wd == "":
	wd = "."
if wd[-1] == "/":
	wd = wd[:-1]
programs = {"PSRT":"{}/psRNATarget.txt".format(wd), "PSROBOT":"psRobot_tar", "TAPIR_FASTA":"tapir_fasta", "TAPIR_HYBRID":"tapir_hybrid"}
tmp_files = {"TAPIR_FASTA":[], "TAPIR_HYBRID":[]}

def inputfiles(microRNA_file,target_file,wd):
	microRNA_tmp = "{}/microRNA_tmp.fa".format(wd)
	target_tmp = "{}/target_tmp.fa".format(wd)
	with open(microRNA_file,"rt") as r:
		with open(microRNA_tmp,"wt") as w:
			for line in r:
				if line[0] == ">":
					t = re.split(r'\s+| +|\t+',line)
					w.write(t[0]+"\n")
				else:
					w.write(line)
	with open(target_file,"rt") as r:
		with open(target_tmp,"wt") as w:
			for line in r:
				if line[0] == ">":
					t = re.split(r'\s+| +|\t+',line)
					w.write(t[0]+"\n")
				else:
					w.write(line)
	return (microRNA_tmp,target_tmp)

def logFile(TYPE,TEXT):
	with open("{}/logFile".format(wd),"at") as log:
		DATE = time.ctime(time.time())
		logline = " ".join([DATE,TYPE,TEXT]) + "\n"
		log.write(logline)
	
def nofile(f):
	sys.stderr.write("\x1b[1m")
	sys.stderr.write("\x1b[31m")
	sys.stderr.write("\x1b[40m")
	sys.stderr.write("{} does not exist!\n".format(f))
	sys.stderr.write("\x1b[0m")
	logFile("ERROR:","{} does not exist!\n".format(f))
	sys.exit()

def numToWords(num,join=True):
	'''words = {} convert an integer number into words'''
	units = ['','one','two','three','four','five','six','seven','eight','nine']
	teens = ['','eleven','twelve','thirteen','fourteen','fifteen','sixteen', \
			 'seventeen','eighteen','nineteen']
	tens = ['','ten','twenty','thirty','forty','fifty','sixty','seventy', \
			'eighty','ninety']
	thousands = ['','thousand','million','billion','trillion','quadrillion', \
				 'quintillion','sextillion','septillion','octillion', \
				 'nonillion','decillion','undecillion','duodecillion', \
				 'tredecillion','quattuordecillion','sexdecillion', \
				 'septendecillion','octodecillion','novemdecillion', \
				 'vigintillion']
	words = []
	if num==0: words.append('zero')
	else:
		numStr = '%d'%num
		numStrLen = len(numStr)
		groups = int((numStrLen+2)/3)
		numStr = numStr.zfill(groups*3)
		for i in range(0,groups*3,3):
			h,t,u = int(numStr[i]),int(numStr[i+1]),int(numStr[i+2])
			g = groups-(i/3+1)
			if h>=1:
				words.append(units[h])
				words.append('hundred')
			if t>1:
				words.append(tens[t])
				if u>=1: words.append(units[u])
			elif t==1:
				if u>=1: words.append(teens[u])
				else: words.append(tens[t])
			else:
				if u>=1: words.append(units[u])
			if (g>=1) and ((h+t+u)>0): words.append(thousands[g]+',')
	if join: return ' '.join(words)
	return words

def args_check(args):
	if not os.path.exists(args.microRNA_file):
		nofile(args.microRNA_file)
	if not os.path.exists(args.target_file):
		nofile(args.target_file)
	if not os.path.exists(args.output_directory):
		os.system("mkdir {}".format(args.output_directory))
	try:
		args.threads = int(args.threads)
	except:
		sys.stderr.write("\x1b[1m")
		sys.stderr.write("\x1b[31m")
		sys.stderr.write("\x1b[40m")
		sys.stderr.write("'threads' must be an integer!\n")
		sys.stderr.write("\x1b[0m")
		logFile("ERROR:","'threads' must be an integer!")
		sys.exit()
	programlist = []
	for program in args.program_string.split(":"):
		program = program.upper()
		if program in programs:
			programlist.append(program)
			if program == "PSRT":
				if not os.path.exists(programs[program]):
					sys.stderr.write("\x1b[1m")
					sys.stderr.write("\x1b[31m")
					sys.stderr.write("\x1b[40m")
					sys.stderr.write("The output file of psRNATarget cannot be found!\n")
					sys.stderr.write("Move the output files of psRNATarget to {}/psRNATarget.txt\n".format(wd))
					sys.stderr.write("\x1b[0m")
					logFile("ERROR:","The output file of psRNATarget cannot be found!")
					logFile("ERROR:","Move the output files of psRNATarget to {}/psRNATarget.txt".format(wd))
					sys.exit()
		else:
			sys.stderr.write("\x1b[1m")
			sys.stderr.write("\x1b[31m")
			sys.stderr.write("\x1b[40m")
			sys.stderr.write("{}: unknown program!\n".format(program))
			sys.stderr.write("Use 'PSRT' for psRNATarget, 'PSROBOT' for psRobot, 'TAPIR_FASTA' for tapir_fasta, or 'TAPIR_HYBRID' for tapir_hybrid.\n")
			sys.stderr.write("\x1b[0m")
			logFile("ERROR:","{}: unknown program!".format(program))
			logFile("ERROR:","Use 'PSRT' for psRNATarget, 'PSROBOT' for psRobot, 'TAPIR_FASTA' for tapir_fasta, or 'TAPIR_HYBRID' for tapir_hybrid.")
			sys.exit()
	cstr = len(programlist)
	parameterlist = args.program_parameters.split(":")
	cpar = len(parameterlist)
	if cstr > cpar:
		c = cstr - cpar
		wstr = numToWords(cstr)
		wpar = numToWords(cpar)
		num = numToWords(c)
		sys.stderr.write("\x1b[1m")
		sys.stderr.write("\x1b[31m")
		sys.stderr.write("\x1b[40m")
		sys.stderr.write("Given {} list(s) of parameters for {} program(s)!\n".format(wpar,wstr))
		sys.stderr.write("The last {} program(s) will use the default parameters.\n".format(num))
		sys.stderr.write("\x1b[0m")
		logFile("WARNING:","Given {} list(s) of parameters for {} program(s)!".format(wpar,wstr))
		logFile("WARNING:","The last {} program(s) will use the default parameters.".format(num))
		[parameterlist.append("") for i in range(0,c)]
	elif cpar > cstr:
		c = cpar - cstr
		wstr = numToWords(cstr)
		wpar = numToWords(cpar)
		num = numToWords(c)
		sys.stderr.write("\x1b[1m")
		sys.stderr.write("\x1b[31m")
		sys.stderr.write("\x1b[40m")
		sys.stderr.write("Given {} list(s) of parameters for {} program(s)!\n".format(wpar,wstr))
		sys.stderr.write("The last {} list(s) will be ignored.\n".format(num))
		sys.stderr.write("\x1b[0m")
		logFile("WARNING:","Given {} list(s) of parameters for {} program(s)!".format(wpar,wstr))
		logFile("WARNING:","The last {} list(s) will be ignored.".format(num))
		parameterlist = parameterlist[:cstr]
	for i in range(0,cstr):
		parameterlist[i] = parameterlist[i].replace('"','').replace("'","")		 
	args.program_string = programlist	
	args.program_parameters = parameterlist
	return args

def oneMiRfile(args):
	tmp_list = []
	c = 0
	with open("{}".format(args.microRNA_file),"rt") as ALLMIR:
		while True:
			header = ALLMIR.readline()
			seq = ALLMIR.readline()
			if not header: break
			if not seq: break
			tfile = "{}/tmp/{}.fa".format(wd,c)
			with open(tfile,"wt") as ONEMIR:
				ONEMIR.write(header)
				ONEMIR.write(seq)
				tmp_list.append(tfile)
			c += 1
	return tmp_list

def do_stuff(q,):
	while not q.empty():
		cmd = q.get()
		os.system(cmd)
		q.task_done()

def joinTmpFiles(tmp_list,f,ext):
	tmp_string = " ".join(tmp_list).replace(".fa",ext)
	os.system("cat {} > {}".format(tmp_string,f))
	os.system("rm -f {}".format(tmp_string))
	
def execute_programs(args):
	if os.path.exists("{}/tmp".format(wd)):
		logFile("WARNING:","Cleaning previous temporary files!")
		os.system("rm -r -f {}/tmp/*".format(wd))
	else:
		os.system("mkdir {}/tmp".format(wd))
	c = 0
	for program in args.program_string:
		if program == "PSRT":
			c += 1
		elif program == "PSROBOT":
			par = args.program_parameters[c]
			p = re.search("-p\s+\d+", par)
			if p is not None:
				par = par.replace(p.group(0),"")
			s = re.search("-s\s+[0-9a-zA-Z_\.]+", par)
			if s is not None:
				par = par.replace(s.group(0),"")
			t = re.search("-t\s+[0-9a-zA-Z_\.]+", par)
			if t is not None:
				par = par.replace(p.group(0),"")
			logFile("INFO:","Running psRobot...")
			cmd = "{} -s {} -t {} -p {} {} -o {}/tmp/{}-{}.gTP".format(programs[program],args.microRNA_file,args.target_file,args.threads,par,wd,args.microRNA_file.split("/")[-1].split(".")[0],args.target_file.split("/")[-1].split(".")[0])
			cmd = cmd.replace("  "," ")
			os.system(cmd)
			logFile("SUCCESS:","Analysis completed successfully.")
			c += 1
		elif program == "TAPIR_FASTA":
			q = Queue(maxsize=0)
			par = args.program_parameters[c]
			mir_file = re.search("--mir_file\s+[0-9a-zA-Z_\.]+", par)
			if mir_file is not None:
				par = par.replace(mir_file.group(0),"")
			target_file = re.search("--target_file\s+[0-9a-zA-Z_\.]+", par)
			if target_file is not None:
				par = par.replace(target_file.group(0),"")
			logFile("INFO:","Running tapir_fasta...")
			tmp_files["TAPIR_FASTA"] = oneMiRfile(args)
			for tfile in tmp_files["TAPIR_FASTA"]:
				cmd = "{} --mir_file {} --target_file {} {} > {}".format(programs[program],tfile,args.target_file,par,tfile.replace(".fa",".tapir_fasta"))
				cmd = cmd.replace("  "," ")
				q.put(cmd)
			for i in range(args.threads):
				worker = Thread(target=do_stuff, args=(q,))
				worker.setDaemon(True)
				worker.start()
			q.join()
			joinTmpFiles(tmp_files["TAPIR_FASTA"],"{}/tmp/{}-{}.tapir_fasta".format(wd,args.microRNA_file.split("/")[-1].split(".")[0],args.target_file.split("/")[-1].split(".")[0]),".tapir_fasta")
			logFile("SUCCESS:","Analysis completed successfully.")
			c += 1
		elif program == "TAPIR_HYBRID":
			q = Queue(maxsize=0)
			par = args.program_parameters[c]
			mir_file = re.search("--mir_file\s+[0-9a-zA-Z_\.]+", par)
			if mir_file is not None:
				par = par.replace(mir_file.group(0),"")
			target_file = re.search("--target_file\s+[0-9a-zA-Z_\.]+", par)
			if target_file is not None:
				par = par.replace(target_file.group(0),"")
			logFile("INFO:","Running tapir_hybrid...")
			tmp_files["TAPIR_HYBRID"] = oneMiRfile(args)
			for tfile in tmp_files["TAPIR_HYBRID"]:
				cmd = "{} {} {} {} | hybrid_parser > {}".format(programs[program],tfile,args.target_file,par,tfile.replace(".fa",".tapir_hybrid"))
				cmd = cmd.replace("  "," ")
				q.put(cmd)
			for i in range(args.threads):
				worker = Thread(target=do_stuff, args=(q,))
				worker.setDaemon(True)
				worker.start()
			q.join()
			joinTmpFiles(tmp_files["TAPIR_HYBRID"],"{}/tmp/{}-{}.tapir_hybrid".format(wd,args.microRNA_file.split("/")[-1].split(".")[0],args.target_file.split("/")[-1].split(".")[0]),".tapir_hybrid")
			logFile("SUCCESS:","Analysis completed successfully.")
			c += 1

def make_consensus(args):
	miR_Target = {}
	for program in args.program_string:
		if program == "PSRT":
			logFile("INFO:","Postprocessing the results of psRNATarget...")
			with open("{}".format(programs[program]),"rt") as ifile:
				ifile.readline()
				ifile.readline()
				with open("{}/PSRT.txt".format(args.output_directory),"wt") as ofile:
					for iline in ifile:
						iline = iline.strip().split("\t")
						oline = "\t".join([iline[0],iline[1],"-"+iline[3],iline[6],iline[7],iline[2]]) + "\n"
						ofile.write(oline)
						mRT = "@".join([iline[0],iline[1]])
						if not mRT in miR_Target:
							miR_Target[mRT] = ["PSRT"]
						else:
							miR_Target[mRT].append("PSRT")
			logFile("SUCCESS:","Postprocessing completed.")				
		elif program == "PSROBOT":
			logFile("INFO:","Postprocessing the results of psRobot...")
			ifile = "{}/tmp/{}-{}.gTP".format(wd,args.microRNA_file.split("/")[-1].split(".")[0],args.target_file.split("/")[-1].split(".")[0])
			with open(ifile,"rt") as ifile:
				with open("{}/PSROBOT.txt".format(args.output_directory),"wt") as ofile:
					ilines = ifile.readlines()
					ilines = "".join(ilines)
					ilines = ilines.split("\n\n\n")
					for iline in ilines:
						iline = iline.split("\n")
						if not iline == ['']:
							new = re.split(r'\s+| +|\t+',iline[0])
							mR = new[0].replace(">","")
							T = new[-1]
							mRT = "@".join([mR,T])
							energy = "n/a"
							tmp = re.split(r'\s+| +|\t+',iline[4])
							Tstart = tmp[1]
							Tend = tmp[3]
							score = new[1].replace("Score:","").strip()
							oline = "\t".join([mR,T,energy,Tstart,Tend,score]) + "\n"
							ofile.write(oline)
							if not mRT in miR_Target:
								miR_Target[mRT] = ["PSROBOT"]
							else:
								miR_Target[mRT].append("PSROBOT")
			logFile("SUCCESS:","Postprocessing completed.")
		elif program == "TAPIR_FASTA":
			logFile("INFO:","Postprocessing the results of tapir_fasta...")
			ifile = "{}/tmp/{}-{}.tapir_fasta".format(wd,args.microRNA_file.split("/")[-1].split(".")[0],args.target_file.split("/")[-1].split(".")[0])
			with open(ifile,"rt") as ifile:
				with open("{}/TAPIR_FASTA.txt".format(args.output_directory),"wt") as ofile:
					oline, mR, T, mRT, energy, Tstart, Tend, score = "", "", "", "@", "n/a", "0", "0", "0"
					for iline in ifile:
						if any([iline.startswith("#"),iline.startswith("//")]):
							if all([mR!="",T!=""]):
								oline = "\t".join([mR,T,energy,Tstart,Tend,score]) + "\n"
								ofile.write(oline)
								mRT = "@".join([mR,T])
								if not mRT in miR_Target:
									miR_Target[mRT] = ["TAPIR_FASTA"]
								else:
									miR_Target[mRT].append("TAPIR_FASTA")
							oline, mR, T, mRT, energy, Tstart, Tend, score = "", "", "", "@", "n/a", "0", "0", "0"
						elif iline.startswith("miRNA "):
							tmp = re.split(r'\s+| +|\t+',iline)
							mR = tmp[1]
						elif iline.startswith("target "):
							tmp = re.split(r'\s+| +|\t+',iline)
							T = tmp[1]
						elif iline.startswith("score"):
							tmp = re.split(r'\s+| +|\t+',iline)
							score = tmp[1]
						elif iline.startswith("start"):
							tmp = re.split(r'\s+| +|\t+',iline)
							Tstart = tmp[1]
						elif iline.startswith("miRNA_3'"):
							tmp = re.split(r'\s+| +|\t+',iline)
							seq = tmp[1]
							Tend = str(int(Tstart) + len(seq) - 1)
					if all([mR!="",T!=""]):
						oline = "\t".join([mR,T,energy,Tstart,Tend,score]) + "\n"
						ofile.write(oline)
						mRT = "@".join([mR,T])
						if not mRT in miR_Target:
							miR_Target[mRT] = ["TAPIR_FASTA"]
						else:
							miR_Target[mRT].append("TAPIR_FASTA")
			logFile("SUCCESS:","Postprocessing completed.")
		elif program == "TAPIR_HYBRID":
			logFile("INFO:","Postprocessing the results of tapir_hybrid...")
			ifile = "{}/tmp/{}-{}.tapir_hybrid".format(wd,args.microRNA_file.split("/")[-1].split(".")[0],args.target_file.split("/")[-1].split(".")[0])
			with open(ifile,"rt") as ifile:
				with open("{}/TAPIR_HYBRID.txt".format(args.output_directory),"wt") as ofile:
					oline, mR, T, mRT, energy, Tstart, Tend, score = "", "", "", "@", "n/a", "0", "0", "0"
					for iline in ifile:
						if any([iline.startswith("#"),iline.startswith("//")]):
							if all([mR!="",T!=""]):
								oline = "\t".join([mR,T,energy,Tstart,Tend,score]) + "\n"
								ofile.write(oline)
								mRT = "@".join([mR,T])
								if not mRT in miR_Target:
									miR_Target[mRT] = ["TAPIR_HYBRID"]
								else:
									miR_Target[mRT].append("TAPIR_HYBRID")
							oline, mR, T, mRT, energy, Tstart, Tend, score = "", "", "", "@", "n/a", "0", "0", "0"
						elif iline.startswith("miRNA "):
							tmp = re.split(r'\s+| +|\t+',iline)
							mR = tmp[1]
						elif iline.startswith("target "):
							tmp = re.split(r'\s+| +|\t+',iline)
							T = tmp[1]
						elif iline.startswith("score"):
							tmp = re.split(r'\s+| +|\t+',iline)
							score = tmp[1]
						elif iline.startswith("start"):
							tmp = re.split(r'\s+| +|\t+',iline)
							Tstart = tmp[1]
						elif iline.startswith("miRNA_3'"):
							tmp = re.split(r'\s+| +|\t+',iline)
							seq = tmp[1]
							Tend = str(int(Tstart) + len(seq) - 1)
					if all([mR!="",T!=""]):
						oline = "\t".join([mR,T,energy,Tstart,Tend,score]) + "\n"
						ofile.write(oline)
						mRT = "@".join([mR,T])
						if not mRT in miR_Target:
							miR_Target[mRT] = ["TAPIR_HYBRID"]
						else:
							miR_Target[mRT].append("TAPIR_HYBRID")
			logFile("SUCCESS:","Postprocessing completed.")
	logFile("INFO:","Making consensus...")
	with open("{}/consensus.txt".format(args.output_directory),"wt") as ofile:
		for mRT in miR_Target:
			iline = mRT.split("@")
			col1 = iline[0]
			col2 = iline[1]
			miR_Target[mRT] = list(set(miR_Target[mRT]))
			col3 = str(len(miR_Target[mRT]))
			col4 = str(miR_Target[mRT])
			oline = "\t".join([col1,col2,col3,col4]) + "\n"
			ofile.write(oline)
	logFile("SUCCESS:","Consensus performed.")
	logFile("INFO:","Cleaning temporary files...")
	os.system("rm -r -f {}/tmp".format(wd))
	#os.system("rm -f {}/microRNA_tmp.fa {}/target_tmp.fa".format(wd,wd))
	logFile("SUCCESS:","Work done.")
	for program in args.program_string:
		logFile("BACKVALUE:","{}/{}.txt".format(wd,program.upper()))
	logFile("BACKVALUE:","{}/consensus.txt".format(wd,program.upper()))

def make_positional_consensus(args):
	logFile("INFO:", "Making positional consensus...")
	try:
		file_string = []
		for program in args.program_string:
			if program == "PSRT":
				file_string.append("PSRT.txt")
			elif program == "PSROBOT":
				file_string.append("PSROBOT.txt")
			elif program == "TAPIR_FASTA":
				file_string.append("TAPIR_FASTA.txt")
			elif program == "TAPIR_HYBRID":
				file_string.append("TAPIR_HYBRID.txt")
		file_string = ",".join(file_string)

		if len(args.program_string) > 1:
			nconsensus = len(args.program_string) - 1
		else:
			nconsensus = len(args.program_string)

		cmd= "java -jar /opt/sRNAtoolboxDB/exec/makeTargetPositionalConsensus.jar %s %s %s %i 7" \
			 "" %(args.output_directory, file_string, args.target_file, nconsensus)
		os.system(cmd)
		logFile("SUCCESS:", "Consensus performed.")
		logFile("INFO:", "Cleaning temporary files...")
		os.system("rm -f {}/microRNA_tmp.fa {}/target_tmp.fa".format(wd, wd))
	except:
		print("An exception occurred")

def main(args):
	args = args_check(args)
	newfiles = inputfiles(args.microRNA_file,args.target_file,wd)
	args.microRNA_file, args.target_file = newfiles[0], newfiles[1]
	execute_programs(args)
	make_consensus(args)
	make_positional_consensus(args)
		
if __name__ == '__main__':
	main(parser.parse_args())
