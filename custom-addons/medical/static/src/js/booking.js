/* @odoo-module */

import { jsonrpc } from "@web/core/network/rpc_service";

$(document).ready(function () {
    function handleClickBtnTimes() {
        let arrBtnTimeSchedule = document.querySelectorAll('.btn-time-booking')
        let scheduleDateBtn = document.getElementById('schedule_date');
        let registerWalkinWrapper = document.querySelector('.register_walkin-wrapper')
        let onDepartmentRegisterWalkinWrapper = document.querySelector('.on_department-register_walkin-wrapper')

        let doctor = document.querySelector('input[name="doctor"]');
        let department = document.querySelector('input[name="department"]');
        let scheduleDate = document.querySelector('input[name="schedule_date"]');
        let scheduleTime = document.querySelector('input[name="schedule_time"]');

        arrBtnTimeSchedule.forEach(item => {
            item.addEventListener('click', async (event) => {
                // console.log(event.target);
                // console.log(scheduleDate.value)
                if (registerWalkinWrapper) {
                    registerWalkinWrapper.style.display = 'block'
                    doctor.value = scheduleDateBtn.getAttribute("data-doctorName")
                    doctor.setAttribute("data-doctorId", scheduleDateBtn.getAttribute("data-doctorId"))
                    department.setAttribute("data-departmentId", scheduleDateBtn.getAttribute("data-departmentId"))
                    department.value = scheduleDateBtn.getAttribute("data-departmentName")
                    scheduleDate.value = scheduleDateBtn.options[scheduleDateBtn.selectedIndex].text
                    scheduleDate.setAttribute("data-scheduleDateId", scheduleDateBtn.options[scheduleDateBtn.selectedIndex].value)
                    scheduleTime.value = event.target.innerText
                    scheduleTime.setAttribute("data-scheduleTimeId", event.target.getAttribute("data-scheduleTimeId"))
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

                                let scheduleDateBtn = document.getElementById('schedule_date');
                                let department_id = scheduleDateBtn.getAttribute("data-departmentId")
                                let doctor_id = scheduleDateBtn.getAttribute("data-doctorId")
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
                                        showToast(phone.value, email.value)
                                        let registerWalkinWrapper = document.querySelector('.register_walkin-wrapper');
                                        registerWalkinWrapper.style.display = 'none';
                                        var scheduleDateBtn = document.getElementById('schedule_date');
                                        renderScheduleTimes(scheduleDateBtn);
                                        patientName.value = "";
                                        phone.value = "";
                                        email.value = "";
                                        dob.value = "";
                                        reason.value = "";
                                    })
                                    .catch(function (error) {
                                        console.error('Error:', error);
                                    })
                            } else {
                                console.log("Cancel booking");
                            }
                        }
                    })
                }
                else if (onDepartmentRegisterWalkinWrapper) {
                    let parent = event.target.parentElement.parentElement.parentElement.parentElement
                    let scheduleDateTarget = parent.querySelector('.schedule_date')
                    onDepartmentRegisterWalkinWrapper.style.display = 'block'
                    doctor.value = scheduleDateTarget.getAttribute("data-doctorName")
                    doctor.setAttribute("data-doctorId", scheduleDateTarget.getAttribute("data-doctorId"))
                    department.value = scheduleDateTarget.getAttribute("data-departmentName")
                    department.setAttribute("data-departmentId", scheduleDateTarget.getAttribute("data-departmentId"))
                    scheduleDate.value = scheduleDateTarget.options[scheduleDateTarget.selectedIndex].text
                    scheduleDate.setAttribute("data-scheduleDateId", scheduleDateTarget.options[scheduleDateTarget.selectedIndex].value)
                    scheduleTime.value = event.target.innerText
                    scheduleTime.setAttribute("data-scheduleTimeId", event.target.getAttribute("data-scheduleTimeId"))
                    Validator('#on_department-register-form', {
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
                                    .then(async function (result) {
                                        showToast(phone.value, email.value)
                                        let onDepartmentRegisterWalkinWrapper = document.querySelector('.on_department-register_walkin-wrapper')
                                        onDepartmentRegisterWalkinWrapper.style.display = 'none';
                                        var arrScheduleDateBtn = document.querySelectorAll('.schedule_date');
                                        arrScheduleDateBtn.forEach(item => {
                                            if (item.getAttribute("data-doctorId") == doctor_id) {
                                                renderScheduleTimes(item);
                                            }
                                        })
                                        patientName.value = "";
                                        phone.value = "";
                                        email.value = "";
                                        dob.value = "";
                                        reason.value = "";
                                    })
                                    .catch(function (error) {
                                        console.error('Error:', error);
                                    })
                            } else {
                                console.log("Cancel booking");
                            }
                        }
                    })
                }
            })

        })
    }

    handleClickBtnTimes()

    // Hàm tạo và show toast thông báo
    function showToast(phone, email) {
        let toast = document.getElementById('toast');
        if (toast) {
            toast.innerHTML = `
                            <div class="toast toast--success" role="alert" aria-live="assertive" aria-atomic="true" data-delay="10000">
                                <div class="toast__icon">
                                    <i class="fa-solid fa-circle-check"></i>
                                </div>
                                <div class="toast__body">
                                    <p class="toast__msg">Đăng kí thành công!</p>
                                    <h4 class="toast__sub-msg">Vui lòng kiểm tra "sđt: ${phone}" hoặc "email: ${email}" để xem chi tiết lịch khám!</h4>
                                </div>
                                <div class="toast__close close" data-dismiss="toast" aria-label="Close">
                                    <i class="fa-solid fa-xmark icon__close "></i>
                                </div>
                            </div>
                            `
            $('.toast').toast('show')
        }
    }
    // Hàm render lại thời gian khám
    async function renderScheduleTimes(scheduleDateBtn) {
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
                $(`#${doctor_id}`).html(result)
                handleClickBtnTimes()
            })
            .catch(function (error) {
                console.error('Error:', error);
            })
    }
    // Xử lý render lại thời gian khám khi nhấn vào doctor page
    var scheduleDateBtn = document.getElementById('schedule_date');
    if (scheduleDateBtn) {
        scheduleDateBtn.addEventListener("change", async (event) => {
            renderScheduleTimes(scheduleDateBtn)
        });
    }

    // Xử lý render lại thời gian khám của từng bác sĩ trong khoa ở department page
    let arrScheduleDate = document.querySelectorAll('.schedule_date')
    arrScheduleDate.forEach(item => {
        item.addEventListener('change', async (event) => {
            renderScheduleTimes(item)
        })
    })

    // Xử lý đóng form đăng kí khám bênh
    let closeBtn = document.querySelectorAll('.close-btn')
    let registerWalkinWrapper = document.querySelector('.register_walkin-wrapper')
    let onDepartmentRegisterWalkinWrapper = document.querySelector('.on_department-register_walkin-wrapper')
    // if (registerWalkinWrapper) {
    //     registerWalkinWrapper.addEventListener('click', (event) => {
    //         registerWalkinWrapper.style.display = 'none'
    //     })
    // }
    // else if (onDepartmentRegisterWalkinWrapper) {
    //     onDepartmentRegisterWalkinWrapper.addEventListener('click', (event) => {
    //         onDepartmentRegisterWalkinWrapper.style.display = 'none'
    //     })
    // }
    $('.formbold-main-wrapper').on('click', (event) => {
        event.stopPropagation();
    })
    closeBtn.forEach(item => {
        if (item) {
            item.addEventListener('click', () => {
                if (registerWalkinWrapper) registerWalkinWrapper.style.display = 'none'
                else if (onDepartmentRegisterWalkinWrapper) onDepartmentRegisterWalkinWrapper.style.display = 'none'
            })
        }
    })
})

