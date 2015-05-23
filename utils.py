import sys, getopt, os

arg_dict = None
login_opt = '--login'
password_opt = '--password'
ch_driver_opt = '--chrome-driver'

def main():
    options = [login_opt[2:] + '=', password_opt[2:] + '=',
               ch_driver_opt[2:] + '=']
    try:
        parsed_args = getopt.getopt(sys.argv[1:], [], options)
    except getopt.GetoptError as e:
        print("Improper arguments: " + e.msg)
        sys.exit(1)
    global arg_dict
    arg_dict = dict(parsed_args[0])

def get_arg(key):
    return arg_dict[key]

def check_required_arg(*args):
    """ Check if the required command line arguments were provided 
       When an argument which is missing is encountered it is returned.
    """
    for a in args:
        if a not in arg_dict:
            return a


def save_response(response, file_name, path='~/tmp/fcb-analyzer'):
    """Write response text to a file """
    
    path = ensure_path(path)
    f = open(path + '/' + file_name, 'w')
    f.write(response.text)

def save_data(data,file):
    """Save a data sequence containing pair (2-tuples) to a file."""

    f = open(file, mode='w',encoding='utf-8', buffering=1024)
    for t in data:
        f.write(str(t[0]) + ', ' + str(t[1]) + '\n')
    f.close()
    

def ensure_path(path):
    """"
    Ensure that the parent folders on the given path exist creating
    them as needed. Also expand character'~' to user home directory path
    and return the absolute path.
    """

    path = os.path.expanduser(path)
    #Do not take into consideration the last path element
    #Unless it end with '/'
    os.makedirs('/'.join(path.split('/')[:-1]), exist_ok=True)
    return path

def exit_program(msg):
    """ Gracefully ends the application and presents the message to the user."""
    print(msg)
    sys.exit(1)
    
def log(msg):
    print(msg)

main()



