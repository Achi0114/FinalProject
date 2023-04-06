
url = 'http://127.0.0.1:5000'

async function getData() {
    const walletID = document.getElementById('walletInput')
    const response = await fetch(url+"/getpt",{
        method: "POST",
        headers:{
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            walletId:walletID
        })
    })
    const result = await response.json()
    const table = document.getElementById('tblData')

    object = {
        "HN": result['HN'],
        "data": result['data']
    }

    for (let i = 0; i < object['data'].length; i++) {
        const newRow = table.insertRow();
        const cell1 = newRow.insertCell(0);
        const cell2 = newRow.insertCell(1);
        const cell3 = newRow.insertCell(2);
        const cell4 = newRow.insertCell(3);
        const cell5 = newRow.insertCell(4);

    
        cell1.innerHTML = new Date(object['data'][i]['timestamp']*1000).toLocaleString();
        cell2.innerHTML = object['data'][i]['temperature'];
        cell3.innerHTML = object['data'][i]['HN'];
        cell4.innerHTML = object['data'][i]['heartrate'];
        cell5.innerHTML = object['data'][i]['spo2'];
      }
    }