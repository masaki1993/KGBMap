const { google } = require('googleapis');
const sheets = google.sheets('v4');
const credentials = require('./credentials.json');

exports.handler = async (event) => {
    const { boardNumber, status, volunteerId } = JSON.parse(event.body);

    const auth = new google.auth.JWT(
        credentials.client_email,
        null,
        credentials.private_key,
        ['https://www.googleapis.com/auth/spreadsheets']
    );

    const spreadsheetId = '1tymbmtDTGGCVuBbDho4c1YiyLwFbLSi2CQfYAty7pz4';
    const sheetName = '掲示板';

    const response = await sheets.spreadsheets.values.get({
        auth,
        spreadsheetId,
        range: `${sheetName}!A:D`, // 例：A列が掲示板番号、B列がステータス、C列が更新者ID、D列が更新日時
    });

    const rows = response.data.values;
    const rowIndex = rows.findIndex(row => row[0] === boardNumber);

    if (rowIndex === -1) {
        return {
            statusCode: 404,
            body: JSON.stringify({ success: false, message: 'Board number not found' }),
        };
    }

    rows[rowIndex][1] = status;
    rows[rowIndex][2] = volunteerId;
    rows[rowIndex][3] = new Date().toISOString();

    await sheets.spreadsheets.values.update({
        auth,
        spreadsheetId,
        range: `${sheetName}!A${rowIndex + 1}:D${rowIndex + 1}`,
        valueInputOption: 'RAW',
        resource: {
            values: [rows[rowIndex]],
        },
    });

    return {
        statusCode: 200,
        body: JSON.stringify({ success: true }),
    };
};