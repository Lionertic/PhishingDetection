from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
import pandas as pd
import joblib

def trainModel():
    df = pd.read_csv("data.csv")
    Y = df.pop("target")
    X = df
    model = selectAlgorithm(X,Y)
    joblib.dump(model,"model.pkl")


def addRow(encodedData):
    columnList = "has_ip,long_url,short_service,has_at,double_slash_redirect,pref_suf,has_sub_domain,ssl_state,long_domain,favicon,port,https_token,req_url,url_of_anchor,tag_links,SFH,submit_to_email,abnormal_url,redirect,mouseover,right_click,popup,iframe,domain_Age,dns_record,traffic,page_rank,google_index,links_to_page,stats_report,target".split(",")
    df = pd.read_csv("./data.csv")
    row = pd.DataFrame(encodedData,columns=columnList)
    df = df.append(row, ignore_index=True)
    df.to_csv("./data.csv", index=False)
    trainModel()
    return df.tail(1).index.item()

def editRow(feedback,pos):
    df = pd.read_csv("data.csv")
    df["target"].iloc[pos] = feedback
    df.to_csv("./data.csv", index=False)
    trainModel()

def selectAlgorithm(X,Y):
    regressor = RandomForestRegressor(n_estimators = 100, random_state = 4) 
    clf = SVC(kernel='linear') 
    gnb = GaussianNB()
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

    regressor.fit(X_train,Y_train)
    clf.fit(X_train,Y_train)
    gnb.fit(X_train,Y_train)

    rf_pred = regressor.predict(X_test)
    clf_pred = clf.predict(X_test)
    gnb_pred = gnb.predict(X_test)

    rf_pred[rf_pred <= 0 ] = -1
    rf_pred[rf_pred > 0 ] = 1

    clf_pred[clf_pred <= 0 ] = -1
    clf_pred[clf_pred > 0 ] = 1

    gnb_pred[gnb_pred <= 0 ] = -1
    gnb_pred[gnb_pred > 0 ] = 1

    predictions = [rf_pred,clf_pred,gnb_pred]

    perfect = -1
    accuracy = 0

    for i in range(len(predictions)):
        newAccuracy = (Y_test != predictions[i]).sum()
        if i == 0:
            perfect = i
            accuracy = newAccuracy
        else:
            if accuracy > newAccuracy:
                accuracy = newAccuracy
                perfect = i

    if perfect == 0 :
        regressor.fit(X, Y)
        return regressor
    elif perfect == 1:
        clf.fit(X,Y)
        return clf
    else:
        gnb.fit(X,Y)
        return gnb

