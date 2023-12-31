from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from reportlab.lib import colors

class TaskPDF:
    def __init__(self, tasks_data, file_name=None):
        self.tasks_data = tasks_data
        self.current_y_position = letter[1] - 10
        self.extra_space = 10
        self.line_space = 20
        self.margin_left = 36
        self.margin_right = letter[0] - 36
        self.margin_top = letter[1] - 36
        self.margin_bottom = 36
        self.logo_width = 50
        self.logo_height = 50
        self.user_icon_path = "icons/per1.png"
        self.creator_icon_path = "icons/per1.png"
        self.importance_icon_path = "icons/danger.webp"
        self.file_name = file_name if file_name else self.get_file_name()
        self.c = canvas.Canvas(self.file_name, pagesize=letter)
        self.add_header()
        

    def get_file_name(self):
        if self.file_name:
            return self.file_name
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"TaskMasterPro_Export_{current_time}.pdf"

    def add_header(self):
        self.c.saveState()
       
        self.logo_path = "icons/logo_task.png"
        logo_x = self.margin_left
        logo_y = self.margin_top - self.logo_height + 20
        self.c.drawInlineImage(self.logo_path, logo_x, logo_y, width=self.logo_width, height=self.logo_height)

       
        self.c.setFont("Helvetica-Bold", 35)
        title_text = "TaskMasterPro"
        title_x = logo_x + self.logo_width + 10
        title_y = logo_y + (self.logo_height - 40)
        self.c.drawString(title_x, title_y, title_text)

        
        self.c.setFont("Helvetica-Bold", 12)
        formatted_time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        header_text = f"Export - {formatted_time}"
        header_x = logo_x + self.logo_width + 17
        header_y = logo_y - 5
        self.c.drawString(header_x, header_y, header_text)
        self.current_y_position = logo_y - 30

        
        self.c.setFont("Helvetica-Bold", 18)
        title_x = self.margin_left
        title_y = self.current_y_position - 10
        agenda_title = "Tasks:"
        self.c.drawString(title_x, title_y, agenda_title)
        title_spacing = 25
        self.current_y_position -= title_spacing

    def format_date(self, input_string):
        def ordinal_suffix(day):
            if 10 <= day % 100 <= 20:
                suffix = 'th'
            else:
                suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
            return str(day) + suffix

        try:
        
            input_datetime = datetime.strptime(input_string, "%Y-%m-%d %H:%M:%S")
            output_string = "{} of {} {}".format(
                ordinal_suffix(input_datetime.day),
                input_datetime.strftime("%B"),
                input_datetime.strftime("%Y")
            )

            date_part = input_datetime.strftime("at %H:%M:%S")
 
            formatted_date = output_string + f" {date_part}"
   
            return formatted_date
        except:
            return input_string

    def add_task(self, task):
        
        name_text = f"{task['name']}"
        name_x = self.margin_left + 40
        name_y = self.current_y_position - 22
        self.c.setFont("Helvetica-Bold", 14)
        self.c.drawString(name_x, name_y, name_text)
        name_spacing = 10
        self.current_y_position -= name_spacing
        self.c.setFillColor(colors.Color(0, 0, 0, alpha=0.75))  
        tag_text = f"Tag: {task['tag']}"
        tag_x = name_x + self.c.stringWidth("Helvetica-Bold") - 96
        tag_y = name_y - 12
        self.c.setFont("Helvetica", 12)
        self.c.drawString(tag_x, tag_y, tag_text)
        tag_spacing = 20
        self.current_y_position -= tag_spacing
        self.c.setFillColor(colors.black)

        creation_date_text = f"Creation Date: {self.format_date(task.get('creation_date', 'No Creation Date'))}"
        creation_date_text_height = self.get_text_height(creation_date_text)

        if self.current_y_position - creation_date_text_height < 36:
            self.c.showPage()
            self.add_header()

        is_complete = task.get('is_complete', 0)
        self.logo_path = 'icons/false.png' if is_complete == 0 else 'icons/true.jpg'
        logo_x = self.margin_left
        logo_y = self.current_y_position - self.logo_height + 39
        self.c.drawInlineImage(self.logo_path, logo_x, logo_y, width=30, height=30)

        text_x = logo_x + 40
        text_y = logo_y + (self.logo_height - 15)
        self.c.setFont("Helvetica-Bold", 12)

        text_start_x = text_x + 10
        self.current_y_position -= creation_date_text_height + self.extra_space

        # Adjust the positions for User and Creator text
        user_creator_x = self.margin_right - 170
        user_creator_y = text_y - 15
        user_icon_x = user_creator_x - 20  
        user_icon_y = user_creator_y - 5  
        self.c.drawInlineImage(self.user_icon_path, user_icon_x, user_icon_y, width=15, height=15)

        creator_icon_x = user_creator_x - 20  
        creator_icon_y = user_creator_y - 22  
        self.c.drawInlineImage(self.creator_icon_path, creator_icon_x, creator_icon_y, width=15, height=15)

        importance = task.get('importance', 0)
        if importance > 0:
            label_text = f"Priority: {importance}"
            label_x = text_start_x
            label_y = self.current_y_position - self.get_text_height(label_text)
            self.c.setFont("Helvetica-Bold", 12)  
            self.c.drawString(label_x, label_y, label_text)

            icon_path = self.importance_icon_path
            icon_x = label_x + self.c.stringWidth(label_text, "Helvetica-Bold", 12) + 5 
            icon_y = label_y - 3
            self.c.drawInlineImage(icon_path, icon_x, icon_y, width=15, height=15)

            self.current_y_position -= self.get_text_height(label_text) + 5

        user_info = task.get('user', {})
        user_text = f"User: {user_info.get('u', '')} ({user_info.get('e', '')})"
        self.c.setFont("Helvetica", 12)
        self.c.drawString(user_creator_x, user_creator_y, user_text)
        user_creator_y -= self.get_text_height(user_text) + 5

        creator_info = task.get('creator', {})
        creator_text = f"Creator: {creator_info.get('u', '')} ({creator_info.get('e', '')})"
        self.c.setFont("Helvetica", 12)
        self.c.drawString(user_creator_x, user_creator_y, creator_text)
        user_creator_y -= self.get_text_height(creator_text) + 5

        details = [
            ('start_date', 'Task start on '),       
            ('deadline',''),
            ('description', 'Description: '),  
            ('creation_date', 'Task created on '),
        ]

        for detail, label in details:
            value = task.get(detail, '')
            if detail == 'start_date' or detail == 'creation_date':
                value = self.format_date(value)
                text = f"{label}{value}"
                self.add_normal_text(text, text_start_x)  
            elif detail == 'deadline':
                if value and value.lower() != "none":
                    value = f"Task must be complete before {self.format_date(value)}"
                    text = f"{label}{value}"
                    self.add_normal_text(text, text_start_x)
                else:
                    self.add_normal_text(f"{label}There is no deadline", text_start_x)         
            else:
                value = value if value else "No information available"
                text = f"{label}{value}"
                self.add_normal_text(text, text_start_x)  

        self.current_y_position -= self.extra_space
        self.c.setStrokeColor(colors.Color(0, 0, 0, alpha=0.55))  
        self.c.setFillColor(colors.Color(0, 0, 0, alpha=0.55))  

        self.c.line(self.margin_left, self.current_y_position, self.margin_right, self.current_y_position)
        self.c.setStrokeColor(colors.black)
        self.c.setFillColor(colors.black) 
        self.current_y_position -= self.line_space

    def add_normal_text(self, text, x):
        text_lines = self.wrap_text(text, self.margin_right - x)
        for line in text_lines:
            text_height = self.get_text_height(line)
            if self.current_y_position - text_height < 36:
                self.c.showPage()
                self.add_header()
            self.c.setFont("Helvetica", 12)  
        
            if "Description:" in line:
                index = line.index("Description:")
                self.c.drawString(x, self.current_y_position - text_height, line[:index])
    
   
                self.c.setFont("Helvetica-Bold", 12)
                self.c.drawString(x + self.c.stringWidth(line[:index], "Helvetica", 12), self.current_y_position - text_height, "Description:")
    
   
                self.c.setFont("Helvetica", 12)
                self.c.drawString(x + self.c.stringWidth("Description:", "Helvetica-Bold", 12), self.current_y_position - text_height, line[index + len("Description:"):])
            else:
                self.c.drawString(x, self.current_y_position - text_height, line)
            self.current_y_position -= text_height + 5

    def wrap_text(self, text, max_width):
        lines = []
        current_line = ""
        words = text.split()

        for word in words:
            if self.c.stringWidth(current_line + word, "Helvetica", 14) <= max_width:
                current_line += word + " "
            else:
                lines.append(current_line.strip())
                current_line = word + " "

        lines.append(current_line.strip())
        return lines

    def get_text_height(self, text):
        return self.c._leading

    def create_pdf(self):
        for task in self.tasks_data:
            self.add_task(task)

        self.c.save()

