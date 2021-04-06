import pickle
import os
import magic_card_detector as mcg

class Saver:
    def __init__(self, trainingDirectory, setName='default'):

        self.trainingDirectory='./' + trainingDirectory + '/'
        self.outputFolder='./' + setName + '/'
        self.card_detector = mcg.MagicCardDetector('./')
        self.card_detector.read_and_adjust_reference_images(self.trainingDirectory)

        hlist = []
        print(len(self.card_detector.reference_images),'images saving to hash')
        for image in self.card_detector.reference_images:
            image.original = None
            image.clahe = None
            image.adjusted = None
            hlist.append(image)
            #print(image)

        #with open('alpha_reference_phash.dat', 'wb') as f:
            #pickle.dump(hlist, f)

        if not os.path.isdir('./hash/'):
            os.mkdir('./hash/')
        with open('./hash/' + setName +'.dat', 'wb') as f:
            pickle.dump(hlist, f)
