from subprocess import call
from time import strftime

class Knitr(object):

    def __init__(self, title="", author="", datascript=""):
        self.content = ""
        if title!="":
            self.content += "---\n"
            self.content += 'title: "%s"\n' % title
            self.content += 'author: %s\n' % author
            self.content += 'date: %s\n' % strftime("%d/%m/%Y - %H:%M:%S")
            self.content += "---\n\n"
        self.titles = []

    def set_options(self, echo=True, comment="##", warning=True, error=True,
                    message=True, highlight=True, background="#FFFFFF", size="normalsize",
                    seed=False, seed_num=100):
        self.content += "```{r, echo=FALSE}\n"
        self.content += "knitr::opts_chunk$set(out.format='html'"
        self.content += ", comment='%s'" % comment
        self.content += ", echo=%s" % self.bool(echo)
        self.content += ", warning=%s" % self.bool(warning)
        self.content += ", error=%s" % self.bool(error)
        self.content += ", message=%s" % self.bool(message)
        self.content += ", background='%s'" % background
        self.content += ", highlight=%s" % self.bool(highlight)
        self.content += ", size='%s'" % size
        self.content += ")\n"
        if seed: self.content += "set.seed(%i)\n" % seed_num
        self.content += "```\n\n"

    def text(self, body, title="", level=2):
        if title!="":
            self.content += "#"*level + title + "\n"
            self.titles.append(title)
        self.content += body+"\n"

    def analysis(self, script, title="", description="", language="R", data=[],
                 display=True, echo=False, level=2):
        """
        Include an R analysis which is to be run in the background.
        Toggle display to show the outputs from the scripts.
        Write a title of the analysis and give a description.
        In description you can write markdown like in any other markdown document.
        """
        if title!="":
            self.content += "#"*level + title + "\n"
            self.titles.append(title)

        if description!="":
            self.content += description + "\n"

        if language=="R":
            if script.split(".")[-1]=="R" or script.split(".")[-1]=="r":
                script = open(script).read()
            if display==False:
                self.makecodeblock(script, "r", results='hide', echo=echo)
            else:
                self.makecodeblock(script, "r", echo=echo)

        if language=="python":
            if script.split(".")[-1]=="py":
                script = open(script).read()
            if display==False:
                self.makecodeblock(script, "python", results='hide', echo=echo)
            else:
                self.makecodeblock(script, "python", echo=echo)


    def figure(self, item, title="", description="", filetype=["R", "image"],
               width=8, height=5, echo=False, language="R", fig_name='', level=2):
        """
        Include a figure in the document, with a title and a description.
        Item can either be an Rscript or an image file. Will detect using the last extension.
        However if filetype is specified then it will use that.
        """
        filetypes = ["pdf", "jpg", "jpeg", "png"]
        if title!="":
            self.content += "#"*level + title + "\n"
            self.titles.append(title)
        if description!="":
            self.content += description + "\n"

        if item.split(".")[-1]=="R":
            script = open(item).read()
            self.makecodeblock(script, "r", width=width, height=height, echo=echo)
        elif any(item.split(".")[-1]==ft for ft in filetypes):
            self.content += "<img src='%s', width='%i', height='%i'>\n\n" % (item, width*96, height*96)
        else:
            if language=="R":
                self.makecodeblock(item, "r", width=width, height=height, echo=echo)
            elif language=="python":
                self.makecodeblock(item, "python", width=width, height=height, echo=echo)
                self.content += "<img src='%s', width='%i', height='%i'>\n\n" % (fig_name, width*96, height*96)

    def save_file(self, filename):
        f = open(filename, "w")
        f.write(self.content)
        f.close()

    def compile(self, filename="", output_type="html"):
        if filename=="": filename = "output.Rmd"
        self.save_file(filename)
        f = open("compile.R", "w")
        compile_file = "#!/usr/bin/env Rscript\nlibrary(knitr)\nlibrary(rmarkdown)\nargs = commandArgs(trailingOnly=TRUE)\n"
        if output_type == "html":
            compile_file += "render(args[1], html_document(toc = TRUE, theme = 'united'))"
        if output_type == "github":
            compile_file += "render(args[1], github_document(toc = TRUE))"
        if output_type == "word":
            compile_file += "render(args[1], word_document())"
        if output_type == "md":
            compile_file += "render(args[1], md_document())"
        if output_type == "pdf":
            compile_file += "render(args[1], pdf_document())"
        f.write(compile_file)
        f.close()
        call("Rscript --vanilla compile.R %s" % filename, shell=True)

    def bool(self, b):
        return {True: "TRUE", False: "FALSE"}[b]

    def makecodeblock(self, script, lang, echo=False, width=8, height=5, results='show',
                      include=True, eval=True):
        self.content += "```{%s" % lang
        self.content += ", echo=%s" % self.bool(echo)
        self.content += ", fig.width=%f" % width
        self.content += ", fig.height=%f" % height
        self.content += ", results='%s'" % results
        self.content += ", include=%s" % self.bool(include)
        self.content += ", eval=%s" % self.bool(eval)
        self.content += "}\n"
        self.content += script+"\n"
        self.content += "```\n\n"