if __name__ == "__main__":
    tasks_data = [
        {"name": "test", "tag": "test", "creation_date": "2023-12-18 23:59:30", "start_date": "2023-12-18 23:59:00", "deadline": None, "user": {"u": "toto", "e": "toto@toto.com"}, "creator": {"u": "toto", "e": "toto@toto.com"}, "importance": 1, "is_complete": 1, "description": None},
        {"name": "Elmir", "tag": "SGEG", "creation_date": "2023-12-19 00:21:51", "start_date": "2023-12-21 00:21:00", "deadline": "2023-12-21 00:21:00", "user": {"u": "toto", "e": "toto@toto.com"}, "creator": {"u": "elmir", "e": "elmir.batjari@uha.fr"}, "importance": 2, "is_complete": 0, "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin sed aliquam purus. Fusce placerat ex at neque vehicula, at cursus ante sagittis. Praesent eget ante nisi. Nam placerat bibendum nisl, ac luctus lorem ultricies eget. Ut ultrices augue sed vulputate sollicitudin. Cras at mi a nulla consectetur pretium eu vitae risus. Curabitur sit amet placerat ligula. Integer gravida, eros et euismod cursus, sapien tortor tincidunt nisi, a tincidunt lacus dui vitae lacus. Donec consectetur efficitur."}
    ]

    file_name = "tasks_export.pdf"
    task_pdf = TaskPDF(tasks_data, file_name)
    task_pdf.create_pdf()
