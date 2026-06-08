import sys 

def osTest():
    operating_sys = sys.platform

    if operating_sys == "linux":
        print("You are on Linux")
    elif operating_sys == "win32":
        print("You are on Windows")
    

if __name__ == "__main__":
    osTest()