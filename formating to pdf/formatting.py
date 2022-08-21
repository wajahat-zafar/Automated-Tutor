
import re
from fpdf import FPDF
def splitter():
    result5 = ""
    output = []
    matchlist= []
    matchlistresult= []
    matchindex = []
    with open('summary.txt.txt') as f:
        contents = f.read()
        x = contents.replace("i.e", "that is")
        if bool(re.search(r'\s',x)) == True:
            c = x.split('\s')

            for i in c:
                result = re.sub(r'  ', '\n', i)
                result2 = re.sub(r'.'+','+'\s',' ',result)
                result3 = re.sub(r':'+'\s',':\n',result2)
                result4 = re.sub(r'\n'+'\s','\n',result3)

            for x in result4.split("\n"):
                try:
                    x = x[0].upper() + x[1:]
                except:
                    pass
                output.append(x)
            result5 = output
            # print(result5)

            for i in result5:
                final = re.findall(r"\w+(?: \w+)*:", i)
                matchlist.append(final)
                # print(matchlist)
            for a in matchlist:
                if a != []:
                    matchlistresult.append(a[0])
            # print(matchlistresult)


        pdf = FPDF()
        pdf.add_page()
        # ##f = open(result5, "r")
        pdf.set_font('Arial', 'B', 20)
        pdf.cell(200, 10, txt="DATA COMMUNICATION AND NETWORKING",ln=1, align='C')
        pdf.cell(200,20, txt="SWITCHES",ln=1, align='C')

        pdf.set_font('Arial', '', 14)
        flag = 0
        index = 0
        for mtch in matchlistresult:
            for x in result5:
                index += 1
                if mtch in x:
                    flag = 1

                    break
            if flag == 0:
                print('String', mtch, 'Not Found')
            else:
                print('String', mtch, 'Found In Line', index)
            matchindex.append(index)
            index-=index

           #### fpdf.multi_cell(w: float, h: float, txt: str, border = 0,align: str = 'J', fill: bool = False
        for x in result5:
            pdf.multi_cell(0, 7, x, 0, 'J', False)
        # for lenth in range(len(result5)):
        #     print(lenth)
        pdf.output("try2.pdf")



splitter()