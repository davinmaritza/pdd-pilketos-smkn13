import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(40, 810, "SOP DESAIN & KONTEN VISUAL PDD — PRAJA SATYA NAYAKA (SMKN 13 BANDUNG)")
            self.setStrokeColor(colors.HexColor("#D4AF37"))
            self.setLineWidth(1)
            self.line(40, 804, 555, 804)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(40, 36, 555, 36)
        
        self.drawString(40, 24, "Divisi Publikasi, Dekorasi & Dokumentasi (PDD) — MPK SMKN 13 Bandung")
        page_str = f"Halaman {self._pageNumber} dari {page_count}"
        self.drawRightString(555, 24, page_str)
        self.restoreState()

def build_pdf(filename="SOP_Desain_PDD.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#0D1B2A")   # Midnight Navy
    gold_color = colors.HexColor("#D4AF37")      # Imperial Gold
    text_color = colors.HexColor("#1E293B")      # Slate Dark
    muted_color = colors.HexColor("#64748B")     # Slate Muted

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=primary_color,
        alignment=0,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=gold_color,
        alignment=0,
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=text_color,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=4
    )

    meta_style = ParagraphStyle(
        'Meta_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=muted_color
    )

    meta_bold = ParagraphStyle(
        'Meta_Bold',
        parent=meta_style,
        fontName='Helvetica-Bold',
        textColor=primary_color
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=text_color
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell,
        fontName='Helvetica-Bold',
        textColor=primary_color
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    story = []

    # --- COVER HEADER ---
    story.append(Paragraph("STANDAR OPERASIONAL PROSEDUR (SOP) DESAIN GRAFIS & KONTEN MULTIMEDIA", title_style))
    story.append(Paragraph("DIVISI PDD — PILKETOS SMKN 13 BANDUNG | TEMA: PRAJA SATYA NAYAKA", subtitle_style))

    # Metadata Box
    meta_data = [
        [
            Paragraph("<b>Nomor Dokumen:</b> SOP-PDD/PLK13/2026/001", meta_style),
            Paragraph("<b>Versi:</b> 2.0 (Professional Agency Standard)", meta_style)
        ],
        [
            Paragraph("<b>Penyusun:</b> Davin Maritza (Koordinator PDD)", meta_style),
            Paragraph("<b>Target Pengguna:</b> Desainer Feed/Story, Videografer, Tim Cetak", meta_style)
        ],
        [
            Paragraph("<b>Tanggal Berlaku:</b> 17 Oktober 2026", meta_style),
            Paragraph("<b>Status:</b> Wajib Dipatuhi Seluruh Anggota Divisi", meta_bold)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[260, 255])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E2E8F0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 12))

    # --- BAB 1: FILOSOFI & ARAH VISUAL TEMA ---
    story.append(Paragraph("BAB I. FILOSOFI TEMA & ARAH VISUAL (*CREATIVE DIRECTION*)", h1_style))
    story.append(Paragraph(
        "Seluruh aset grafis PILKETOS 2026 wajib mencerminkan identitas resmi bertema <b>'PRAJA SATYA NAYAKA'</b>. "
        "Desain tidak boleh hanya sekadar estetis, melainkan harus menyampaikan pesan kepemimpinan yang berwibawa, adil, dan transparan.",
        body_style
    ))
    
    story.append(Paragraph("<b>1. Tiga Pilar Filosofi:</b>", h2_style))
    story.append(Paragraph("• <b>PRAJA (Rakyat / Warga Sekolah):</b> Desain bersifat inklusif, ramah dibaca, dan memprioritaskan penyampaian aspirasi seluruh siswa SMKN 13.", bullet_style))
    story.append(Paragraph("• <b>SATYA (Kebenaran / Integritas):</b> Teks data visi-misi, tata cara, dan hasil perhitungan disajikan transparan, faktual, tanpa manipulasi.", bullet_style))
    story.append(Paragraph("• <b>NAYAKA (Pemimpin Bijaksana):</b> Nuansa visual agung, percaya diri, dan berwibawa dengan layout bersih (*clean modern*).", bullet_style))

    story.append(Paragraph("<b>2. Anti-Patterns (Larangan Mutlak Desain):</b>", h2_style))
    story.append(Paragraph("❌ <b>DILARANG</b> menggunakan gradasi pelangi acak atau efek warna neon yang menyilaukan mata.", bullet_style))
    story.append(Paragraph("❌ <b>DILARANG</b> memakai efek <i>drop shadow</i> hitam pekat tebal tanpa blur (memberikan kesan desain amatir/slop).", bullet_style))
    story.append(Paragraph("❌ <b>DILARANG</b> menumpuk teks di atas foto yang ramai tanpa lapisan overlay kartu peredam (*card container*).", bullet_style))
    story.append(Paragraph("❌ <b>DILARANG</b> menggunakan font dekoratif tulisan tangan (*script/brush*), Comic Sans, atau graffiti pada teks informasi resmi.", bullet_style))

    story.append(Spacer(1, 8))

    # --- BAB 2: SISTEM WARNA ---
    story.append(Paragraph("BAB II. SISTEM WARNA RESMI & ATURAN 60-30-10", h1_style))
    story.append(Paragraph(
        "Kepatuhan palet warna adalah hukum mutlak agar seluruh materi publikasi memiliki kesatuan visual (*brand consistency*). "
        "Penerapan warna wajib mengikuti rasio harmoni <b>60% Dominan, 30% Sekunder, dan 10% Aksen</b>:",
        body_style
    ))

    color_table_data = [
        [
            Paragraph("Role & Proporsi", table_header),
            Paragraph("Nama Warna", table_header),
            Paragraph("HEX Code", table_header),
            Paragraph("RGB / CMYK", table_header),
            Paragraph("Fungsi & Aturan Penggunaan", table_header)
        ],
        [
            Paragraph("<b>Dominan (60%)</b>", table_cell_bold),
            Paragraph("Midnight Navy", table_cell),
            Paragraph("<code>#0D1B2A</code>", table_cell),
            Paragraph("13, 27, 42<br/>C:69 M:36 Y:0 K:84", table_cell),
            Paragraph("Latar belakang utama kanvas, header dokumen, teks heading di kartu terang. Memberikan kesan kokoh dan wibawa.", table_cell)
        ],
        [
            Paragraph("<b>Sekunder (30%)</b>", table_cell_bold),
            Paragraph("Pure White", table_cell),
            Paragraph("<code>#FFFFFF</code>", table_cell),
            Paragraph("255, 255, 255<br/>C:0 M:0 Y:0 K:0", table_cell),
            Paragraph("Kontainer kartu, latar belakang teks panjang, tipografi di atas bidang gelap. Wajib menjaga keterbacaan tinggi.", table_cell)
        ],
        [
            Paragraph("<b>Aksen (10%)</b>", table_cell_bold),
            Paragraph("Imperial Gold", table_cell),
            Paragraph("<code>#D4AF37</code>", table_cell),
            Paragraph("212, 175, 55<br/>C:0 M:17 Y:74 K:17", table_cell),
            Paragraph("Nomor urut paslon, badge kategori, tombol CTA, garis pemisah halus. <b>Dilarang</b> dipakai sebagai warna background penuh.", table_cell)
        ],
        [
            Paragraph("<b>Supporting</b>", table_cell),
            Paragraph("Slate Neutral", table_cell),
            Paragraph("<code>#64748B</code>", table_cell),
            Paragraph("100, 116, 139<br/>C:28 M:17 Y:0 K:45", table_cell),
            Paragraph("Garis batas pembatas (*border*), teks catatan kaki (*caption*), dan metadata pendukung.", table_cell)
        ]
    ]

    t_color = Table(color_table_data, colWidths=[80, 85, 70, 95, 185])
    t_color.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_color)
    story.append(Spacer(1, 14))

    # --- BAB 3: TIPOGRAFI ---
    story.append(Paragraph("BAB III. STANDAR TIPOGRAFI & HIERARKI TEKS", h1_style))
    story.append(Paragraph(
        "Kombinasi font resmi yang diizinkan hanya 2 keluarga font (*font families*). "
        "Dilarang menambahkan jenis font lain di luar ketentuan berikut:",
        body_style
    ))

    typo_data = [
        [
            Paragraph("Kategori Font", table_header),
            Paragraph("Font Family Resmi", table_header),
            Paragraph("Weight / Gaya", table_header),
            Paragraph("Penggunaan Khusus", table_header)
        ],
        [
            Paragraph("<b>Display / Title</b>", table_cell_bold),
            Paragraph("League Spartan", table_cell),
            Paragraph("Bold, ExtraBold, Black", table_cell),
            Paragraph("Judul Poster, Header Banner, Nomor Urut, Nama Paslon. Huruf kapital (*ALL CAPS*) dengan sedikit tracking (+10 s/d +30).", table_cell)
        ],
        [
            Paragraph("<b>Body / Isi</b>", table_cell_bold),
            Paragraph("Poppins", table_cell),
            Paragraph("Regular (400), Medium (500)", table_cell),
            Paragraph("Penjelasan visi misi, tanggal tahapan, alur memilih, caption penjelasan. Gunakan <i>line-height</i> minimal 1.5x.", table_cell)
        ],
        [
            Paragraph("<b>Sub-Header / Label</b>", table_cell_bold),
            Paragraph("Poppins", table_cell),
            Paragraph("SemiBold (600)", table_cell),
            Paragraph("Label tahapan, sub-judul poin visi, nama divisi panitia, badge kategori.", table_cell)
        ]
    ]

    t_typo = Table(typo_data, colWidths=[110, 110, 115, 180])
    t_typo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_typo)

    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Aturan Penyusunan Teks:</b>", h2_style))
    story.append(Paragraph("• <b>Rata Kiri (*Left-Aligned*):</b> Seluruh naskah visi-misi dan teks paragraf wajib rata kiri. Dilarang memakai <i>Justify</i> (rata kanan-kiri) karena menimbulkan spasi bolong-bolong (*rivers of white*).", bullet_style))
    story.append(Paragraph("• <b>Kontras Minimum:</b> Teks putih hanya boleh di atas background Navy/Gelap. Teks pada background putih wajib memakai Navy (#0D1B2A) atau Slate Dark (#1E293B) dengan rasio kontras minimal 4.5:1.", bullet_style))

    story.append(Spacer(1, 14))

    # --- BAB 4: LAYOUT, GRID & SAFE ZONE ---
    story.append(Paragraph("BAB IV. LAYOUT, DIMENSI KANVAS & SAFE ZONE MEDIA", h1_style))
    story.append(Paragraph(
        "Setiap platform digital dan media cetak memiliki karakteristik teknis yang berbeda. "
        "Desainer wajib memastikan seluruh teks penting dan subjek foto berada di dalam <b>Safe Zone</b>:",
        body_style
    ))

    layout_data = [
        [
            Paragraph("Platform / Media", table_header),
            Paragraph("Rasio & Resolusi", table_header),
            Paragraph("Aturan Safe Zone (Zona Aman Teks & Subjek)", table_header)
        ],
        [
            Paragraph("<b>Feed Instagram</b><br/>(Postingan Utama)", table_cell_bold),
            Paragraph("<b>4:5 Portrait</b><br/>1080 x 1350 px<br/>(Wajib 4:5, dilarang 1:1)", table_cell),
            Paragraph("<b>Grid 1:1 Safe Center:</b> Elemen paling penting (wajah paslon, judul postingan, nomor urut) WAJIB berada di area tengah <b>1080 x 1080 px</b> agar tidak terpotong saat muncul di profil feed Instagram.<br/>Beri margin tepi luar minimal <b>80 px</b>.", table_cell)
        ],
        [
            Paragraph("<b>Story & Reels IG</b><br/>(Live Report, Countdown)", table_cell_bold),
            Paragraph("<b>9:16 Vertikal</b><br/>1080 x 1920 px", table_cell),
            Paragraph("• <b>Top Safe Zone:</b> Kosongkan <b>250 px</b> dari atas (area nama akun & story bar).<br/>• <b>Bottom Safe Zone:</b> Kosongkan <b>280 px</b> dari bawah (area kolom kirim pesan & like).<br/>Area aman teks: Y = 250 px s/d Y = 1640 px.", table_cell)
        ],
        [
            Paragraph("<b>Banner Lapangan</b><br/>(Panggung Utama)", table_cell_bold),
            Paragraph("<b>3:1 Landscape</b><br/>Ukuran: 300 x 100 cm<br/>Skala: 1:10 (300 DPI)", table_cell),
            Paragraph("<b>Margin Lipat & Ring Mata Ayam:</b> Beri jarak kosong aman minimal <b>15 cm</b> dari seluruh tepi luar spanduk agar teks tidak terpotong saat dilipat/dilem atau tertusuk ring besi gantungan.", table_cell)
        ],
        [
            Paragraph("<b>ID Card Panitia</b><br/>(Lanyard)", table_cell_bold),
            Paragraph("<b>Ukuran B3 / A6</b><br/>105 x 148 mm<br/>Bleed: 2 mm (CMYK)", table_cell),
            Paragraph("Area lubang kait lanyard di atas: beri ruang bebas minimal <b>20 mm</b> dari sisi atas kartu. Foto panitia berukuran proporsional dan nama jelas.", table_cell)
        ]
    ]

    t_layout = Table(layout_data, colWidths=[120, 115, 280])
    t_layout.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_layout)

    story.append(Spacer(1, 14))

    # --- BAB 5: NETRALITAS MUTLAK PASLON ---
    story.append(Paragraph("BAB V. PROTOKOL NETRALITAS MUTLAK PASLON (*ELECTION FAIRNESS*)", h1_style))
    story.append(Paragraph(
        "Sebagai penyelenggara pemilu (MPK), Divisi PDD memegang prinsip <b>independen dan netral tanpa keberpihakan</b>. "
        "Pelanggaran estetika yang menguntungkan salah satu paslon dianggap sebagai pelanggaran berat:",
        body_style
    ))

    story.append(Paragraph("<b>1. Ketentuan Foto Profil Paslon:</b>", h2_style))
    story.append(Paragraph("• <b>Dimensi Frame & Ukuran Kepala:</b> Ukuran kotak bingkai foto Paslon 1 dan Paslon 2 wajib 100% identik dalam piksel. Jarak mata (*eye-level*) dan skala kepala harus berada di garis horizontal yang sama.", bullet_style))
    story.append(Paragraph("• <b>Grading & Retouching Kulit:</b> Dilarang memoles salah satu paslon lebih putih/glowing sementara paslon lain dibiarkan kusam. Gunakan preset grading warna yang sama untuk seluruh paslon.", bullet_style))
    story.append(Paragraph("• <b>Pakaian & Latar:</b> Kedua paslon wajib mengenakan seragam sekolah resmi yang sama (baju praktek/OSIS sesuai kesepakatan) dengan latar belakang polos tanpa ornamen pembeda.", bullet_style))

    story.append(Paragraph("<b>2. Ketentuan Teks Visi, Misi & Nomor Urut:</b>", h2_style))
    story.append(Paragraph("• <b>Ukuran Tipografi Setara:</b> Ukuran huruf (*font size*) teks visi misi kedua paslon wajib sama persis. Jika teks paslon A lebih panjang, paslon B TIDAK BOLEH diperbesar fontnya hanya untuk memenuhi bidang kosong.", bullet_style))
    story.append(Paragraph("• <b>Verifikasi Teks:</b> Seluruh teks visi-misi WAJIB disalin langsung dari dokumen master terverifikasi di tab Administrasi. Dilarang menambah atau memparafrase kalimat paslon secara sepihak.", bullet_style))
    story.append(Paragraph("• <b>Urutan Paparan:</b> Urutan tampil di slide carousel atau urutan kiri-ke-kanan mutlak didasarkan pada nomor urut undian resmi KPU/MPK.", bullet_style))

    story.append(Spacer(1, 14))

    # --- BAB 6: LOGO RESMI & CLEAR SPACE ---
    story.append(Paragraph("BAB VI. ATURAN PENGGUNAAN LOGO RESMI & INTEGRASI BRAND", h1_style))
    story.append(Paragraph(
        "Tiga entitas logo resmi yang wajib disematkan pada seluruh rilisan resmi adalah: <b>Logo SMKN 13 Bandung</b>, <b>Logo MPK</b>, dan <b>Logo OSIS</b>.",
        body_style
    ))
    story.append(Paragraph("• <b>Hierarki Penempatan:</b> Pada media cetak/banner, Logo SMKN 13 diletakkan di sisi paling kiri/tengah atas sebagai induk sekolah, disusul Logo MPK dan OSIS di sisi yang seimbang.", bullet_style))
    story.append(Paragraph("• <b>Aspek Rasio Terkunci:</b> Menarik ukuran logo WAJIB selalu dari sudut diagonal pojok sambil menahan tombol Shift. Dilarang memipihkan (*squash*) atau meregangkan (*stretch*) logo dalam kondisi apa pun.", bullet_style))
    story.append(Paragraph("• <b>Ruang Bebas (*Clear Space*):</b> Berikan ruang bernapas di sekeliling logo minimal setara 50% tinggi logo tersebut tanpa tertabrak teks lain atau garis batas.", bullet_style))
    story.append(Paragraph("• <b>Format Bersih:</b> Gunakan file asli format PNG transparan dari folder <code>_LOGO_RESMI_HD</code>. Dilarang menggunakan logo hasil crop kasar yang menyisakan tepian putih.", bullet_style))

    story.append(Spacer(1, 14))

    # --- BAB 7: FILE MANAGEMENT & ALUR KERJA ---
    story.append(Paragraph("BAB VII. STANDAR PENAMAAN FILE, EXPORT & QUALITY CONTROL (QC)", h1_style))
    story.append(Paragraph(
        "Agar file arsip tidak tercecer dan tim multimedia/desain dapat bekerja secara terstruktur, "
        "seluruh anggota PDD wajib menerapkan standar operasional berikut:",
        body_style
    ))

    story.append(Paragraph("<b>1. Standar Penamaan File (*Naming Convention*):</b>", h2_style))
    story.append(Paragraph("Gunakan format: <code>[FASE]_[FORMAT]_[NAMA-KONTEN]_[VERSI].[ext]</code>", body_style))
    
    naming_data = [
        [Paragraph("Contoh Nama File", table_header), Paragraph("Keterangan & Peruntukan", table_header)],
        [
            Paragraph("<code>PRA_FEED_ALUR-MEMILIH_V1.png</code>", table_cell),
            Paragraph("Feed pra-hari H tentang alur memilih, draf versi pertama.", table_cell)
        ],
        [
            Paragraph("<code>PRA_FEED_VISI-MISI-PASLON_FINAL.png</code>", table_cell),
            Paragraph("Poster visi misi paslon yang sudah disetujui (*ACC*) koordinator.", table_cell)
        ],
        [
            Paragraph("<code>HARI-H_STORY_LIVE-ORASI_V2.mp4</code>", table_cell),
            Paragraph("Story video liputan hari H sesi orasi kandidat, revisi kedua.", table_cell)
        ],
        [
            Paragraph("<code>CETAK_BANNER_PANGGUNG_3x1M_SIAP-PRINT.pdf</code>", table_cell),
            Paragraph("File master cetak spanduk panggung 3x1 meter resolusi tinggi (CMYK).", table_cell)
        ]
    ]
    t_naming = Table(naming_data, colWidths=[240, 275])
    t_naming.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_naming)

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>2. Standar Ekspor (*Export Specifications*):</b>", h2_style))
    story.append(Paragraph("• <b>Postingan Gambar (Feed/Story):</b> Format <b>PNG</b> (24-bit). Hindari JPEG kualitas rendah untuk mencegah artefak buram pada teks dan logo.", bullet_style))
    story.append(Paragraph("• <b>Video Reels / Story:</b> Format <b>MP4 (H.264 / AAC)</b>, 1080x1920 piksel pada 30 atau 60 fps, bitrate audio minimal 128 kbps.", bullet_style))
    story.append(Paragraph("• <b>Bahan Cetak:</b> Format <b>PDF Print</b> (Press Quality) atau TIFF 300 DPI, mode warna CMYK.", bullet_style))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>3. Alur Kerja & Approval Checklist:</b>", h2_style))

    workflow_data = [
        [
            Paragraph("Tahap", table_header),
            Paragraph("Penanggung Jawab", table_header),
            Paragraph("Aktivitas & Kriteria Lolos (Checklist QC)", table_header)
        ],
        [
            Paragraph("<b>1. Draft Desain</b>", table_cell_bold),
            Paragraph("Desainer Grafis / Editor", table_cell),
            Paragraph("Mengerjakan aset mengacu pada master template di Canva/CapCut. Menggunakan palet 3 warna dan font resmi.", table_cell)
        ],
        [
            Paragraph("<b>2. Self-QC</b>", table_cell_bold),
            Paragraph("Desainer Terkait", table_cell),
            Paragraph("Mengecek mandiri: 1) Tidak ada typo nama/tanggal; 2) Elemen di safe zone; 3) Foto paslon seimbang; 4) Logo proporsional.", table_cell)
        ],
        [
            Paragraph("<b>3. Review Koor</b>", table_cell_bold),
            Paragraph("Davin (Koordinator)", table_cell),
            Paragraph("Review kesesuaian brand, akurasi teks, dan netralitas. Mengubah status task di web menjadi <code>Review Koor</code>.", table_cell)
        ],
        [
            Paragraph("<b>4. ACC & Publish</b>", table_cell_bold),
            Paragraph("Koordinator & Admin", table_cell),
            Paragraph("Setelah dinyatakan ACC (<code>Done</code>), file diunggah ke folder Drive resmi dan diposting sesuai jadwal rilis publikasi.", table_cell)
        ]
    ]

    t_wf = Table(workflow_data, colWidths=[90, 120, 305])
    t_wf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_wf)

    story.append(Spacer(1, 16))

    # Sign-off box
    sign_data = [
        [
            Paragraph("<b>Ditetapkan di:</b> Bandung<br/><b>Tanggal:</b> 17 Oktober 2026", table_cell),
            Paragraph("<b>Koordinator Divisi PDD PILKETOS</b><br/><br/><br/><b><u>Davin Maritza</u></b><br/>MPK SMKN 13 Bandung", table_cell)
        ]
    ]
    t_sign = Table(sign_data, colWidths=[260, 255])
    t_sign.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, gold_color),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FDFDFD")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_sign)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"SOP PDF successfully generated: {filename}")

if __name__ == '__main__':
    build_pdf('SOP_Desain_PDD.pdf')
