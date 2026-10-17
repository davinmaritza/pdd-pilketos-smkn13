/**
 * Google Apps Script untuk Realtime Task Tracker PDD PILKETOS
 * SMKN 13 Bandung - Tema: Praja Satya Nayaka
 *
 * CARA PASANG:
 * 1. Buka Google Drive (folder arsip PDD)
 * 2. Buat Spreadsheet baru / buka ALL_IN_ONE_PDD_PILKETOS di Google Sheets
 * 3. Klik menu "Ekstensi" (Extensions) -> "Apps Script"
 * 4. Hapus semua kode default, lalu tempel (paste) seluruh kode di bawah ini.
 * 5. Klik "Deploy" (Terapkan) di pojok kanan atas -> "New deployment" (Penerapan baru).
 * 6. Pilih jenis: "Web app" (Aplikasi Web).
 * 7. Isi:
 *    - Description: PDD Task Tracker API
 *    - Execute as: Me (email kamu)
 *    - Who has access: Anyone (Siapa saja)  <-- PENTING agar semua user bisa baca/tulis
 * 8. Klik "Deploy" -> Beri izin akses Google -> Salin Web App URL (berakhiran /exec).
 * 9. Berikan Web App URL tersebut untuk dipasang di index.html web portal.
 */

function doGet(e) {
  var props = PropertiesService.getScriptProperties();

  // Jika ada aksi update status dari website
  if (e && e.parameter && e.parameter.action === 'update') {
    var taskId = e.parameter.taskId;
    var status = e.parameter.status;
    if (taskId && status) {
      props.setProperty(taskId, status);
      return ContentService.createTextOutput(JSON.stringify({
        success: true,
        taskId: taskId,
        status: status,
        updatedAt: new Date().toISOString()
      })).setMimeType(ContentService.MimeType.JSON);
    }
  }

  // Default: Ambil seluruh data status tugas yang tersimpan
  var allTasks = props.getProperties();
  return ContentService.createTextOutput(JSON.stringify(allTasks))
    .setMimeType(ContentService.MimeType.JSON);
}
