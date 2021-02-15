from odoo import api, fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    course_instructor_ids = fields.One2many("course.course", 'instructor_id', string="Instructing")
    course_ids = fields.Many2many("course.course", 'course_attendees_rel', 'attendees_ids', 'course_ids', string="Attending")
    lesson_ids = fields.Many2many("course.lesson", 'lesson_attendees_rel', 'attendees_ids', 'lesson_ids', string="Lessons")
    instructed_courses_count = fields.Integer('# Courses Instructed', compute='_compute_courses_state')
    attended_courses_count = fields.Integer('# Courses Attended', compute='_compute_courses_state')

    @api.depends('course_instructor_ids', 'course_ids')
    def _compute_courses_state(self):
        self.instructed_courses_count = len(self.course_instructor_ids)
        self.attended_courses_count = len(self.course_ids)
        return True

    def action_show_courses_instructed(self):
        return {
            'name': 'Courses Instructed',
            'view_mode': 'tree,form',
            'domain': [('instructor_id', '=', self.id)],
            'res_model': 'course.course',
            'type': 'ir.actions.act_window',
            'context': {'group_by': ['instructor_id']}
        }
    def action_show_courses_attended(self):
        return {
            'name': 'Courses Attended',
            'view_mode': 'tree,form',
            'domain': [('attendees_ids', '=', self.id)],
            'res_model': 'course.course',
            'type': 'ir.actions.act_window',
        }