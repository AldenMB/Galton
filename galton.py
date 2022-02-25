"""
A small Galton board. All units are millimeters.
"""
import cadquery as cq
from types import SimpleNamespace as ns
from math import sqrt, cos, sin, tan, pi

INCH = 25.4

pin = ns(diameter = 1, length=0.5*INCH)
screw = ns(diameter = 3, length= 0.25*INCH)#measure this

thickness = 2 + max(pin.length, screw.length)
depth = 4.5

spacing = 4
gate = ns(thickness = 1.5, height = 60)

border = 8

height = 220
width = 34 * spacing + 2 * border


galton = cq.Workplane().box(width, height, thickness)

galton = (galton
          .faces('>Z')
          .workplane()
          .moveTo(0, -height/2+border)
          .hLineTo(-width/2+border)
          .vLine(gate.height)
          .polarLine(26*spacing, 60)
          .line(4*spacing - 2.5/2, (4*spacing-2.5/2)*tan(pi/12))
          .vLine(3*depth)
          .line(-(34.5*spacing - 2.5)/2, (34.5*spacing-2.5)*tan(pi/12)/2)
          .vLineTo(height/2-border)
          .hLineTo(0)
          .mirrorY()
          .cutBlind(-depth)
          )
galton.ctx.firstPoint = None # was not set by mirror

galton = galton.edges("|Z exc >Y exc <Y").edges("not <Y").fillet(spacing)


galton = (galton
          .faces('>Z')
          .workplane()
          .rect(width-border*1.5, height-border*1.5, forConstruction=True)
          .vertices()
          .hole(screw.diameter, screw.length)
          )

galton = galton.edges("+Z").fillet(border)
galton = galton.faces("<Z").chamfer(3)

for i in range(35):
    galton = (galton
              .faces('>Z')
              .workplane()
              .moveTo(-width/2+border+i*spacing, -height/2+border+gate.height)
              .line(gate.thickness/2, -gate.thickness/2)
              .vLine(-gate.height)
              .hLine(-gate.thickness)
              .vLine(gate.height)
              .close()
              .extrude('next')
    )

galton = galton.faces('>Z[-2]').edges().fillet(0.5)

for row in range(32-7):
    for column in range(32 - row):
        galton = (galton
                  .moveTo(
                      (column+row/2-31/2)*spacing,
                      -height/2 + border + gate.height + spacing * sqrt(3) * (row+1) / 2
                      )
                  .hole(pin.diameter, pin.length)
            )


cq.exporters.export(galton, 'galton.stl')

if __name__ == 'temp':
    show_object(galton, options={'alpha':0.8})