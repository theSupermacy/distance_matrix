import json
import MySQLdb
import requests

def check_key(destination,origin,key):
                _origins_="origins="+origin
                _destination="destinations="+str(destination)+","
                _parameter_=_origins_+"&"+_destination+"&"+key
                _url_final=_url_+_parameter_
                r=requests.get(_url_final)
                json_data=json.loads(r.text)
                if json_data['status']=="OVER_QUERY_LIMIT":
                    return 0
                else:
                    return 1


_url_="https://maps.googleapis.com/maps/api/distancematrix/json?"
key="AIzaSyC4Ik6E3p6krQxMUDT9WrFCiecANZwnFY0"
'''
        _origins_="origins="+str(_origins_latitude)+","+str(_origins_longitude)
        _destination="destinations="+str(_destination_latitude)+","+str(_destination_longitude)
        _parameter_=_origins_+"&"+_destination+"&"+key
        _url_final=_url_+_parameter_
        r=requests.get(_url_final)
        response_json=response.response_parser(r.text)
        '''


f=open('city.csv','r')
as1=f.read()

cities=as1.split('\r')


f.close();
host="localhost"
username=""
password=""
databdase=""
db = MySQLdb.connect(host,username,password,databdase )
cursor = db.cursor()
'''
i=0
for city in cities:
    if city == "Surat":
        break
    else:
        i=i+1
print i
'''
dub_city=cities
l=0;


if check_key(cities[0],cities[1],key):

    for origin in cities[32:]:
          _origins_="origins="+origin
          if l==1:
              break
          for destination in dub_city:
                if origin == destination:
                    pass
                else:
                    _destination="destinations="+str(destination)+","
                    _parameter_=_origins_+"&"+_destination+"&"+key
                    _url_final=_url_+_parameter_
                    try:
                        r=requests.get(_url_final)
                        json_data=json.loads(r.text)
                        dist= json_data['rows'][0]['elements'][0]['distance']['text']
                        cursor.execute("""INSERT INTO source_destination(idsource_destination,source,destination,distance) VALUES ('null',%s,%s,%s)""",(origin,destination,dist));
                        db.commit()
                    except KeyError:
                        pass
                    except :
                        pass
                    try:
                        print origin+destination+dist
                    except NameError:
                        print "Key expired"
                        l=1
                        break

else:
    print "Enter new Key"


