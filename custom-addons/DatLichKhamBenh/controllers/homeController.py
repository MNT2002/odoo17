from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
class  HomePage(http.Controller):

    @http.route('/', website=True)
    def homePage(self, **kw):
        departments = http.request.env['medical.department'].search([])
        return http.request.render('DatLichKhamBenh.homepage', {
            'departments': departments,
        })

    @http.route('/department', auth='public', website=True)
    def index(self, **kw):
        departments = http.request.env['medical.department'].search([])
        return http.request.render('DatLichKhamBenh.departments', {
            'departments': departments,
        })

    @http.route('/department/<model("medical.department"):department>/', auth='public', website=True)
    def display_department_detail(self, department):
        return http.request.render('DatLichKhamBenh.department_detail', {
            'department': department
        })
    class DepartmentCustomerPortal(CustomerPortal):
        def _prepare_home_portal_values(self):
            values = super(DepartmentCustomerPortal, self)._prepare_home_portal_values()
            count_departments = http.request.env['medical.department'].search_count([])
            values.update({
                'count_departments': count_departments,
            })
            return values