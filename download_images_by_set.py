import scrython
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import time, os
import shutil
import pprint
import pickle
from PIL import Image, ImageOps

IMAGE_PATH = './pacifism/' # You can replace this with whatever path
FILE_EXT='.jpg'

retries = Retry(total=5,
                backoff_factor=0.1,
                status_forcelist=[ 500, 502, 503, 504 ])

def get_set_code():
    all_sets = scrython.sets.Sets()
    for i, set_object in enumerate(all_sets.data()):
        print(i, all_sets.data(i, "name"))

    choice = int(input("Select your set by number: "))

    code = all_sets.data(choice, "code")
    print(code)
    return code

def save_image(path, url, name):
    if not os.path.exists(path):
        os.makedirs(path)
    output_image_file_and_path= path + name + FILE_EXT
    if not os.path.isfile(output_image_file_and_path):
        s = requests.Session()
        s.mount('https://', HTTPAdapter(max_retries=retries))
        
        img=Image.open(s.get(url, stream=True).raw) #open image with PIL
        img = ImageOps.expand(img, border=20, fill=200) # add border to help find outline
        #print(name)
        output_image_file_and_path=output_image_file_and_path.replace("//","--")
        #print(name)
        img.save(output_image_file_and_path)
        time.sleep(0.1)

def get_all_pages(set_code):
    page_count = 1
    all_data = []
    while True:
        print(page_count)
        time.sleep(0.1)
        #page=scrython.cards.Search(q='e:khm',page=page_count, unique='prints', order='usd', dir='desc')
        #page=scrython.cards.Search(q='name:pacifism',page=page_count, unique='prints', order='usd', dir='desc')
        try:
            page = scrython.cards.Search(q='e:{}'.format(set_code), page=page_count, unique='prints', order='usd', dir='desc')
        except:
            break
        all_data = all_data + page.data()
        page_count += 1
        if not page.has_more():
            break
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint (all_data)
    return all_data

def getCardByID(id_,tries):
    time.sleep(0.2)
    if tries>0:
        try:
            card = scrython.cards.Id(id=id_)
        except:
            print('Card Retry. Tries: '+str(tries))
            card=getCardByID(id_,tries-1)
    else:
        card = scrython.cards.Id(id=id_)
    return card
        
def get_all_cards(card_array):
    card_list = []
    print('Getting all cards..')
    for card in card_array:
        id_ = card['id']
        #print(str(id_))
        card = getCardByID(id_,15)
        card_list.append(card)
        if (len(card_list)%10==0 or len(card_list)==len(card_array)):
            print (len(card_list),'out of',len(card_array), 'cards found!')

    return card_list

class SetDownloader:
    def startDownload(self, setName, outputFolder='./default/'):
        self.setName=setName
        self.outputFolder='./' + outputFolder + '/'

        card_list = get_all_pages(self.setName)
        print('Got all pages')
        
        dirPickle='./pickleDump/'
        if not os.path.isdir(dirPickle):
            os.mkdir(dirPickle)
        setPickle=dirPickle+setName+'.dat'
        if not os.path.isfile(setPickle):
            card_list_objects = get_all_cards(card_list)
            with open(setPickle, 'wb') as f:
                pickle.dump(card_list_objects, f)
            print('Set saved!')
        else:
            print(setPickle)
            with open(setPickle, 'rb') as file:
                card_list_objects=pickle.load(file)
            print('Set loaded!')
        print('Got all cards')
        self.numCards=len(card_list_objects)
        index=0
        for card in card_list_objects:
            try:
                save_image(self.outputFolder, card.image_uris(0, 'normal'), card.name() + ' ID='+card.id())
            except:
                foo=1
            index+=1
            if (index%25==0 or index==len(card_list_objects)):
                print (index,'out of',len(card_list_objects), 'images saved!')

        if os.path.isfile(setPickle):
            os.remove(setPickle)

    def deleteDirectory(self):
        if os.path.isdir(self.outputFolder):
            shutil.rmtree(self.outputFolder)
        else:
            print("Directory DNE")
                
#s=SetDownloader()

##code = get_set_code()
###code='kld' #throne
##code='j21'
##card_list = get_all_pages(code)
##print('Got all pages')
##card_list_objects = get_all_cards(card_list)
##print('Got all cards')
###card_list_objects = []
##index=0
##for card in card_list_objects:
##    time.sleep(0.1)
##    save_image(IMAGE_PATH, card.image_uris(0, 'normal'), card.name() + ' ID='+card.id())
##    index+=1
##    if (index%25==0 or index==len(card_list_objects)):
##        print (index,'out of',len(card_list_objects), 'images saved!')
