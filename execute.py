from save_hash import Saver
import scrython
import os
from download_images_by_set import SetDownloader
#from magic_card_detector import MagicCardDetector

s=SetDownloader()
all_sets = scrython.sets.Sets()
for i, set_object in enumerate(all_sets.data()):
    code=(all_sets.data(i, "code"))

    print("Set ", i, " of ", len(all_sets.data()))
    print("Set: ",all_sets.data(i, "name"), '(', all_sets.data(i, "code"), ')')
    if not os.path.isfile('./hash/' + code + '.dat'):
        s.startDownload(code,code)
        saver=Saver(code,code)
        s.deleteDirectory()
    else:
        print(code + ' is skipped!')
