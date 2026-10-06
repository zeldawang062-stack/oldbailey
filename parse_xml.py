import xml.etree.ElementTree as ET
import pandas as pd

def parse_xml(path):
    tree = ET.parse(path)
    root = tree.getroot()

    defendant = []
    for person in root.iter("persName"):
        if person.get("type") == "defendantName":
            record = {}
            given = None
            surname = None
            gender = None
            age = None
            id = person.get("id")
            record["id"] = id
            for element in person.iter("interp"):
                if element.get("type") == "gender": 
                    gender = element.get("value")
                if element.get("type") =="age":
                    age = element.get("value")
                if element.get("type") =="given":
                    given = element.get("value")
                if element.get("type") =="surname":
                    surname =  element.get("value")
            record["gender"] =gender
            record["age"] = age
            record["given"] = given
            record ["surname"] =surname
            defendant.append(record)

    df_defendant = pd.DataFrame(defendant)

    offences = []
    for offence in root.iter("rs"):
        if offence.get("type") == "offenceDescription":
            off = {}
            id = None
            offenceCat = None
            offenceSubCat = None
            id = offence.get("id")
            off["id"] = id
            for element in offence.iter("interp"):
                if element.get("type") == "offenceCategory": 
                    offenceCat= element.get("value")
                if element.get("type") =="offenceSubcategory":
                    offenceSubCat = element.get("value")
            off["offenceCategory"] = offenceCat
            off["offenceSubCategory"] = offenceSubCat
            offences.append(off)

    df_offences = pd.DataFrame(offences)

    verdicts =[]
    for verdict in root.iter("rs"):
        if verdict.get("type") =="verdictDescription":
            ver = {}
            verdictCat = None
            verdictSubCat = None
            id = None
            id = verdict.get("id")
            ver["id"] = id
            for element in verdict.iter("interp"):
                if element.get("type") == "verdictCategory":
                    verdictCat = element.get("value")
                if element.get("type") == "verdictSubcategory":
                    verdictSubCat = element.get("value")
            ver["verdictCategory"] = verdictCat
            ver["verdictSubcategory"] = verdictSubCat
            verdicts.append(ver)

    df_verdicts = pd.DataFrame(verdicts)

    punishments = []
    for punishment in root.iter("rs"):
        if punishment.get("type") == "punishmentDescription":
            pun = {}
            punishmentCat = None
            punishmentSubCat = None
            id = None
            id = punishment.get("id")
            pun["id"] = id
            for element in punishment.iter("interp"):
                if element.get("type") == "punishmentCategory":
                    punishmentCat = element.get("value")
                if element.get("type") == "punishmentSubcategory":
                    punishmentSubCat = element.get("value")
            pun["punishmentCat"] = punishmentCat
            pun["punishmentSubCat"] =  punishmentSubCat
            punishments.append(pun)
    df_punishments = pd.DataFrame(punishments)

    charge = []
    for trial in root.iter("div1"):
        if trial.get("type") == "trialAccount":
            for element in trial.iter("join"):
                if element.get("result") == "criminalCharge":
                    char = {}
                    targOrder = None
                    targets = None
                    charge_id = element.get("id")
                    targOrder =element.get("targOrder")
                    targets = element.get("targets").split (" ")
                    char["charge_id"] = charge_id
                    char["targOrder"] = targOrder
                    char["defendant_id"] = targets[0]
                    char["offence_id"] = targets[1]
                    char["verdict_id"] = targets[2]
                    charge.append(char)

    df_charge = pd.DataFrame(charge)


    defpunish = []
    for punish in root.iter("join"):
        if punish.get("result") == "defendantPunishment":
            defpun = {}
            targOrder = None
            targets = None
            result = punish.get("result")
            targOrder =punish.get("targOrder")
            targets = punish.get("targets").split (" ")
            defpun["result"] = result
            defpun["targOrder"] = targOrder
            defpun["defendant_id"] = targets[0]
            defpun["punishment_id"] = targets[1]
            defpunish.append(defpun)
    df_defpunish = pd.DataFrame(defpunish)

    return df_defendant, df_offences, df_verdicts, df_punishments, df_charge, df_defpunish

