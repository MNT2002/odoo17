/* @odoo-module */

import { jsonrpc } from "@web/core/network/rpc_service";

$(document).ready(function () {
    var scheduleDateBtn = document.getElementById('schedule_date');
    if (scheduleDateBtn) {
        scheduleDateBtn.addEventListener("change", async (event) => {

            let doctor_id = scheduleDateBtn.getAttribute("data-doctorId")
            if (!doctor_id) {
                console.error("Doctor ID is missing or invalid!");
                return;
            }

            await jsonrpc('/get_schedule_times', {
                'schedule_date': $(scheduleDateBtn)[0].value,
                'doctor_id': doctor_id
            }
            )
                .then(function (result) {
                    console.log($('#reload_schedule_times'))
                    $('#reload_schedule_times').html(result)
                })
                .catch(function (error) {
                    console.error('Error:', error);
                })
        });
    }

    var scheduleTimes = document.querySelectorAll('.schedule_date')
    scheduleTimes.forEach(itemt => {
        itemt.addEventListener('change', async (event) => {
            let doctor_id = itemt.getAttribute("data-doctorId")
            if (!doctor_id) {
                console.error("Doctor ID is missing or invalid!");
                return;
            }

            await jsonrpc('/get_schedule_times', {
                'schedule_date': event.target.value,
                'doctor_id': doctor_id
            }
            )
                .then(function (result) {
                    console.log($('#reload_schedule_times_department'))
                    console.log('result: ',result)
                    $(`#${doctor_id}`).html(result)
                })
                .catch(function (error) {
                    console.error('Error:', error);
                })
        })
    })

})

