import json
import MySQLdb
import requests
import math
def check_key(destination,origin,key):
                print(destination)
                _origins_="origins="+str(origin)
                _destination="destinations="+str(destination)+","
                _parameter_=str(_origins_)+"&"+_destination+"&"+key
                _url_final=_url_+_parameter_
                r=requests.get(_url_final)
                json_data=json.loads(r.text)
                print json_data
                if json_data['status']=="OVER_QUERY_LIMIT":
                    return 0
                else:
                    return 1
def file_write(filename,message1,message2='null'):
    f=open(filename,'a')
    message=message1+"   "+message2+'\n';
    f.write(message)
    f.close()
def read_file(filename):
    with open(filename) as f:
        content = f.readlines()
    return content
def enter_table():
    global l,key
    flag=0
    print cities[0]
    current_key = key[l]
    print current_key
    if check_key(cities[0],cities[1],key[l]):
        try:
            content=read_file('start_point')
            str_content=str(content[-1])
            print(str_content)
            if content:
                point=str_content.split('   ')
                start_point=int(point[0])
                end_point=int(point[1])
            else:
                start_point=0
                end_point=0
        except ValueError:
            start_point=0
            end_point=0
        except IndexError:
            start_point=0
            end_point=0
        for i in range(start_point,len(cities)-1):
              _origins_="origins="+cities[i]
              if flag==1:
                  break
              for j in range(end_point,len(cities)-1):
                    if cities[i] == cities[j] :
                        pass
                    else:
                        _destination="destinations="+str(cities[j])+","
                        _parameter_=_origins_+"&"+_destination+"&"+current_key
                        _url_final=_url_+_parameter_
                        try:
                            r=requests.get(_url_final)
                            json_data=json.loads(r.text)
                            if json_data['status']=="OVER_QUERY_LIMIT":
                                print "Key expired at "+" "+str(cities[i])+" "+cities[j]
                                try:
                                        current_key=key[l+1]
                                except :
                                    file_write("start_point",str(i),str(j))
                                    flag=1
                                    break
                                file_write('error.txt',str(l),'key expired')
                            dist= json_data['rows'][0]['elements'][0]['distance']['text']
                            cursor.execute("""INSERT INTO source_destination(idsource_destination,source,destination,distance) VALUES ('null',%s,%s,%s)""",(cities[i],cities[j],dist));
                            db.commit()
                        except KeyError:
                            file_write('error.txt',cities[i],cities[j])
                            pass
                        except :
                            pass
                        print cities[i]+" "+cities[j]+" "+dist


    else:
        try:
            print l,current_key
            l=l+1
            current_key=current_key[l+1]
            enter_table()
        except:
             return -1





_url_="https://maps.googleapis.com/maps/api/distancematrix/json?"
key=["AIzaSyC4Ik6E3p6krQxMUDT9WrFCiecANZwnFY0","AIzaSyAbEdVw_tLZOpMLWs9IvgS7WkbeC3P7Adw"]
f=open('city.csv','r')
as1=f.read()
cities=as1.split('\r')
n=len(cities)
total=(n*n-1)/2-n;
total_keys=math.ceil(float(total)/2400);
f.close()
i=0
host="localhost"
username="root"
password="rahulsinha"
databdase="distance"
db = MySQLdb.connect(host,username,password,databdase)
cursor = db.cursor()
l=0
current_key = key[l]
enter_table()