/* @odoo-module */

import { jsonrpc } from "@web/core/network/rpc_service";

$(document).ready(function () {
    Validator('#register-form', {
        onSubmit: async function (data) {
            let result = confirm("Bạn có chắc chắn muốn tạo lịch khám!");
            if (result === true) {
                let patientName = document.querySelector('input[name="patient_name"]');
                let phone = document.querySelector('input[name="phone"]');
                let email = document.querySelector('input[name="email"]');
                let dob = document.querySelector('input[name="dob"]');
                let sex = document.querySelector('input[name="sex"]:checked');
                let reason = document.querySelector('input[name="reason"]');

                let scheduleDatetInput = document.querySelector('input[name="schedule_date"]');
                let schedule_date_id = scheduleDatetInput.getAttribute("data-scheduleDateId")
                let scheduleTimetInput = document.querySelector('input[name="schedule_time"]');
                let schedule_time_id = scheduleTimetInput.getAttribute("data-scheduleTimeId")
                let departmentInput = document.querySelector('input[name="department"]');
                let department_id = departmentInput.getAttribute("data-departmentId")
                let doctorInput = document.querySelector('input[name="doctor"]');
                let doctor_id = doctorInput.getAttribute("data-doctorId")
                let formData = {
                    'patient_name': patientName.value,
                    'phone': phone.value,
                    'email': email.value,
                    'dob': dob.value,
                    'sex': sex.value,
                    'schedule_date_id': schedule_date_id,
                    'schedule_time_id': schedule_time_id,
                    'department_id': department_id,
                    'doctor_id': doctor_id,
                    'reason': reason.value,
                }
                console.log('formData: ', formData)
                await jsonrpc('/create-appointment', formData)
                    .then(function (result) {
                    })
                    .catch(function (error) {
                        console.error('Error:', error);
                    })
            } else {
                console.log("Cancel booking");
            }
        }
    })
    function handleClickBtnTimes() {
        let arrBtnTimeSchedule = document.querySelectorAll('.btn-time-booking')
        let scheduleDateBtn = document.getElementById('schedule_date');
        let registerWalkinWrapper = document.querySelector('.register_walkin-wrapper')

        let doctorInput = document.querySelector('input[name="doctor"]');
        let department = document.querySelector('input[name="department"]');
        let scheduleDate = document.querySelector('input[name="schedule_date"]');
        let scheduleTime = document.querySelector('input[name="schedule_time"]');

        arrBtnTimeSchedule.forEach(item => {
            item.addEventListener('click', async (event) => {
                // console.log(event.target);
                // console.log(scheduleDate.value)
                registerWalkinWrapper.style.display = 'block'
                doctorInput.value = doctorInput.getAttribute("data-doctorName")
                department.value = department.getAttribute("data-departmentName")
                scheduleDate.value = scheduleDateBtn.options[scheduleDateBtn.selectedIndex].text
                scheduleDate.setAttribute("data-scheduleDateId", scheduleDateBtn.options[scheduleDateBtn.selectedIndex].value)
                scheduleTime.value = event.target.innerText
                scheduleTime.setAttribute("data-scheduleTimeId", event.target.getAttribute("data-scheduleTimeId"))
            })

        })
    }

    handleClickBtnTimes()

    // Xử lý render lại thời gian khám khi nhấn vào doctor page
    var scheduleDateBtn = document.getElementById('schedule_date');
    if (scheduleDateBtn) {
        scheduleDateBtn.addEventListener("change", async (event) => {

            let doctor_id = scheduleDateBtn.getAttribute("data-doctorId")
            if (!doctor_id) {
                console.error("Doctor ID is missing or invalid!");
                return;
            }

            await jsonrpc('/get_schedule_times', {
                'schedule_date': scheduleDateBtn.options[scheduleDateBtn.selectedIndex].text,
                'doctor_id': doctor_id
            })
                .then(function (result) {
                    // console.log(result)
                    $('#reload_schedule_times').html(result)
                    handleClickBtnTimes()
                })
                .catch(function (error) {
                    console.error('Error:', error);
                })
        });
    }

    // Xử lý render lại thời gian khám của từng bác sĩ trong khoa ở department page
    let scheduleTimes = document.querySelectorAll('.schedule_date')
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
                    // console.log($('#reload_schedule_times_department'))
                    // console.log('result: ',result)
                    $(`#${doctor_id}`).html(result)
                })
                .catch(function (error) {
                    console.error('Error:', error);
                })
        })
    })

    // Xử lý đóng form đăng kí khám bênh
    var closeBtn = document.querySelector('.close-btn')
    var registerWalkinWrapper = document.querySelector('.register_walkin-wrapper')
    if (registerWalkinWrapper) {
        registerWalkinWrapper.addEventListener('click', (event) => {
            registerWalkinWrapper.style.display = 'none'
        })
    }
    $('.formbold-main-wrapper').on('click', (event) => {
        event.stopPropagation();
    })
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            registerWalkinWrapper.style.display = 'none'
        })
    }

})

