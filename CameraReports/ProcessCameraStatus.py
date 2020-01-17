from sys import argv

if __name__=="__main__":
    try:
        f = open(argv[1]).read()
    except:
        outfile = open("SYSTEM_ERROR", "w")
        outfile.write("SYSTEM IS DOWN")
        outfile.close()
        raise "No file system is down"
    if f=="":
        outfile = open("SYSTEM_ERROR", "w")
        outfile.write("SYSTEM IS DOWN")
        outfile.close()
        raise "No data system is down"
    outfile = open("camreport.csv", "w")
    flag = 0
    for lines in f.split("\n"):
        if lines[0]=="#":
            if flag==0:
                outfile.close()
                outfile = open("DIRS.txt", "w")
            if flag==1:
                outfile.close()
                outfile = open("BACKUPDIRS.txt", "w")
            if flag==2:
                outfile.close()
                outfile = open("TEMPERATURE.txt", "w")
            flag += 1
        if flag==0:
            outfile.write(",".join(lines.split(" is "))+"\n")
        if flag>0:
            outfile.write(lines+"\n")
            
    outfile.close()

