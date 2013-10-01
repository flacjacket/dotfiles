import os
import signal

def main():
    fn = os.path.expanduser('~/.dzen/pid')
    if os.path.isfile(fn):
        with open(fn, 'r') as f:
            pid = f.read().strip().split()
        for p in pid:
            os.kill(int(p), signal.SIGTERM)
        os.remove(fn)

if __name__ == '__main__':
    main()
