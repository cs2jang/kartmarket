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
        for db_date, _, menu in data[1:]:
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

    def setExceptPeople(self, number):
        target_date=dt.now().strftime("%Y-%m-%d %H:%M:%S")
        if int(target_date[11:13]) > 9:
            result_string = '제외 가능 신청 시간이 지났습니다.'
            return result_string

        doc = self.gc.open_by_url(self.spreadsheet_url)
        # 시트 선택하기
        worksheet = doc.worksheet('sheet1')
        data = worksheet.get_all_values()
        result_string = ''
        t_date = dt.strptime(target_date[0:10], "%Y-%m-%d")
        for idx, (db_date, except_num, _) in enumerate(data[1:]):
            d_date = dt.strptime(db_date, "%Y-%m-%d")
            if (t_date == d_date):
                if except_num:
                    result_num = int(except_num) + number
                else:
                    result_num = number
                cell_num = idx + 2
                worksheet.update_acell('B{0}'.format(cell_num), result_num)
                result_string = target_date + ' {0}명 접수 되었습니다.'.format(number)
                break
            if d_date > t_date:
                result_string = '등록된 식단이 아직 없습니다. 식당으로 직접 문의해 주세요' 
                break
        return result_string

    def getExceptPeople(self, target_date=dt.now().strftime("%Y-%m-%d")):
        # 스프레스시트 문서 가져오기
        doc = self.gc.open_by_url(self.spreadsheet_url)
        # 시트 선택하기
        worksheet = doc.worksheet('sheet1')
        data = worksheet.get_all_values()

        t_date = dt.strptime(target_date, "%Y-%m-%d")
        result_num = '등록된 식단이 아직 없어, 제외신청을 못 받았습니다.'
        for db_date, except_num, _ in data[1:]:
            d_date = dt.strptime(db_date, "%Y-%m-%d")
            if (t_date == d_date):
                result_num = '현재, {0}명 입니다.'.format(except_num) 
                break
            if d_date > t_date:
                break
            
        return result_num 

if __name__ == "__main__":
    gsheet = GS()
    print(gsheet.setExceptPeople(5))