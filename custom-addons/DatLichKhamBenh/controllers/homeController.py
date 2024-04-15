from odoo import http
from odoo import fields
from datetime import datetime, timedelta
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.http import Response
class  HomePage(http.Controller):

    @http.route('/', auth='public', website=True)
    def homePage(self, **kw):
        departments = http.request.env['medical.department'].search([])
        doctors = http.request.env['medical.doctor'].search([]).sorted(key='walkins_count', reverse=True)
        return http.request.render('DatLichKhamBenh.homepage', {
            'departments': departments,
            'doctors': doctors,
        })

    @http.route('/department/<model("medical.department"):department>/', auth='public', website=True)
    def display_department_detail(self, department):
        doctors = http.request.env['medical.doctor'].search([('department_id', '=', department.id)])
        
        arrDoctorScheduleTimes = []
        for doctor in doctors:
            if len(doctor.examination_schedule_ids) == 0:
                schedule_times = ""
            else :
                arrWalkinsByDoctor = http.request.env['medical.walkins'].search([('doctor_id', '=', int(doctor.id)), ('schedule_selection_id', '=', int(doctor.examination_schedule_ids[0].id))]).schedule_time_id._ids

                schedule_times = http.request.env['medical.examination_time'].search([('id','not in',arrWalkinsByDoctor), ('shift_id', '=', int(doctor.examination_schedule_ids[0].shift_id))])
            arrDoctorScheduleTimes.append({
                'doctor': doctor,
                'schedule_times': schedule_times,
            })
        return http.request.render('DatLichKhamBenh.department_detail', {
            'department': department,
            'doctors': doctors,
            'arrDoctorScheduleTimes': arrDoctorScheduleTimes,
        })
     
    @http.route('/doctor/<model("medical.doctor"):doctor>', auth='public', website=True)
    def display_doctor_detail(self, doctor):
        if len(doctor.examination_schedule_ids) == 0:
            return http.request.render('DatLichKhamBenh.doctor_detail', {
            'doctor': doctor,
        })
        arrWalkinsByDoctor = http.request.env['medical.walkins'].search([('doctor_id', '=', int(doctor.id)), ('schedule_selection_id', '=', int(doctor.examination_schedule_ids[0].id))]).schedule_time_id._ids

        schedule_times = http.request.env['medical.examination_time'].search([('id','not in',arrWalkinsByDoctor), ('shift_id', '=', int(doctor.examination_schedule_ids[0].shift_id))])

        return http.request.render('DatLichKhamBenh.doctor_detail', {
            'doctor': doctor,
            'schedule_times': schedule_times,
        })


    @http.route(['/get_schedule_times'], methods=['POST'], type='json', auth="public", website=True)
    def get_schedule_times(self, **kw):
        schedule_date = kw.get('schedule_date')
        doctor = kw.get('doctor_id')
        split_date = schedule_date.split('-')
        doctor_search = http.request.env['medical.doctor'].browse(int(doctor))
        date_convert = '%s/%s/%s'%(split_date[1],split_date[2],split_date[0])
        schedule_times = doctor_search.examination_schedule_ids.filtered(lambda x: x.schedule.strftime('%m/%d/%Y') == date_convert)
        print('schedule_times',schedule_times.id)

        arrWalkinsByDoctor = http.request.env['medical.walkins'].search([('doctor_id', '=', int(doctor)), ('schedule_selection_id', '=', int(schedule_times.id))]).schedule_time_id._ids
        print('arrWalkinsByDoctor: ', arrWalkinsByDoctor)
        schedule_times_list = http.request.env['medical.examination_time'].search([('id','not in',arrWalkinsByDoctor), ('shift_id', '=', int(schedule_times.shift_id.id))])
        print('schedule_times_list: ', schedule_times_list)
        return http.request.env['ir.ui.view']._render_template('DatLichKhamBenh.reload_schedule_times', values={'schedule_times': schedule_times_list})
        # schedule_times_list = []
        # if schedule_times:
        #     for rec in schedule_times:
        #         schedule_times_list.append((rec.id, rec.name))
        # return {
        #         'schedule_times_list': schedule_times_list
        #     }


        # next_days = []
        # today = fields.Date.today()
        # next_days.append(
        #     (
        #         str(today),
        #         ("Today "+ today.strftime("%Y-%m-%d"))
        #     )
        # ) 
        # for i in range(1, 7):  # Get the next 6 days
        #     next_day = today + timedelta(days=i)
        #     next_days.append(
        #         (
        #             str(next_day),
        #             (next_day.strftime("%a") + " "+ next_day.strftime("%Y-%m-%d"))
        #         )
        #     )  # Append formatted date string to the list
