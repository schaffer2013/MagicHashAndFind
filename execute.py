from save_hash import Saver
import scrython
import os
import datetime
from download_images_by_set import SetDownloader
#from magic_card_detector import MagicCardDetector

s=SetDownloader()
all_sets = scrython.sets.Sets()
cardsCounted=0

for i, set_object in enumerate(all_sets.data()):
    start_time=datetime.datetime.now()
    code=(all_sets.data(i, "code"))

    print("Set ", i, " of ", len(all_sets.data()))
    print("Set: ",all_sets.data(i, "name"), '(', all_sets.data(i, "code"), ')')
    if not os.path.isfile('./hash/' + code + '.dat'):
        s.startDownload(code,'image/'+code)
        saver=Saver('image/'+code,code)
        #s.deleteDirectory()
        end_time=datetime.datetime.now()
        delta=end_time-start_time
        print('Total time:', delta)
        if s.numCards>0:
            print('Time per card:',delta/s.numCards)
    else:
        print(code + ' is skipped!')
    #cardsCounted+=s.numCards
    #print("Cards Counted:",cardsCounted)
