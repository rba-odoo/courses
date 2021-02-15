from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError



class Lesson(models.Model):
    _name = 'course.lesson'

    name = fields.Char()
    course_ids = fields.Many2many("course.course", 'course_lesson_rel','lesson_ids', 'course_ids', "Courses")
    room_id = fields.Many2one('course.room', "Room")
    attendees_ids = fields.Many2many("res.partner")

class Room(models.Model):
    _name = 'course.room'

    name = fields.Char()
    course_id = fields.Many2one('course.course', "Course")
    lesson_ids = fields.One2many('course.lesson','room_id', "Lessons")
    capacity = fields.Integer('Capacity', help="Room capacity for total number of participants")


class Course(models.Model):
    _name = 'course.course'

    name = fields.Char()
    instructor_id = fields.Many2one('res.partner',string='Instructor', required=True)
    room_id = fields.Many2one('course.room', string="Room", required=True)
    lesson_ids = fields.Many2many("course.lesson")
    attendees_ids = fields.Many2many("res.partner", 'course_attendees_rel', 'course_ids', 'attendees_ids')
    description = fields.Text()
    from_date = fields.Datetime()
    to_date = fields.Datetime()

    @api.onchange('from_date', 'to_date')
    def onchange_dates(self):
        if self.to_date:
            if self.to_date < self.from_date:
                raise UserError("From date should not be less than To date")

    @api.onchange('attendees_ids','instructor_id')
    def _onchange_attendees_ids(self):
        if self.room_id and self.room_id.capacity < len(self.attendees_ids.ids):
            raise UserError(("Capacity of the room is full for this particular course. Attendees should not be more than %s") % self.room_id.capacity)
        if self.instructor_id and self.instructor_id.id in self.attendees_ids.ids:
            raise UserError("Instructor cannot be attendee of the same course")