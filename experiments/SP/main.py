import sys
from session import SPSession
import appnope


def main():
    # initials = sys.argv[1]
    # initials = raw_input('Your initials: ')
    # run_nr = int(raw_input('Run number: '))
    # scanner = raw_input('Are you in the scanner (y/n)?: ')
    # track_eyes = raw_input('Are you recording gaze (y/n)?: ')
    # if track_eyes == 'y':
    #     tracker_on = True
    # elif track_eyes == 'n':
    #     tracker_on = False

    initials = 'test'
    run_nr = 1
    tracker_on = False
    appnope.nope()

    ts = SPSession(subject_initials=initials, index_number=run_nr, tracker_on=tracker_on)
    ts.run()

if __name__ == '__main__':
    main()
