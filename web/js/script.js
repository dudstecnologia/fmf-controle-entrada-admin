var connection = false

setInterval(() => { getRegisters() }, 2000)

eel.get_ports()(ports => {
    ports.forEach(port => {
        $('#selectPorts').append(new Option(port.description, port.port))
    })
})

function getRegisters() {
    eel.get_registers()(registers => {
        // console.log(r)
        let tableRegisters = document.getElementById('table-registers').getElementsByTagName('tbody')[0];
        tableRegisters.innerHTML = '';

        registers.forEach(register => {
            // console.log(register)
            let row = tableRegisters.insertRow();

            let morador = row.insertCell(0);
            let torre = row.insertCell(1);
            let apartamento = row.insertCell(2);
            let placa = row.insertCell(3);
            let data = row.insertCell(4);
            let action = row.insertCell(5);

            const btnSendCommand = document.createElement('button');
            btnSendCommand.innerHTML = 'Liberar';
            btnSendCommand.className = 'btn btn-sm btn-success';

            btnSendCommand.onclick = function() {
                open(register.id);
            };

            morador.innerHTML = register.name;
            torre.innerHTML = register.tower;
            apartamento.innerHTML = register.apartment;
            placa.innerHTML = register.plate;
            data.innerHTML = register.date_entry;

            if (register.status_deliveryman == 1) {
                action.appendChild(btnSendCommand);
            } else {
                action.innerHTML = ''
            }
        })
    })
}

$('#formConnection').submit((e) => {
    e.preventDefault()

    let port = $('#selectPorts').val()

    if (!port) {
        Swal.fire({
          icon: 'error',
          text: 'Selecione uma porta serial válida',
        })
        return false
    }

    eel.connection(port)

    $('#selectPorts').prop('disabled', true)
    $('#btnConnect').prop('disabled', true)
    $('#btnDisconnect').prop('disabled', false)
    $('#btnClose').prop('disabled', false)
    connection = true
})

$("#btnDisconnect").click(() => {
    eel.disconnect()

    $('#selectPorts').prop('disabled', false)
    $('#btnDisconnect').prop('disabled', true)
    $('#btnConnect').prop('disabled', false)
    $('#btnClose').prop('disabled', true)
    connection = false
})

$("#btnClose").click(() => {
    if (connection) {
        eel.close()
    }
})

function open(id) {
    if (connection) {
        eel.open(id)
    }
}
