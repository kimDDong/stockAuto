import win32com.client
import pandas as pd
from datetime import datetime
import pytz

cpTopVol = win32com.client.Dispatch('CpSysDib.CpSvr7049')
cpStock = win32com.client.Dispatch('Dscbo1.StockMst')
objCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
KST = pytz.timezone('Asia/Seoul')
def get_top_etf(qty,qty2):
    """qty로 받은 종목에서 거래량 상위 qty2 종목들을 리턴한다."""
    try:
        cpTopVol.SetInputValue(0, '4')  # 시장 구분 "1":거래소, "2":코스닥, "4":전체(거래소+코스닥)
        cpTopVol.SetInputValue(1, 'V')  # 선택 구분 : "V":거래량상위, "A":거래대금상위
        cpTopVol.SetInputValue(2, 'Y')  # 관리 구분 :  "Y'', "N"
        cpTopVol.SetInputValue(3, 'Y')  # 우선주 구분 :  "Y'', "N"
        cpTopVol.BlockRequest()
        columns = ['code', '종목명', '현재가', '전일대비', '전일대비율', '거래량', '거래대금']
        index = []
        rows = []
        for i in range(qty):
            index.append(cpTopVol.GetDataValue(0, i))
            rows.append([cpTopVol.GetDataValue(1, i), cpTopVol.GetDataValue(2, i),
                         cpTopVol.GetDataValue(3, i), cpTopVol.GetDataValue(4, i),
                         cpTopVol.GetDataValue(5, i), cpTopVol.GetDataValue(6, i),
                         cpTopVol.GetDataValue(7, i)])
        df = pd.DataFrame(rows, columns=columns, index=index)
        df = df.head(qty)
        # df = df[~df['종목명'].str.contains("KODEX | KINDEX")]
        # df = df[~df['종목명'].str.contains("TIGER | 레버리지")]
        # df = df[~df['종목명'].str.contains("스팩")]
        # df = df[df['현재가'] >= 1000]
        # df = df[df['현재가'] <= 50000]
        df = df[df['전일대비율'] <= 10]
        df = df.sort_values(by=['거래량'], ascending=False).head(qty2)
        # df.to_csv(datetime.now(KST).strftime('%m_%d_%H%M') + "_top" + str(qty2) + ".csv", encoding='utf-8-sig')
        df_list = list(df['code'])

        codeList = objCodeMgr.GetStockListByMarket(1)  # 거래소
        codeList2 = objCodeMgr.GetStockListByMarket(2)  # 코스닥
        allCode = codeList + codeList2
        ETFList = []
        for code in allCode:
            stockKind = objCodeMgr.GetStockSectionKind(code)
            if  stockKind == 10 or stockKind == 12 :
                ETFList.append(code)
        etfTopList = [x for x in df_list if x not in ([x for x in (df_list+ETFList) if x not in ETFList])]
        # condition = (df.code == etfTopList[0])
        # print(df[condition].code)
        # print(df[condition].종목명)
        return etfTopList
    except Exception as ex:
        print('get_top_volume(qty) -> 에러 발생! ' + str(ex))
        return None


print(get_top_etf(300,300))
