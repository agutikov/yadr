

SCAD_SRCS= delta_mount.scad servo_mount.scad effector.scad
STLS=$(SCAD_SRCS:.scad=.stl)

.PHONY: clean all

all: $(STLS)

%.stl: %.scad
	openscad $^ -o $@

clean:
	rm *.stl

