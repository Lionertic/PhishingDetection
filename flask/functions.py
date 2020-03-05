from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import joblib

def trainModel():
    regressor = RandomForestRegressor(n_estimators = 100, random_state = 4) 
    df = pd.read_csv("data.csv")
    X = df.drop("target",axis=1)
    Y = df.target.values
    regressor.fit(X, Y)
    joblib.dump(regressor,"model.pkl")

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