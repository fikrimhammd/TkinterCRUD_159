import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk

# Fungsi untuk membuat database dan tabel
def create_database():
    # Membuka koneksi ke database 'nilai_siswa.db'
    conn = sqlite3.connect('nilai_siswa.db')
    
    # Membuat cursor untuk mengeksekusi perintah SQL
    cursor = conn.cursor()
    
    # Mengeksekusi perintah SQL untuk membuat tabel 'nilai_siswa' jika belum ada
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    ''')
    
    # Menyimpan perubahan ke database
    conn.commit()
    
    # Menutup koneksi ke database
    conn.close()

# Fungsi untuk mengambil data dari database
def fetch_data():
    # Membuka koneksi ke database 'nilai_siswa.db'
    conn = sqlite3.connect('nilai_siswa.db')
    
    # Membuat cursor untuk mengeksekusi perintah SQL
    cursor = conn.cursor()
    
    # Mengeksekusi perintah SQL untuk mengambil semua data dari tabel 'nilai_siswa'
    cursor.execute("SELECT * FROM nilai_siswa")
    
    # Mengambil semua baris hasil eksekusi perintah SQL
    rows = cursor.fetchall()
    
    # Menutup koneksi ke database
    conn.close()
    
    # Mengembalikan hasil yang diambil dari database
    return rows

# Fungsi untuk menyimpan data ke dalam database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    # Membuka koneksi ke database 'nilai_siswa.db'
    conn = sqlite3.connect('nilai_siswa.db')
    
    # Membuat cursor untuk mengeksekusi perintah SQL
    cursor = conn.cursor()
    
    # Mengeksekusi perintah SQL untuk memasukkan data baru ke tabel 'nilai_siswa'
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))
    
    # Menyimpan perubahan ke database
    conn.commit()
    
    # Menutup koneksi ke database
    conn.close()

# Fungsi untuk memperbarui data dalam database
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    # Membuka koneksi ke database 'nilai_siswa.db'
    conn = sqlite3.connect('nilai_siswa.db')
    
    # Membuat cursor untuk mengeksekusi perintah SQL
    cursor = conn.cursor()
    
    # Mengeksekusi perintah SQL untuk memperbarui data di tabel 'nilai_siswa' berdasarkan id
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))
    
    # Menyimpan perubahan ke database
    conn.commit()
    
    # Menutup koneksi ke database
    conn.close()

# Fungsi untuk menghapus data dari database
def delete_database(record_id):
    # Membuka koneksi ke database 'nilai_siswa.db'
    conn = sqlite3.connect('nilai_siswa.db')
    
    # Membuat cursor untuk mengeksekusi perintah SQL
    cursor = conn.cursor()
    
    # Mengeksekusi perintah SQL untuk menghapus data dari tabel 'nilai_siswa' berdasarkan id
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))
    
    # Menyimpan perubahan ke database
    conn.commit()
    
    # Menutup koneksi ke database
    conn.close()

# Fungsi untuk menghitung prediksi fakultas
def calculate_prediction(biologi, fisika, inggris):
    # Memeriksa apakah nilai biologi lebih besar dari fisika dan inggris
    if biologi > fisika and biologi > inggris:
        # Mengembalikan string "Kedokteran" jika kondisi terpenuhi
        return "Kedokteran"
    # Memeriksa apakah nilai fisika lebih besar dari biologi dan inggris
    elif fisika > biologi and fisika > inggris:
        # Mengembalikan string "Teknik" jika kondisi terpenuhi
        return "Teknik"
    # Memeriksa apakah nilai inggris lebih besar dari biologi dan fisika
    elif inggris > biologi and inggris > fisika:
        # Mengembalikan string "Bahasa" jika kondisi terpenuhi
        return "Bahasa"
    else:
        # Mengembalikan string "Tidak Diketahui" jika tidak ada kondisi yang terpenuhi
        return "Tidak Diketahui"

# Fungsi untuk menangani pengiriman data (menambah data baru)
def submit():
    try:
        # Mengambil nilai dari input nama siswa
        nama = nama_var.get()
        # Mengambil dan mengkonversi nilai biologi ke integer
        biologi = int(biologi_var.get())
        # Mengambil dan mengkonversi nilai fisika ke integer
        fisika = int(fisika_var.get())
        # Mengambil dan mengkonversi nilai inggris ke integer
        inggris = int(inggris_var.get())

        # Memeriksa apakah nama siswa kosong
        if not nama:
            # Jika nama kosong, raise exception
            raise Exception("Nama siswa tidak boleh kosong.")

        # Menghitung prediksi fakultas berdasarkan nilai
        prediksi = calculate_prediction(biologi, fisika, inggris)
        # Menyimpan data ke database
        save_to_database(nama, biologi, fisika, inggris, prediksi)

        # Menampilkan pesan sukses dengan prediksi fakultas
        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
        # Mengosongkan input form
        clear_inputs()
        # Memperbarui tampilan tabel dengan data terbaru
        populate_table()
    except ValueError as e:
        # Menangkap error jika input tidak valid (misalnya bukan angka untuk nilai)
        messagebox.showerror("Error", f"Input tidak valid: {e}")

# Fungsi untuk memperbarui data yang sudah ada
def update():
    try:
        # Memeriksa apakah ada record yang dipilih
        if not selected_record_id.get():
            # Jika tidak ada, raise exception
            raise Exception("Pilih data dari tabel untuk di-update!")

        # Mengambil ID record yang dipilih dan mengkonversinya ke integer
        record_id = int(selected_record_id.get())
        # Mengambil nilai nama siswa dari input
        nama = nama_var.get()
        # Mengambil dan mengkonversi nilai biologi ke integer
        biologi = int(biologi_var.get())
        # Mengambil dan mengkonversi nilai fisika ke integer
        fisika = int(fisika_var.get())
        # Mengambil dan mengkonversi nilai inggris ke integer
        inggris = int(inggris_var.get())

        # Memeriksa apakah nama siswa kosong
        if not nama:
            # Jika kosong, raise ValueError
            raise ValueError("Nama siswa tidak boleh kosong.")

        # Menghitung prediksi fakultas berdasarkan nilai baru
        prediksi = calculate_prediction(biologi, fisika, inggris)
        # Memperbarui data di database
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)

        # Menampilkan pesan sukses
        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
        # Mengosongkan input form
        clear_inputs()
        # Memperbarui tampilan tabel dengan data terbaru
        populate_table()
    except ValueError as e:
        # Menangkap dan menampilkan pesan error jika terjadi ValueError
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk menghapus data
def delete():
    try:
        # Memeriksa apakah ada record yang dipilih
        if not selected_record_id.get():
            # Jika tidak ada, raise exception
            raise Exception("Pilih data dari tabel untuk dihapus!")

        # Mengambil ID record yang dipilih dan mengkonversinya ke integer
        record_id = int(selected_record_id.get())
        # Memanggil fungsi untuk menghapus data dari database
        delete_database(record_id)
        # Menampilkan pesan sukses
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
        # Mengosongkan input form
        clear_inputs()
        # Memperbarui tampilan tabel dengan data terbaru
        populate_table()
    except ValueError as e:
        # Menangkap dan menampilkan pesan error jika terjadi ValueError
        messagebox.showerror("Error", f"Kesalahan: {e}")
# Fungsi untuk menghapus input form
def clear_inputs():
    # Mengosongkan input nama siswa
    nama_var.set("")
    # Mengosongkan input nilai biologi
    biologi_var.set("")
    # Mengosongkan input nilai fisika
    fisika_var.set("")
    # Mengosongkan input nilai inggris
    inggris_var.set("")
    # Mengosongkan ID record yang dipilih
    selected_record_id.set("")

# Fungsi untuk mengisi ulang data ke dalam tabel
def populate_table():
    # Menghapus semua baris yang ada di tabel
    for row in tree.get_children():
        tree.delete(row)
    # Mengambil data baru dari database dan memasukkannya ke dalam tabel
    for row in fetch_data():
        # Memasukkan setiap baris data ke dalam tabel
        tree.insert('', 'end', values=row)

# Fungsi untuk mengisi input dari data yang dipilih di tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]
        selected_row = tree.item(selected_item)['values']

        selected_record_id.set(selected_row[0])
        nama_var.set(selected_row[1])
        biologi_var.set(selected_row[2])
        fisika_var.set(selected_row[3])
        inggris_var.set(selected_row[4])
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid!")

# Inisialisasi database
create_database()

# Membuat GUI dengan tkinter
root = Tk()
root.title("Prediksi Fakultas Siswa")

# Variabel tkinter
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()  # Untuk menyimpan ID record yang dipilih

Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)

# Tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
tree = ttk.Treeview(root, columns=columns, show='headings')

# Mengatur posisi isi tabel di tengah
for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, anchor='center') 

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

tree.bind('<ButtonRelease-1>', fill_inputs_from_table)

populate_table() # Fungsi ini dipanggil untuk mengisi atau memperbarui tabel (treeview) dengan data yang sesuai.

root.mainloop() # Memulai loop utama aplikasi tkinter.