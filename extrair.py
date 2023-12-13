from bs4 import BeautifulSoup
import requests
import sqlite3


def ExtrairArquivofuncao():
    url = 'https://www.vriconsulting.com.br/guias/guiasIndex.php?idGuia=22'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.select_one('section section:nth-of-type(2) table:nth-of-type(1)')
    rows = table.select('tbody tr')

    conn = sqlite3.connect('NF.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dados (
            N INTEGER,
            Campo TEXT,
            Descricao TEXT,
            Tipo TEXT,
            Tam TEXT,
            Dec TEXT,
            Entr TEXT,
            Saida TEXT
        )
    ''')

    for row in rows:
        columns = row.select('td')
        data = [col.get_text(strip=True) for col in columns]

        cursor.execute('''
            INSERT INTO dados (N, Campo, Descricao, Tipo, Tam, Dec, Entr, Saida)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)

    conn.commit()
    conn.close()
