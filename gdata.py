from datetime import datetime as dt
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GS:
    def __init__(self):
        scope = ['https://spreadsheets.google.com/feeds']
        json_file_name = 'googlekey.json'
        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
        self.gc = gspread.authorize(credentials)
        self.spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1LitiLHdr-pqA5oRvMyJfdLr8Cqavaxwxfi0WKAcYz_s/edit#gid=0'

    def getGSMenu(self, target_date):
        # 스프레스시트 문서 가져오기
        doc = self.gc.open_by_url(self.spreadsheet_url)
        # 시트 선택하기
        worksheet = doc.worksheet('sheet1')
        data = worksheet.get_all_values()

        t_date = dt.strptime(target_date, "%Y-%m-%d")
        result_menu = ''
        for db_date, menu in data[1:]:
            d_date = dt.strptime(db_date, "%Y-%m-%d")
            if (t_date == d_date):
                result_menu = menu
                break
            if d_date > t_date:
                break
        if result_menu:
            result_menu = "\n".join(result_menu.split('#'))
            return result_menu
        else:
            return '등록된 식단이 아직 없습니다.' 


if __name__ == "__main__":
    gsheet = GS()
    print(gsheet.getGSMenu('2020-08-20'))