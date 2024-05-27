import argparse
import requests
import time
import os
import shutil

def LPR_request(date,road, value, real_count, ex1, plate_7, plate_0to6, plate_8to9, plate_trash):

    default_path = f'R:/seatbelt/highway_send_data/{road}'
 
    # 타조아이 LPR 연결 후
    url = 'http://192.168.0.77:8082/lpr'
    path_in = os.path.join(default_path, date + '_base64')  # base64 data 있는 곳

    base64_list = os.listdir(path_in)  # 파일 목록

    for i in base64_list[value:]:
        ex1 = ex1 + 1
        if ex1 > 10:
            time.sleep(0.8)
            ex1 = 0
        real_count = real_count + 1
        print('현재 번호는: ' + str(real_count))
        print('현재 값은: ' + str(i))
        file = open(path_in + '\\' + i, 'rb')  # 데이터 열어서
        upload = {
            'name': 'ysw',
            'imgBuffer': file,
        }
        try:
            res = requests.post(url, data=upload)  # 서버에 요청
            out = res.text  # 번호판 결과 나옴
        except requests.exceptions.ConnectionError as e:
            print('Connection Error:', e)
            print('Sleeping for 10 seconds...')
            time.sleep(10)
            # 업데이트된 값으로 LPR_request를 재귀적으로 호출
            LPR_request(date, road, real_count-1, real_count-1, ex1-1, plate_7, plate_0to6, plate_8to9, plate_trash)
            return
        except requests.exceptions.RequestException as e:
            print('Request Exception:', e)
            # RequestException에 대한 예외처리
            return

        if out.startswith('7'):
            plate_7.append(i)  # 7로 시작하면 파일이름 저장
            print('plate number 7: ' + str(len(plate_7)))
        elif out.startswith('8') or out.startswith('9'):
            plate_8to9.append(i)
            print('plate number 8to9: ' + str(len(plate_8to9)))
        elif (
            out.startswith('0')
            or out.startswith('1')
            or out.startswith('2')
            or out.startswith('3')
            or out.startswith('4')
            or out.startswith('5')
            or out.startswith('6')
        ):
            plate_0to6.append(i)
            print('plate number 0to6: ' + str(len(plate_0to6)))
        else:
            plate_trash.append(i)
            print('plate number trash: ' + str(len(plate_trash)))

        c_count = sum("_c_" in filename for filename in base64_list)
        
        if real_count >= c_count:
            break

    plate_path = os.path.join(path_in, f'{date}_plate')
    
    os.makedirs(plate_path, exist_ok= True)
    
    # 마지막 변수를 파일에 저장
    with open(plate_path + '/' + f'{date}_request_result.txt', 'w') as f:
        f.write(f'date: {date}\n')
        f.write(f'total real count: {real_count}\n')
        f.write(f'total plate 0 to 6 count: {len(plate_0to6)}\n')
        f.write(f'total plate 7 count: {len(plate_7)}\n')
        f.write(f'total plate 8 to 9 count: {len(plate_8to9)}\n')
        f.write(f'total plate trash: {len(plate_trash)}\n')

    # 7번 변수 리스트를 파일에 저장
    with open(plate_path + '/' + f'{date}_plate_7.txt', 'w') as f:
        plate_7_string = '\n'.join(plate_7)
        f.write(f'{plate_7_string}')

    # 0to6번 변수 리스트를 파일에 저장
    with open(plate_path + '/' + f'{date}_plate_0to6.txt', 'w') as f:
        plate_0to6_string = '\n'.join(plate_0to6)
        f.write(f'{plate_0to6_string}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--date', type=str, help='Specify the date')
    parser.add_argument('-r', '--road', type=str, default = 'dp' ,help='Specify the road')
    parser.add_argument('-v', '--value', type=int, default=0, help='Specify the value')
    parser.add_argument('-rt', '--real_count', type=int, default=0, help='Add c7ounts')
    parser.add_argument('-ex', '--ex1', type=int, default=0, help='Add number to sleep')
    args = parser.parse_args()

    plate_7 = []
    plate_0to6 = []
    plate_8to9 = []
    plate_trash = []

    LPR_request(args.date,args.road, args.value, args.real_count, args.ex1, plate_7, plate_0to6, plate_8to9, plate_trash)