import glob
from PIL import ExifTags
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import date
from spreadsheet import Equipment
import os
import sys
import PIL.Image


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# setup variables
WIDTH, HEIGHT = letter
styles = getSampleStyleSheet()
mbta_logo = resource_path("resources/MBTA_logo_text.png")
wsp_logo = resource_path("resources/img-png-wsp-red.png")
styleN = styles["Normal"]
styleT = ParagraphStyle(
    'newTitle',
    parent=styles['Title'],
    fontSize=14
)
document_name = "MBTA Tunnel Vent and System Assessment.pdf"
cs_colors = [colors.pink, colors.orange, colors.yellow, colors.lightgreen, colors.green]

for orientation_key in ExifTags.TAGS.keys():
    if ExifTags.TAGS[orientation_key] == 'Orientation':
        break


# for rotating portrait photos
class RotatedImage(Image):
    global orientation_key

    def __init__(self, orig_path, path):  # orig_path contains exif data, temp_path is compressed photo
        with PIL.Image.open(orig_path) as img:
            exif = img._getexif()
            if exif is not None and orientation_key in exif:
                self.orientation = exif[orientation_key]
            else:
                self.orientation = 0

        super().__init__(path, width=2.5 * inch, height=2.65 * inch, kind="proportional")

    # draws image with proper rotation based on orientation from exif data
    def draw(self):
        if self.orientation in [0, 1]:  # normal landscape/unknown rotation
            pass

        elif self.orientation in [6]:  # normal portrait, 90 degrees
            self.canv.rotate(-90)  # note that this rotation rotates counterclockwise, so it must be negative
            self.canv.translate(- self.drawWidth / 2 - self.drawHeight / 2, self.drawWidth / 2 - self.drawHeight / 2)

        elif self.orientation in [3]:  # upside down landscape, 180 degrees
            self.canv.rotate(180)
            self.canv.translate(- self.drawWidth, - self.drawHeight)

        elif self.orientation in [8]:  # backwards portrait, 270 degrees
            self.canv.rotate(90)
            self.canv.translate(- self.drawWidth / 2 + self.drawHeight / 2, - self.drawWidth / 2 - self.drawHeight / 2)

        Image.draw(self)


