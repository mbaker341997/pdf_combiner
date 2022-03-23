import os

# Generates 10,000 files to load test the system on
PREFIX_1 = '1234567'
PREFIX_2 = '7654321'


def create_file(filename):
    with open(filename, 'w') as f:
        f.write('This perspective, however, did not receive mainstream recognition until after the seminal work of Milman Parry. Now most classicists agree that, whether or not there was ever such a composer as Homer, the poems attributed to him are to some degree dependent on oral tradition, a generations-old technique that was the collective inheritance of many singer-poets (or ἀοιδοί, aoidoi). An analysis of the structure and vocabulary of the Iliad and Odyssey shows that the poems contain many regular and repeated phrases; indeed, even entire verses are repeated. Thus according to the theory, the Iliad and Odyssey may have been products of oral-formulaic composition, composed on the spot by the poet using a collection of memorized traditional verses and phrases. Milman Parry and Albert Lord have pointed out that such elaborate oral tradition, foreign to today\'s literate cultures, is typical of epic poetry in an exclusively oral culture. The crucial words here are "oral" and "traditional". Parry starts with the former: the repetitive chunks of language, he says, were inherited by the singer-poet from his predecessors, and were useful to him in composition. Parry calls these chunks of repetitive language "formulas".[7] ')


directory_path = input("Enter directory path: ")
full_path = f'{directory_path}/mover_load'
if not os.path.exists(full_path):
    os.makedirs(full_path)
for x in range(5000):
    create_file(f'{full_path}/{PREFIX_1}.{x}.txt')
    create_file(f'{full_path}/{PREFIX_2}.{x}.txt')

