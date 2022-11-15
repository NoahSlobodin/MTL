dataset_id = "cbfbec1c-5558-c2ff-d67d-d4b51056fba3" #put in the dataset ID. this comes directly from constellate client

import constellate
import re #i really didnt want it to come to this but here we are...
re.I #ignore case. This will become important later.

dataset_file = constellate.get_dataset(dataset_id)
dataset_metadata = constellate.get_metadata(dataset_id)

import pandas as pd
import os

pre_processed_filename = f'data/preprocessed_{dataset_id}.csv'

if os.path.exists(pre_processed_filename): #this may be important for using file preprocessing
    df = pd.read_csv(pre_processed_file_name)
    filtered_id_list = df["id"].tolist()
    use_filtered_list = True
    print(f'Pre-Processed CSV found. Filtered dataset is ' + str(len(df)) + ' documents.')
else:
    use_filtered_list = False #use full dataset if no preprocessing
    df = pd.read_csv(dataset_metadata)
    print('No pre-processed CSV file found. Full dataset will be used.')
from collections import Counter 

word_frequency = Counter() #put word counts into variable
doc_woi_count = list() #initialize count of our word of interest

for document in constellate.dataset_reader(dataset_file): # iterate loop over all documents
    
    if use_filtered_list is True: #if there is some sort of filtering applied from preprocessing, use this filter here
        document_id = document['id'] # may be needed for future functionality
        if document_id not in filtered_id_list: 
            continue
        
    unigrams = document.get("unigramCount",[])

    ### ENTER WOI HERE ###
    word_of_interest = "money"
    ### ENTER WOI HERE ###
    doc_counter = 0
    if word_of_interest not in unigrams.keys():
        doc_woi_count.append(0)
    for gram, count in unigrams.items():
        if gram == word_of_interest: #add the specific count
            doc_woi_count.append(count)
            doc_counter += 1
        word_frequency[gram] += count #add the count to a running total count data dict for each word

######### THIS SECTION NEEDS WORK: DO NOT RUN TOMORROW UNLESS CERTAIN THIS IS WORKING! MAKE SURE THIS IS COMMENTED OUT #####
#    x = []
#    for gram, count in unigrams.items(): 
#        del x
#        x = re.search("^money",gram) #look for unigrams that start with the letters "money" in any case. perhaps there will be hyphenations but maybe not we shall see.
#        
####################################################################################################

    
print('Unigrams collected. Success!')
assert(len(doc_woi_count) == len(df)) #make sure that we got an equal number of counts for each doc to put into the .csv
print('Succesful count of word of interest!')

###########################################################################################
################ START CODING STUFF TO HANDLE THE DATA FRAME HERE #########################
##################################################################################

df_oi = pd.DataFrame()
df_oi['JournalTitle'] = df['title']
df_oi['publicationYear'] = df['publicationYear']
df_oi['wordCount'] = df['wordCount']
df_oi[str(word_of_interest)+'AggregateUse'] = doc_woi_count
filename = (str(word_of_interest)+'aggregateuse.xml')
df_oi.to_xml(filename)
