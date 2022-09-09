#############################################################################################
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Plib: Quantitative Research and Trading Library
# https://bitbucket.org/bamboos-consulting/plib/src/master/
#
# Copyright 2018-2022 Roberto Garrone
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#############################################################################################
# Kibot APIs 
#
# Module including functions to download data from Kibot
#############################################################################################      

UID=''
PWD=''

headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0",
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
   'Accept-Encoding': 'gzip, deflate',
   'Accept-Language': 'en-us,en;q=0.5',
   'Connection': 'keep-alive'}

##############################################
# End of Day Historical data
##############################################    
def klogin(uid='', pwd=''):
    import urllib.request
    url='http://api.kibot.com/?action=login&user='+uid+'&password='+pwd
    try:
        request=urllib.request.Request(url,None,headers) 
        response = urllib.request.urlopen(request)   
        UID=uid
        PWD=pwd
    except:
        print('Error logging in: check user id and password.')
    return response.read()
      
def kibot(symbol, sd='05-01-2017', ed='10-02-2017', regsess_only=False, ctype='stock', unadj=True, freq='daily', tz='America/New_York'):
    import requests
    from io import StringIO
    from pandas import read_csv,to_datetime
    import pytz
    
    if ctype not in ['stock','etf,'']:
        print('Error: invalid security type.')
        return pd.DataFrame()
    if freq not in ['daily','weekly,'yearly']:
        print('Error: invalid frequency.')
        return pd.DataFrame()
    if tz not in in pytz.all_timezones:
        print('Error: invalid timezone string.')
        return pd.DataFrame()  
    if regsess_only not in [True, False]:
        print('Error: invalid session flag.')
        return pd.DataFrame()  
    if unadj not in [True, False]:
        print('Error: invalid unadjusted flag.')
        return pd.DataFrame()  
                    
    endpoint='?action=history'
    url=root+endpoint+'&symbol='+symbol+'&interval='+freq+'&startdate='+sd+'&enddate='+ed+'&type='+str(ctype)      
    if regsess_only:
        url=url+'&regularsession=1'
    if unadj:
        url=url+'&unadjusted=1'
    req = requests.get(url+&user='+UID+'&password='+PWD, headers=headers)

    df=pd.read_csv(StringIO(req.text), header=None)
    if len(df)>1:
        df.columns=['Date','Open','High','Low','Close','Volume']
        df['Adjusted_close']=df['Close']
        df['Date'] = pd.to_datetime(df['Date'])
        df['Date'] = df['Date'].astype('datetime64[ns]')
        df['Date'] = df.Date.dt.tz_localize(ORIGIN_TZ).dt.tz_convert(tz)
        df=df.set_index('Date')
        df = df.asfreq('d')
        df=df[['Open','High','Low','Close','Adjusted_close','Volume']]
    return df.dropna()
