#!bin/python3
#
# load_my_file.py
#
def file_namer(file_number,dot_extension):
    # Load the Gcode file

    file_list = ['zero','Star-Wars-Yoda', 'cat_outline_11_9_16_tsp']
    #file_name = 'PelotonLinkLogo.gcode'
    #file_name = 'cat_outline_from_unicorn'
    #file_name = 'circle_from_unicorn.gcode'
    file_name = 'Star-Wars-Yoda'
    #file_name = 'yoda_from_plotterize.gcode'
    #file_name = 'sitting_cat_outline.gcode'
    #file_name = 'tiger_10_4_16_with_unicorn.gcode'
    #file_name = 'cat_outline_11_9_16_tsp'

    ###print('loading data from: '+file_name+dot_extension)

    return file_list[file_number]+dot_extension


def file_path_os(win_or_pi):
    if win_or_pi == 'win':
        file_path = 'DrawingInputFiles/'
    if win_or_pi == 'pi':
        file_path = '/home/pi/Documents/drawing_robot/DrawingInputFiles/'
        

    return file_path




if __name__ == '__main__':
    print('Running: load_my_file.py, as MAIN')

    print(file_namer(1,'.gcode'))
