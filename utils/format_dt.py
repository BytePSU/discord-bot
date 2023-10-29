from datetime import datetime 


def current_time(): 
    '''formats the current time in a nicely manner'''
    now = datetime.now()
    return now.strftime("%b %d, %Y at %H:%M")




