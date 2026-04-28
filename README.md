# Mini Project 1 - Image Restoration

## Identitas
- Nama: Faruq Awliya Labiib
- NRP: 5024241020

## Penjelasan Pipeline Restorasi
Pipeline pada program di [main.py](main.py) menggunakan kombinasi teknik denoising, sharpening, dan penyesuaian intensitas.

Urutan pipeline yang dipakai:
1. Median Filter (`median_filter`, kernel 7x7)
2. Gaussian Filter (`gauss_filter`, kernel 7x7, sigma 3)
3. Unsharp Mask (`unsharp_mask`)
4. Laplacian Sharpening (`laplacian_filter`)
5. Histogram Matching (`hist_match`) terhadap citra referensi

Alasan pemilihan teknik:
1. Median Filter dipilih untuk mereduksi noise salt-and-pepper 
2. Gaussian Filter dipakai untuk menghaluskan noise sisa secara lebih natural sebelum proses penajaman.
3. Unsharp Mask meningkatkan ketajaman detail lokal dengan menambahkan high-frequency component (mask) ke citra.
4. Laplacian Sharpening menonjolkan tepi dan struktur halus agar citra terlihat lebih jelas.
5. Histogram Matching dilakukan dengan membuat LUT dari citra target kemudian menerapkannya ke citra, sehingga kontras dan tonal range lebih mendekati referensi. Dipakai diakhir karena unsharp mask memberikan halo pada citra.

## Perbandingan Visual (Sebelum vs Sesudah)

### Sebelum (Noisy Input)
![Sebelum - Noisy](test_image_lena_noisy.png)

### Sesudah (Hasil Restorasi)
![Sesudah - Restorasi](hasil_proses.png)

## Analisis Singkat
Yang berhasil:
1. Noise pada citra berkurang signifikan setelah kombinasi median + gaussian filtering.
2. Detail tepi tampak lebih jelas setelah unsharp mask dan laplacian.
3. Kontras keseluruhan lebih mendekati citra acuan berkat histogram matching.

Yang bisa ditingkatkan:
1. Parameter kernel/sigma/amount masih statis, sehingga belum optimal untuk semua jenis noise.
2. Potensi over-sharpening pada area tertentu masih bisa muncul; perlu tuning adaptif.
3. Histogram matching saat ini dilakukan langsung pada array warna secara sederhana; kualitas warna bisa ditingkatkan dengan matching per channel yang lebih terkontrol atau pada ruang warna lain.

## Notes
>Citra masih jauh dari citra referensi dikarenakan noise yang terlalu banyak sehingga untuk menghilangkan keseluruhan noise akan menyebabkan gambar terlalu blur dan sulit untuk di sharpen. Saya telah mencoba pipeline serupa di Photoshop dan mendapat hasil yang serupa. 

## Cara Menjalankan Program
1. Pastikan Python 3 sudah terpasang.
2. (Opsional) Aktifkan virtual environment:

```powershell
 ".\\.venv\\Scripts\\Activate.ps1"
```

3. Install dependency:

```powershell
pip install opencv-python numpy matplotlib
```

4. Jalankan program:

```powershell
python main.py
```

5. Output hasil restorasi akan tersimpan sebagai:
- `hasil_proses.png`
