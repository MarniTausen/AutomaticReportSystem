from PythonKnitr import Knitr
from os import listdir

document = Knitr("Camera Status report")

document.set_options(comment='', message=False, highlight=False)

document.makecodeblock("options(bitmapType='cairo')", "R")

document.figure("DisplayReport.R", height=4)

document.text("##Latest number of pictures from the Cameras")
lday = open("latestday.txt").read()
document.text("Images from day: " + lday)
document.makecodeblock("""
data <- read.csv("noplatest.csv", header=TRUE)
n <- nrow(data)
bin <- n/4
maxv <- max(data$nPictures)
ndata <- cbind(data[(bin*0+1):(bin*1),],
data[(bin*1+1):(bin*2),],
data[(bin*2+1):(bin*3),],
data[(bin*3+1):(bin*4),])
print(ndata)
cat("Problematic cameras")
data %>% filter(nPictures<maxv) -> fdata
print(fdata)
""", "R")

f = open("DIRS.txt").read()
document.text("#"+f.split("\n")[0])
document.makecodeblock("\n".join(f.split("\n")[1:]), "R", eval=False, echo=True)

allcams = sorted(listdir("pictures"), key=lambda x: int(x.split("_")[0][3:]))

document.text("##QR-detection\n")

document.makecodeblock("""
data <- read.csv("summary.csv", header=TRUE)

cat("Critical QR cameras where the center codes are missing!")
data %>% filter(CCODE==0) -> ccodes
print(ccodes)

cat("Cameras where other QR codes are missing!")
data %>% filter(CCODE==1, QRCODES<3) -> ccodes                                                                                                                                                                                             
print(ccodes)
""", "R")

document.text("##Pot-detection\n")
document.makecodeblock("""
cat("Total number of pots identified\n")
cat(sum(data$POTS), "\n")

cat("List of cameras with failed pot identifictation\n")
data %>% filter(POTS<10) -> ccodes
print(ccodes)

""", "R")


document.text("##Particular Pot sizes\n")
document.makecodeblock(""" 
h1 <- read.csv("harvest1ps.csv", header=TRUE)
h2 <- read.csv("harvest2ps.csv", header=TRUE) 

h1$Pot <- c("Aaran_0413-SM42-1", "Banca_0626-SM67-1", "Aalon_0617-RCR221-1", "Rling_0306-MIX-1", "Ctain_0747-SM109-1", "Aearl_0749-SM165A-1", "Rling_0951-SM42-1", "Aearl_0749-SM37-1", "Aearl_0749-SM125-1", "Aearl_0749-SM125-1")
h2$Pot <- c("Aaran_0413-SM42-2", "Banca_0626-SM67-2", "Aalon_0617-RCR221-2", "Rling_0306-MIX-2", "Ctain_0747-SM109-2", "Aearl_0749-SM165A-2", "Aearl_0749-SM165A-2", "Rling_0951-SM42-2", "Aearl_0749-SM37-2", "Aearl_0749-SM125-2")

h1$Date <- c("01/Jul", "01/Jul", "01/Jul", "01/Jul", "01/Jul", "01/Jul", "01/Jul", "01/Jul",
"01/Jul", "01/Jul")
h2$Date <- c("23/Jul", "23/Jul", "23/Jul", "23/Jul", "23/Jul", "23/Jul", "23/Jul", "23/Jul",
"23/Jul", "23/Jul")

h <- cbind(h1,h2)

cat("Harvest 1 (Left) vs Harvest 2 (Right)")
print(h)

""", "R")


document.text("\n##Latest-Images")
for image in allcams:
    document.text(image)
    document.text("![](pictures/"+image+")")

#document.text("![Cam1](pictures/Cam1.png)")

f = open("TEMPERATURE.txt").read()
document.text("#"+f.split("\n")[0])
document.makecodeblock("\n".join(f.split("\n")[1:]), "R", eval=False, echo=True)

f = open("BACKUPDIRS.txt").read()
document.text("#"+f.split("\n")[0])
document.makecodeblock("\n".join(f.split("\n")[1:]), "R", eval=False, echo=True)

document.compile("camreport.Rmd", output_type="github")
