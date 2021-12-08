import glob
import pandas as pd
import pymongo
import time


def datawarehouse1(subject):
    start_time = time.time()
    client = pymongo.MongoClient()
    db = "vveille_scientifique_" + subject
    vs = client[db]
    Cjournal = vs['journal']
    Cauthor = vs['author']
    CDate = vs['date']
    Ctitle = vs['title']
    Cabstract = vs['abstract']
    Caffiliation = vs['affiliation']
    Cmesh = vs['mesh']
    Carticle = vs['article']
    aaa = ""

    bbb = ""
    aa = 0
    bb = 0
    cc = 0
    dd = 0
    directoryPath = "C:/Users/lenevo/Downloads/veille/"
    filetxt = glob.glob(directoryPath + '*.txt')
    #  if len(filetxt)!=0:
    for q in range(len(filetxt)):
        f = open(filetxt[q], "r", encoding='utf-8')
        Lines = f.readlines()
        list1 = ["PMID-", "DP  -", "TI  -", "LID -", "FAU -", "AD  -", "JT  -", "MH  -"]
        list2 = ["PG  -", "LID -", "FAU -", "AU  -", "AD  -", "LA  -", "PT  -", "DEP -", "TA  -", "JT  -", "JID -",
                 "SB  -", "MH  -", "CI  -"]
        authnumber = 0
        meshnumber = 0
        affnumber = 0
        mhnumber = 0
        tous = {}
        tous['FK_abstract'] = ""
        tous['FK_title'] = ""
        tous['FK_date'] = ""
        tous['FK_journal'] = ""
        tous['doi'] = ""
        for i in range(0, len(Lines)):

            iterr = "p" + str(i)
            line = Lines[i]
            if "PMID-" in line:

                authnumber = 0
                meshnumber = 0
                affnumber = 0
                mhnumber = 0
                if all(value != "" for value in tous.values()):
                    FKabstract = tous['FK_abstract']
                    FKtitle = tous['FK_title']
                    FKdate = tous['FK_date']
                    FKjournal = tous['FK_journal']
                    FKDOI = tous['doi']
                    insert_article = {'doi': FKDOI, 'FK_date': FKdate, 'FK_title': FKtitle,
                                      ' FK_abstract': FKabstract, 'FK_J': FKjournal}
                    for k, v in tous.items():
                        if 'author' in k:
                            insert_article['FK_auth'] = v
                        if 'aff' in k:
                            bb += 1
                            bbb = 'g' + str(bb)
                            insert_article['FK_aff'] = v
                            insert_article['_id'] = bbb
                            Carticle.insert_one(insert_article)
                    tous = {}
                    tous['FK_abstract'] = ""
                    tous['FK_title'] = ""
                    tous['FK_date'] = ""
                    tous['FK_journal'] = ""
                    tous['doi'] = ""

                insert_abstract = {}
                insert_title = {}
                insert_date = {}
                insert_journal = {}
                insert_author = {}
                insert_aff = {}
                insert_article = {}
                pmid = line.split("-", 1)
            if "DP  -" in line:
                DP = line.split("-", 1)
                insert_date = {'datepub': DP[1]}
                id_date = CDate.insert_one(insert_date).inserted_id
                tous['FK_date'] = id_date
            if "MH  -" in line:
                meshnumber += 1
                mh = line.split("-", 1)
                insert_mh = {'mesh': mh[1]}
                id_mesh = Cmesh.insert_one(insert_mh).inserted_id
                meesh = 'mesh' + str(mhnumber)
                tous[meesh] = id_mesh

            if "LID -" in line and "[doi]" in line:
                LID = line.split("-", 1)
                tous['doi'] = LID[1]
            if "JT  -" in line:
                JT = line.split("-", 1)
                insert_journal = {'journal': JT[1]}
                id_journal = Cjournal.insert_one(insert_journal).inserted_id
                tous['FK_journal'] = id_journal
            if "TI  -" in line:
                Ti = line.split("-", 1)
                titre = Ti[1]
                next_line = Lines[i + 1]
                k = 1
                j = list2[0]
                m = list2[1]
                while j not in next_line:
                    if m in next_line:
                        break
                    k = k + 1
                    titre = titre + next_line
                    next_line = Lines[i + k]
                insert_title = {'title': titre}
                id_title = Ctitle.insert_one(insert_title).inserted_id
                tous['FK_title'] = id_title

            if "FAU -" in line:
                authnumber += 1
                fau = line.split("-", 1)
                insert_author['name'] = fau[1]
                aa += 1
                aaa = 'p' + str(aa)
                insert_author['_id'] = aaa
                id_author = Cauthor.insert_one(insert_author).inserted_id
                author = 'author' + str(authnumber)
                tous[author] = id_author

            if "AD  -" in line:
                affnumber += 1
                ad = line.split("-", 1)
                adress = ad[1]
                next_line = Lines[i + 1]
                k = 1
                w = list2[2]
                z = list2[5]
                p = list2[4]
                while w not in next_line:
                    if z in next_line:
                        break
                    if p in next_line:
                        break
                    k = k + 1
                    adress = adress + next_line
                    next_line = Lines[i + k]

                for o in range(1, k):
                    continue
                insert_aff = {'address': adress}
                id_aff = Caffiliation.insert_one(insert_aff).inserted_id
                aff = 'aff' + str(affnumber)
                tous[aff] = id_aff
            if "AB  -" in line:
                ab = line.split("-", 1)
                abstract = ab[1]
                next_line = Lines[i + 1]
                k = 1
                w = list2[2]
                z = list2[13]
                while z not in next_line:
                    if w in next_line:
                        break
                    k = k + 1
                    abstract = abstract + next_line
                    next_line = Lines[i + k]
                insert_abstract = {'abstract': abstract}
                id_abstract = Cabstract.insert_one(insert_abstract).inserted_id
                tous['FK_abstract'] = id_abstract
datawarehouse1("covid")