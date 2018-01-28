from steal import steal
from download import download_beatmaps
from path_helper import get_path
from os.path import join
import logging


# stupid text interaction for users
def main():
    print("~~ https://github.com/CollectorFTB ~~\n\n")
    while True:
        user_in = input("Choose an option:\n1. Create your own beatmaps.txt\n2. Download the maps that someone gave you that you don't have\n3. Close the program\n(input should be 1, 2 or 3)\n")
        print('\n\n\n\n')
        if user_in not in ['1', '2', '3']:
            print("Please try a different input")
        else:
            if user_in == '1':
                print('Creating beatmaps.txt ...')
            elif user_in == '2':
                print('Creating my_beatmaps.txt ...')
            elif user_in == '3':
                print('Why did you even open this up?')
            break

    if user_in == '1':
        steal(0)
        print("Finished creating beatmaps.txt, the file should be waiting for you after you close this window\nGive this to other people for them to download your beatmaps!")
    elif user_in == '2':
        steal(1)
        print('Finished creating my_beatmaps.txt\n\n\n\n')
        download_beatmaps(2.5)  # seconds between each beatmap
        print('Finished downloading the beatmaps you didn\'t already have!')
    input("Press enter to close the program...")

if __name__ == "__main__":
    path = get_path()[1]
    log_path = join(path, 'error_log.txt')
    logging.basicConfig(filename=log_path, level=logging.DEBUG)
    try:
        main()
    except Exception as e:
        logging.exception(str(e))
        raise


