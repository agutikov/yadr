

STL= delta_mount.stl servo_mount.stl effector.stl
DXF= base.dxf
PS= $(DXF:.dxf=.ps)


.PHONY: clean all

all: $(STL) $(PS)

%.stl: %.scad
	openscad $^ -o $@

clean:
	rm -f *.stl *.dxf *.ps *.svg *.pdf

%.dxf: %.scad
	openscad $^ -o $@

%.ps: %.dxf
	inkscape -f $^ -P %.ps
