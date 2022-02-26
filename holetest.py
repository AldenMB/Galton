"""
A block to check the sizes of the holes for good fit.
"""
import cadquery as cq
import numpy as np

screw_sizes = 1.5 + np.arange(10)/10
pin_sizes = 1 + np.arange(10)/20

block = cq.Workplane().box(36, 10, 4)

placements = np.linspace(-14, 14, 10)

for i, (x, screw, pin) in enumerate(zip(placements, screw_sizes, pin_sizes)):
    block = (block
        .faces('>Z')
        .workplane()
        .moveTo(x, 2)
        .hole(screw)
    )
    block = (block
        .faces('>Z')
        .workplane()
        .moveTo(x, -2)
        .hole(pin)
    )
    
block = block.edges("#Z").chamfer(0.75)

cq.exporters.export(block, 'holetest.stl')

if __name__ == 'temp':
    show_object(block, options={'alpha':0.8})