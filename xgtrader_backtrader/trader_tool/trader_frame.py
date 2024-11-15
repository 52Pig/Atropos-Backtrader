from qmt_trader.qmt_trader_ths import qmt_trader_ths
from xgtrader.xgtrader import xgtrader
class trader_frame:
    def __init__(self,trader_tool='ths',exe='C:/同花顺软件/同花顺/xiadan.exe',tesseract_cmd='C:/Program Files/Tesseract-OCR/tesseract',
                qq='1029762153@qq.com',open_set='否',qmt_path='D:/国金QMT交易端模拟/userdata_mini',
                qmt_account='55009640',qmt_account_type='STOCK'):
        self.exe=exe
        self.tesseract_cmd=tesseract_cmd
        self.qq=qq
        self.trader_tool=trader_tool
        self.open_set=open_set
        self.qmt_path=qmt_path
        self.qmt_account=qmt_account
        self.qmt_account_type=qmt_account_type
    def get_trader_frame(self):
        if self.trader_tool=='ths':
            self.trader=xgtrader(exe=self.exe,tesseract_cmd=self.tesseract_cmd,open_set=self.open_set)
            return self.trader
        else:
            self.trader=qmt_trader_ths(path=self.qmt_path,account=self.qmt_account,account_type=self.qmt_account_type)
            return self.trader
