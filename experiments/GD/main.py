from session import BinocularSession
import appnope


def main():
    #initials = raw_input('Your initials: ')
    #run_nr = int(raw_input('Run number: '))
    #scanner = raw_input('Are you in the scanner (y/n)?: ')
    #track_eyes = raw_input('Are you recording gaze (y/n)?: ')
    # if track_eyes == 'y':
        #tracker_on = True
    # elif track_eyes == 'n':
        #tracker_on = False

    initials = 'GdH'
    run = 1
    appnope.nope()

    ts = BinocularSession(initials, run)
    ts.run()

    # plot_mapper_staircase(initials, run_nr)


if __name__ == '__main__':
    main()
