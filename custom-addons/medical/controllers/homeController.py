from odoo import http
from odoo import fields
from datetime import datetime, timedelta
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.http import Response
class  HomePage(http.Controller):

    @http.route('/', auth='public', website=True)
    def homePage(self, **kw):
        departments = http.request.env['medical.department'].search([])
        doctors = http.request.env['medical.doctor'].sudo().search([]).sorted(key='walkins_count', reverse=True)
        return http.request.render('medical.homepage', {
            'departments': departments,
            'doctors': doctors,
        })
    
    @http.route('/department/', auth='public', website=True)
    def display_department(self, **kw):
        departments = http.request.env['medical.department'].search([])
        return http.request.render('medical.department', {
            'departments': departments,
        })

    @http.route('/department/<model("medical.department"):department>/', auth='public', website=True)
    def display_department_detail(self, department):
        doctors = http.request.env['medical.doctor'].sudo().search([('department_id', '=', department.id)])
        
        arrDoctorScheduleTimes = []
        for doctor in doctors:
            if len(doctor.examination_schedule_ids) == 0:
                schedule_times = ""
            else :
                arrWalkinsByDoctor = http.request.env['medical.walkins'].sudo().search([('doctor_id', '=', int(doctor.id)), ('schedule_selection_id', '=', int(doctor.examination_schedule_ids[0].id))]).schedule_time_id._ids

                schedule_times = http.request.env['medical.examination_time'].sudo().search([('id','not in',arrWalkinsByDoctor), ('shift_id', '=', int(doctor.examination_schedule_ids[0].shift_id))])
            arrDoctorScheduleTimes.append({
                'doctor': doctor,
                'schedule_times': schedule_times,
            })
        return http.request.render('medical.department_detail', {
            'department': department,
            'doctors': doctors,
            'arrDoctorScheduleTimes': arrDoctorScheduleTimes,
        })
     
    @http.route('/doctor/<model("medical.doctor"):doctor>', auth='public', website=True)
    def display_doctor_detail(self, doctor):
        if len(doctor.examination_schedule_ids) == 0:
            return http.request.render('medical.doctor_detail', {
            'doctor': doctor,
        })
        arrWalkinsByDoctor = http.request.env['medical.walkins'].sudo().search([('doctor_id', '=', int(doctor.id)), ('schedule_selection_id', '=', int(doctor.examination_schedule_ids[0].id))]).schedule_time_id._ids

        schedule_times = http.request.env['medical.examination_time'].sudo().search([('id','not in',arrWalkinsByDoctor), ('shift_id', '=', int(doctor.examination_schedule_ids[0].shift_id))])

        return http.request.render('medical.doctor_detail', {
            'doctor': doctor,
            'schedule_times': schedule_times,
        })


    @http.route(['/get_schedule_times'], methods=['POST'], type='json', auth="public", website=True)
    def get_schedule_times(self, **kw):
        schedule_date = kw.get('schedule_date')
        doctor = kw.get('doctor_id')
        split_date = schedule_date.split('-')
        doctor_search = http.request.env['medical.doctor'].sudo().browse(int(doctor))
        date_convert = '%s/%s/%s'%(split_date[1],split_date[2],split_date[0])
        schedule_times = doctor_search.examination_schedule_ids.filtered(lambda x: x.schedule.strftime('%m/%d/%Y') == date_convert)
        # print('schedule_times',schedule_times.id)
        arrWalkinsByDoctor = http.request.env['medical.walkins'].sudo().search([('doctor_id', '=', int(doctor)), ('schedule_selection_id', '=', int(schedule_times.id))]).schedule_time_id._ids
        # print('arrWalkinsByDoctor: ', arrWalkinsByDoctor)
        schedule_times_list = http.request.env['medical.examination_time'].sudo().search([('id','not in',arrWalkinsByDoctor), ('shift_id', '=', int(schedule_times.shift_id.id))])
        # print('schedule_times_list: ', schedule_times_list)
        return http.request.env['ir.ui.view']._render_template('medical.reload_schedule_times', values={'schedule_times': schedule_times_list})

    @http.route(['/create-appointment'], type='json', auth="public", website=True)
    def final_submission(self, **kw):
        patient_name = kw.get('patient_name')
        phone = kw.get('phone')
        email = kw.get('email')
        dob = kw.get('dob')
        sex = kw.get('sex')
        reason = kw.get('reason')
        schedule_date_id = kw.get('schedule_date_id')
        schedule_time_id = kw.get('schedule_time_id')
        department_id = kw.get('department_id')
        doctor_id = kw.get('doctor_id')
        doctor_search = http.request.env['medical.doctor'].sudo().browse(int(doctor_id))
        # dob_convert = '%s-%s-%s'%(split_dob[0],split_dob[1],split_dob[2])

        schedule_date_search = http.request.env['medical.examination_schedule'].browse(int(schedule_date_id))
        schedule_time_search = http.request.env['medical.examination_time'].browse(int(schedule_time_id))
        date_value = schedule_date_search.schedule
        float_value = schedule_time_search.name
        if date_value and float_value:
            hours = int(float_value)
            minutes = int((float_value - hours) * 60)
            # print(hours, minutes)
            combined_datetime = fields.datetime.strptime(str(date_value), '%Y-%m-%d').replace(hour=(hours - 7), minute=minutes) #(hourse-7 => thời gian khám đang hiển thị là giờ VN))
            schedule_datetime = combined_datetime
            print('schedule_datetime: ',  schedule_datetime)

        try:
            searchPhone = http.request.env['medical.patient'].search([('phone', '=', phone )])
            if searchPhone:
                walkin = http.request.env['medical.walkins'].create({
                'patient_id': searchPhone.id,
                'health_center_id': doctor_search.health_center_id.id,
                'department_id': department_id,
                'doctor_id': doctor_id,
                'schedule_selection_id': schedule_date_id,
                'schedule_time_id': schedule_time_id,
                'reason_check': reason,
                'schedule_date': schedule_datetime,
                })
                return
                # return http.request.env['ir.ui.view']._render_template('medical.reload_schedule_times', values={'phone': phone, 'email': searchPhone.email})
            patient = http.request.env['medical.patient'].create({
                'name': patient_name,
                'sex': sex,
                'dob': dob,
                'phone': phone,
                'email': email,
            })
            walkin = http.request.env['medical.walkins'].create({
                'patient_id': patient.id,
                'health_center_id': doctor_search.health_center_id.id,
                'department_id': department_id,
                'doctor_id': doctor_id,
                'schedule_selection_id': schedule_date_id,
                'schedule_time_id': schedule_time_id,
                'reason_check': reason,
                'schedule_date': schedule_datetime,
            })
        except Exception as e:
            print('Error:', e)
            # return http.request.redirect('/error')
