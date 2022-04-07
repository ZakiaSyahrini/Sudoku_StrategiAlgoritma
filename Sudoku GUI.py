import tkinter as tr
import re


def ceksudoku(board):  # Cek data SUDOKU apakah valid untuk y dalam rentang (9)
    for y in range(9):
        for x in range(9):
            if board[y][x] > 9:
                return False

            if board[y][x] != 0 and board[y].count(board[y][x]) > 1:
                return False

            for col in range(9):
                if board[y][x] != 0 and col != y:
                    if board[col][x] == board[y][x]:
                        return False

            for i in range(3):
                for j in range(3):
                    if board[y][x] != 0 and (i+3*(y//3), j+3*(x//3)) != (y, x):
                        if board[i+3*(y//3)][j+3*(x//3)] == board[y][x]:
                            return False
    return True


def get_sudoku():  # Program UTAMA
    window = tr.Tk()
    window.title('Solve a Sudoku')
    window.geometry('600x450')

    width = 3
    # height = 1
    labels = []
    entrys = []
    sudoku = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    for i in range(81):
        entrys.append(tr.Entry(window, width=width))  # Inisialisasi data entry
        labels.append(tr.Label(window, width=3, height=1, bg='white'))  # Inisialisasi label
        print(i)

    l1 = tr.Label(window, text='**SUDOKU SOLVER**', bg='white', font=('Arial', 15))  # Judul
    l1.place(x='170', y='15')

    l2 = tr.Label(window, text='inputkan angka sudoku disini!', bg='yellow', font=('Arial', 11))  # Judul
    l2.place(x='174', y='43')
    
    b1 = tr.Button(window, text='Klik di sini!', bg='white', activebackground='orange', font=(
        'Arial', 12), command=lambda: get_data())   # Tombol "Jalankan"  
    b1.place(x='230', y='320')
    
    
    b2 = tr.Button(window, text='Clean up', bg='white', activebackground='orange', font=(
        'Arial', 12), command=lambda: bersihkan_data())   # Tombol "Hapus"
    b2.place(x='20', y='320')
    
    l0 = tr.Label(window, text='Data entry tidak valid!', font=('Arial', 20))  # kesalahan prompt

    for e in entrys:
        e.place(x=str(entrys.index(e) % 9*28+entrys.index(e)//3 % 3*6+20),
                y=str(entrys.index(e)//9*24+entrys.index(e)//27*6+70))  # GUI digunakan untuk membagi matriks Sudoku menjadi 9 kotak

    def get_data():  # Membaca nilai matriks Sudoku dan lakukan operasi
        for e in entrys:
            # Membaca data  entry, nomor yang tidak masuk akal atau spasi kosong dicatat sebagai 0
            sudoku[entrys.index(e)//9][entrys.index(e) % 9] = int(e.get()) if re.match('\d+', e.get()) else 0
        if ceksudoku(sudoku):  # Cek apakah data entry valid (apakah bentrok)
            data = sudoku  # Substitusi masukan Sudoku ke dalam algoritma untuk menghitung
            # Untuk setiap ruang di Sudoku, hitung kemungkinan nomor kandidatnya dan simpan di data_list; setiap kali ruang tersebut dikonfirmasi sebagai nilai unik, data_list yang tersisa perlu disegarkan lagi
            data_list = data_list_filter(data, buat_data_list(data), 0)
            # Hitung data baru Sudoku lengkap
            newdata = fill_num(data, data_list, 0)
            cetaksudoku(newdata)  # Keluaran Sudoku data baru
            l0.place(x='-350', y='-150')
            for l in labels:
                labels[labels.index(l)]['text'] = newdata[labels.index(
                    l)//9][labels.index(l) % 9]  # Mengganti nilai Sudoku lengkap ke dalam label
                l.place(x=str(labels.index(l) % 9*28+labels.index(l)//3 % 3*6+300),
                        y=str(labels.index(l)//9*24+labels.index(l)//27*6+70))  # Gunakan label untuk mengeluarkan Sudoku ke antarmuka GUI
        else:
            print('Error!, Periksa data tidak valid.')
            for l in labels:
                l.place(x='-100', y='-100')
            l0.place(x='310', y='160')

    def bersihkan_data():  # Kosongkan semua data entry
        for e in entrys:
            e.delete(0, 10)

    window.mainloop()


def cetaksudoku(data):  # Cetak hasil akhir sudoku
    for i in range(9):
        for j in range(9):
            print('{:^3}'.format(data[i][j]), end='')
        print('')
    print('')


# Inisialisasi, tidak membuat daftar nomor kandidat untuk setiap spasi data_list
def buat_data_list(data):
    data_list = []
    for y in range(9):
        for x in range(9):
            if data[y][x] == 0:
                data_list.append([(x, y), [1, 2, 3, 4, 5, 6, 7, 8, 9]])
    return data_list


def judge(data, x, y, num):  # Langkah Pertama, untuk menentukan apakah nomor tersebut diulang, apakah boleh diisi
    if data[y].count(num) > 0:  # Line
        # print('error1')
        return False

    for col in range(9):  # Kolom
        if data[col][x] == num:
            # print('error2')
            return False

    for a in range(3):  # Nilai Hasil Penentuan
        for b in range(3):
            if data[a+3*(y//3)][b+3*(x//3)] == num:
                # print('error3')
                return False
    return True


def data_list_filter(data, data_list, start):  # Refresh nomor kandidat
    for blank_index in range(start, len(data_list)):
        data_list[blank_index][1] = []
        for num in range(1, 10):
            if judge(data, data_list[blank_index][0][0], data_list[blank_index][0][1], num):
                data_list[blank_index][1].append(num)
    return data_list


# Langkah Kedua, dicoba secara berurutan pada posisi dengan beberapa nomor kandidat. Mirip dengan algoritme depth-first traversal(DFT), jika hasil angka pada posisi tertentu adalah True, tebakan posisi berikutnya diperbolehkan; jika posisi tertentu False, maka akan diabaikan.
def fill_num(data, data_list, start):
    if start < len(data_list):
        one = data_list[start]
        for num in one[1]:
            if judge(data, one[0][0], one[0][1], num):
                data[one[0][1]][one[0][0]] = num
                tem_data = fill_num(data, data_list, start+1)
                if tem_data != None:
                    return tem_data
        # Kemungkinan terjadi kesalahan sebelumnya setelah menebak beberapa langkah kemudian. Semua operasi penugasan dalam proses perlu dibersihkan.
        data[one[0][1]][one[0][0]] = 0
    else:
        return data


if __name__ == '__main__':
    try:
        get_sudoku()
    except:
        print('Error! Cek kembali data anda~')

