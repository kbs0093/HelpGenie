import webbrowser
import os




def openMap(loc):

    # 인천일 경우
    if (loc == 'incheon'):
        webbrowser.open('file://' + os.path.realpath('./Geomaster/incheon.html'))

    elif (loc == 'daejeon'):
        webbrowser.open('file://' + os.path.realpath('./Geomaster/daejeon.html'))

    elif (loc == 'kwangju'):
        webbrowser.open('file://' + os.path.realpath('./Geomaster/kwangju.html'))

    return


    