def create_equipment_table(equip):
    path = equip.image_path
    temp_path = path[:path.rfind("\\", 0, -1)] + "/temp/" + path[path.rfind("\\", 0, -1):]

    # fix rotated images
    image = RotatedImage(path, temp_path)

    # infomation paragraphs
    descr_p = Paragraph(equip.descr)
    descr_p.wrap(4.75 * inch, HEIGHT)
    sol_text_p = Paragraph(equip.sol_text)
    sol_text_p.wrap(4.75 * inch, HEIGHT)
    data = [
        ["  " + equip.id, Paragraph('<b>Room:</b>'), equip.room, Paragraph('<b>Equipment ID:</b>'), equip.equipment_id,
         Paragraph('<b>CS:</b> %s' % equip.cs)],
        [Paragraph('<b>ISSUE: %s</b>' % equip.title), "", "", "", image],
        [descr_p],
        [Paragraph('<b>SOLUTION: %s</b>' % equip.sol_title)],
        [sol_text_p],
    ]
    t = Table(data, style=[('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # align top row centered
                           ('ALIGN', (3, 1), (-1, 1), 'CENTER'),  # align title and photo
                           # ('ALIGN', (0, 3), (0, 3), 'CENTER'),  # align solution title centered
                           ('VALIGN', (0, 2), (0, 2), 'TOP'),
                           ('VALIGN', (0, 4), (0, 4), 'TOP'),
                           ('VALIGN', (4, 1), (-1, -1), 'CENTER'),
                           ('BOX', (0, 0), (-1, -1), 1, colors.black),
                           ('BOX', (0, 0), (-1, 0), 1, colors.black),
                           ('GRID', (0, 1), (3, -1), 1, colors.black),
                           ('SPAN', (0, 1), (3, 1)),  # span title
                           ('SPAN', (0, 2), (3, 2)),  # span descr
                           ('SPAN', (0, 3), (3, 3)),  # span sol title
                           ('SPAN', (0, 4), (3, 4)),  # span sol descr
                           ('SPAN', (-2, 1), (-1, -1)),  # span picture box
                           ('BACKGROUND', (-1, 0), (-1, 0), cs_colors[equip.cs - 1])
                           ],
              colWidths=[.4 * inch, .75 * inch, 2.3 * inch, 1.25 * inch, 1.9 * inch, .6 * inch],
              rowHeights=[.25 * inch, .25 * inch, 1.25 * inch, .25 * inch, 1 * inch])
    return t


# creates report table for top of document
def create_report_table(loc):
    data = [
        [Paragraph('<b>RAIL LINE:</b> %s' % loc.rail),
         Paragraph('<b>INSPECTION DATE:</b> %s' % loc.insp_date)],
        [Paragraph('<b>LOCATION:</b> %s' % loc.location),
         Paragraph('<b>TIN NUMBER: </b> %s' % loc.tin)],
    ]
    t = Table(data)
    return t


def create_condition_notes_table(loc):
    data = [
        ["CS: 5", "Condition State 5", "", Paragraph('<b>NOTES:</b> %s' % loc.notes)],
        ["CS: 4", "Condition State 4"],
        ["CS: 3", "Condition State 3"],
        ["CS: 2", "Condition State 2"],
        ["CS: 1", "Condition State 1"],
    ]
    t = Table(data, style=[
        ('VALIGN', (-1, 0), (-1, -1), 'TOP'),
        ('BOX', (-1, 0), (-1, -1), 1, colors.black),
        ('GRID', (0, 0), (0, -1), 1, colors.black),
        ('SPAN', (-1, 0), (-1, -1)),  # span notes block
        ('BACKGROUND', (0, 0), (0, 1), cs_colors[4]),
        ('BACKGROUND', (0, 1), (0, 2), cs_colors[3]),
        ('BACKGROUND', (0, 2), (0, 2), cs_colors[2]),
        ('BACKGROUND', (0, 3), (0, 3), cs_colors[1]),
        ('BACKGROUND', (0, 4), (0, 4), cs_colors[0]),
    ],
              colWidths=[.5 * inch, 1.25 * inch, 1.25 * inch, 3 * inch])
    return t


# formatting for the first page
def first_page_format(canvas, doc):
    canvas.saveState()

    # setup header
    canvas.drawImage(mbta_logo, .45 * inch, HEIGHT - .05 * inch, width=100, height=19)
    canvas.drawImage(wsp_logo, WIDTH - 1.65 * inch, HEIGHT - .2 * inch, width=70, height=33)
    p = Paragraph("MBTA TUNNEL VENTILATION FACILITY AND SYSTEM ASSESSMENT", styleT)
    w, h = p.wrap(inch * 4, HEIGHT)
    p.drawOn(canvas, (WIDTH - 16) / 2 - w / 2, HEIGHT - .25 - h / 2)

    # setup footer
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(.75 * inch, .75 * inch, "%s" % date.today().strftime("%m/%d/%Y"))
    canvas.drawCentredString((WIDTH - 16) / 2, .75 * inch, "Page %d" % doc.page)
    canvas.drawRightString(WIDTH - inch, .90 * inch, "Contract No. Z94PS10")
    canvas.drawRightString(WIDTH - inch, .75 * inch, "Task Order: 03")
    canvas.restoreState()


# assembles the document and saves it to the sheet's location
def build_document(sheet):
    doc = SimpleDocTemplate(os.path.join(sheet.folder, document_name), pageSize=letter,
                            title="MBTA Tunnel Vent and System Assessment", author="WSP")  # start document template
    story = []

    # add location table
    t = create_report_table(sheet.location)
    story.append(t)
    story.append(Spacer(1, 0.2 * inch))

    # add notes and condition table
    t = create_condition_notes_table(sheet.location)
    story.append(t)
    story.append(Spacer(1, 0.2 * inch))

    # compress images into temp folder
    sheet.compress_pictures()

    for i in range(5):
        story.append(Paragraph(sheet.fp.sheet_names[i + 1], style=styleT))

        for row in sheet.fp.parse(i + 1).itertuples():  # for row in spreadsheet
            e = Equipment.generate_equip(sheet.folder, row)
            t = create_equipment_table(e)

            story.append(KeepTogether(t))
            story.append(Spacer(1, 0.1 * inch))

    doc.build(story, onFirstPage=first_page_format, onLaterPages=first_page_format)

    # delete compressed image temp folder
    sheet.delete_compressed_pictures()


# checks if document already exists in sheet's folder
def check_doc_exists(sheet):
    matches = glob.glob(os.path.join(sheet.folder, document_name))
    return len(matches) != 0
